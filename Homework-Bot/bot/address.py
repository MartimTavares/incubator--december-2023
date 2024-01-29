from webex_bot.models.command import Command
import requests
import json

class Address(Command):
    def __init__(self):
        super().__init__(
            command_keyword="Locate",
            help_message="Get current location and time of an IP address.",
            card=None
        )
    def execute(self, message, attachment_actions, activity):
        IPADDRESS_KEY = "99dba247a0cf4efc9479304cc2d9c696"
        url = "https://ipgeolocation.abstractapi.com/v1/?api_key="
        url += f"{IPADDRESS_KEY}&ip_address="
        url += f"{message}"

        json_string_data = response.content.decode('utf-8')
        response = json.loads(json_string_data)
        address = response['city'] + ", " + response['region'] + ", " + response['country']
        time = response['timezone']['current_time'] + ", " + response['timezone']['abbreviation']
        isp = response['connection']['isp_name']
        response_msg = f"IP address {ip} found!\n ------------------------------------------------- \n"
        response_msg += f"This IP address is located in {address}.\n"
        response_msg += f"In this location, the current time is: {time}.\n"
        response_msg += f"This data is provided by ISP {isp}."
        return response_msg

