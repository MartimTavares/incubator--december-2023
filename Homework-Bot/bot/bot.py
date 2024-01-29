from webex_bot.webex_bot import WebexBot
import os
from address import Address
webex_token = os.environ["WEBEX_TOKEN"]
bot = WebexBot(webex_token)
bot.add_command(Address())
bot.run()