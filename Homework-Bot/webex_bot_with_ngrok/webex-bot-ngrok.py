# -*- coding: utf-8 -*-
"""Webex Ngrok Bot code.
GOAL: Webex Bot code that automatically creates ngrok webhooks
BASED ON: https://github.com/DJF3/Virtual-Lamp-Code-templates, template bot
Copyright (c) 2022 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""
__author__ = "Dirk-Jan Uittenbogaard"
__email__ = "duittenb@cisco.com"
__version__ = "0.1"
__date__ = "16-July-2022"
__copyright__ = "Copyright (c) 2022 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

from flask import Flask, jsonify, request
from webexteamssdk import WebexTeamsAPI, ApiError
import sys
import json
import requests
import os

webserver_port = 3000
webserver_debug = True
# Put your BOT token in environment variable "MY_BOT_TOKEN" or replace the 4 lines below with: my_bot_token="your_bot_token"
my_bot_token = os.getenv('WEBEX_TOKEN')
if my_bot_token is None:
    print("**ERROR** environment variable 'WEBEX_TOKEN' not set, stopping.")
    sys.exit(-1)

try:
    app = Flask(__name__)
    api = WebexTeamsAPI(access_token=my_bot_token)
except Exception as e:
    print(f"**ERROR** starting Flask or the Webex API. Error message:\n{e}")
    sys.exit(-1)

#                             _
#  _ __    __ _  _ __   ___  | | __ Check for Ngrok
# | '_ \  / _` || '__| / _ \ | |/ / tunnels and get
# | | | || (_| || |   | (_) ||   <  the public_url
# |_| |_| \__, ||_|    \___/ |_|\_\ (for webhook)
#         |___/
def check_ngrok():
    try:
        response = requests.get("http://127.0.0.1:4040/api/tunnels")
        return json.loads(response.text)['tunnels'][0]['public_url'].replace("p://", "ps://")
    except Exception as e:
        return f"**ERROR** Please start 'ngrok http {webserver_port}' in another window, then run this script again.\n\n"


#                  _      _                    _
# __      __  ___ | |__  | |__    ___    ___  | | __    CHECK all WHs
# \ \ /\ / / / _ \| '_ \ | '_ \  / _ \  / _ \ | |/ /    and remove
#  \ V  V / |  __/| |_) || | | || (_) || (_) ||   <     or create WHs
#   \_/\_/   \___||_.__/ |_| |_| \___/  \___/ |_|\_\    when needed
def check_webhooks(ngrok_url):
    try:
        wh_result = api.webhooks.list()
    except ApiError as e:
        print(f"**ERROR** getting bot webhooks.\n          error message: {e}")
        sys.exit(-1)
    wh_count = len(list(wh_result))
    if wh_count > 0:
        for wh in wh_result:
            if wh.targetUrl == ngrok_url:
                print(f"___ WEBHOOK: exists!")
                break
            else:
                try:
                    api.webhooks.delete(webhookId=wh.id)
                    wh_count -= 1
                except ApiError as e:
                    print(f"**ERROR** deleting old bot webhooks.\n          error message: {e}")
    if wh_count < 1:  # ___ ZERO webhooks --> create one
        try:
            wh_result = api.webhooks.create(name="Webhook for Webex Bot with ngrok", targetUrl=ngrok_url, resource="messages", event="created")
            print(f"___ WEBHOOK: created with URL: {ngrok_url}")
        except ApiError as e:
            print(f"**ERROR** creating new webhook.\n          error message: {e}")
        wh_count = 1
    return wh_count


#  _ __ ___    ___  ___  ___   __ _   __ _   ___  ___
# | '_ ` _ \  / _ \/ __|/ __| / _` | / _` | / _ \/ __|  Process
# | | | | | ||  __/\__ \\__ \| (_| || (_| ||  __/\__ \  Bot
# |_| |_| |_| \___||___/|___/ \__,_| \__, | \___||___/  Messages
#                                    |___/
def process_message(message_obj):
    # Process messages that the bot receives.
    # Access incoming message content with: message_obj.personEmail, message_obj.text, etc. Example API msg at the end of this code.
    import ipaddress
    ip = "0.0.0.0"
    parse_error = False
    print("here")
    for str in message_obj.text.lower().split():
        if message_obj.text.lower().split()[0] == "locate" and str != "locate":
            if ipaddress.ip_address(str):
                ip = str
                parse_error = False
            else:
                parse_error == True
        elif message_obj.text.lower().split()[0] != "locate":
            parse_error = True
    if parse_error:
        msg_result = api.messages.create(toPersonEmail=message_obj.personEmail, markdown="Type command **Locate IP_ADDRESS**")
    else:
        response = requests.get("https://ipgeolocation.abstractapi.com/v1/?api_key=99dba247a0cf4efc9479304cc2d9c696&ip_address="+ip)
        print(response.status_code)
        print(response.content)
        json_string_data = response.content.decode('utf-8')
        response = json.loads(json_string_data)
        address = response['city'] + ", " + response['region'] + ", " + response['country']
        time = response['timezone']['current_time'] + ", " + response['timezone']['abbreviation']
        isp = response['connection']['isp_name']
        response_msg = f"IP address {ip} found!\n ------------------------------------------------- \n"
        response_msg += f"This IP address is located in {address}.\n"
        response_msg += f"In this location, the current time is: {time}.\n"
        response_msg += f"This data is provided by ISP {isp}."
        msg_result = api.messages.create(toPersonEmail=message_obj.personEmail, markdown="# "+ response_msg)
    
    return msg_result


#  _                                 _
# (_) _ __    ___   ___   _ __ ___  (_) _ __    __ _    Capture
# | || '_ \  / __| / _ \ | '_ ` _ \ | || '_ \  / _` |   Incoming
# | || | | || (__ | (_) || | | | | || || | | || (_| |   Webhooks
# |_||_| |_| \___| \___/ |_| |_| |_||_||_| |_| \__, |
@app.route('/', methods=["POST"])  #           |___/
def webhook():
    try:
        json_payload = request.json                             # get the webhook json message:
        message = api.messages.get(json_payload['data']['id'])  # read the message text
        if "@webex.bot" in message.personEmail:                 # don't respond to my own messages
            return ""
        print(f"___ message TEXT: '{message.text}'   ___ FROM: {message.personEmail}")
        process_message(message)
    except Exception as e:
        print(f"**ERROR** receiving the incoming webhook message.\n          error message: {e}")
        return jsonify({"success": False})
    return jsonify({"success": True})


#       _                 _
#  ___ | |_   __ _  _ __ | |_   1. check ngrok
# / __|| __| / _` || '__|| __|  2. check webhooks
# \__ \| |_ | (_| || |   | |_   3. start server
# |___/ \__| \__,_||_|    \__|

#___1 check if ngrok is running and what the public https URL is
print("\n___start_______________________")
ngrok_url = check_ngrok()
if "**ERROR**" in ngrok_url:
    print(f"\n{ngrok_url}")
    exit()

#___2 check webhooks, remove unnessecary ones and create one for the above ngrok public_url
wh_result = check_webhooks(ngrok_url)
if wh_result != 1:
    print(f"\n**ERROR** problem with your webhooks ({wh_result})")
    exit()

#___3 run webserver
app.run(host='0.0.0.0', port=webserver_port, debug=webserver_debug)  # to skip restart-on-save, add: use_reloader=False

