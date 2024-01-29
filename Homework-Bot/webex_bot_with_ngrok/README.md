[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/DJF3/Webex-Bot-with-Ngrok)
# Webex-Bot-with-Ngrok
Basic example of a Webex bot that automatically manages it's own webhooks, making sure they point to the correct Ngrok public URL.

<img src="https://github.com/DJF3/My-Image-Repo/blob/main/webex-python-bot-ngrok.jpg?raw=true" width="650px" style="padding-left:50px;"/>

**Time to setup**: if you have setup a bot and have Python installed you can get this to work in 5-10 minutes.

**A Prepare**
- Create a bot (on [developer.webex.com](https://developer.webex.com))
- Download the code (above)
- Check if you have python: ```python -V```    The version should be 3.9 or higher
- Check if you have pip: ```python -m pip -V```    'pip' is used to install Python libraries

**B Create a folder**** for the bot and copy the bot files to this folder
- ```mkdir webex-bot-ngrok```
- ```cd webex-bot-ngrok```
- copy bot files to this folder  (when using Pipenv, also copy "Pipfile")

**C Install "Ngrok"**
- Check if you have Ngrok: ```ngrok```
- If not installed, download the [Ngrok installer](https://ngrok.com/download) and run it. 

______________ *BELOW: D/E/F/G only if you use Pipenv* ______________

**D Install "Pipenv"** (if not installed)
- Check if you have pipenv: ```pipenv -V```
- If not, install it: ```python -m pip install pipenv```


**E Create Pipfile** (***or use the provided Pipfile***)
- (Mac) ```touch Pipfile``` (or create a file called "Pipfile")
- Edit "Pipfile"
- Paste content below in the Pipfile and save it. The folder now contains 1 file: "Pipfile" and Pipenv is ready to do its job.

```source
url = "https://pypi.python.org/simple"
verify_ssl = true
name = "webex-bot-using-ngrok"
[dev-packages]
[packages]
requests = "*"
webexteamssdk = "*"
flask = "*"
[requires]
python_version = "3.9"
```

**F Setup virtual environment**
- ```Pipenv install```
- Based on the Pipfile, this creates a local environment with the required packages.

**G Activate the created virtual environment**
- ```Pipenv shell```
- Your prompt changes to indicate you are in the "isolated" setup.

NOTE: When you start the bot, you need to be in the Pipenv shell. Otherwise, it will not have the right libraries available.
alternatively: type ```pipenv run python webex-bot-ngrok.py``` This directly runs the python code inside the pipenv environment. 

______________ *ABOVE: D/E/F/G only if you use Pipenv* ______________

**H Set bot token environment variable**
- (MacOS): ```export MY_BOT_TOKEN='YOUR_TOKEN_HERE'```
- (Windows): ```set MY_BOT_TOKEN=YOUR_TOKEN_HERE```


**I Run the Bot** (Python code)
- ```python webex-bot-ngrok.py```
- When the ```___start_____``` message appears, test the bot!


**J Test the bot**
- Send ```test``` to the bot.
- It should repeat your message.
- Send ```hello``` to the bot. The not should respond differently.




# Customize code

> **webserver port** (default: 4111) -- variable: ```webserver_ port = 4111```  

> **enable debugging** (default: False) -- With debugging enabled your code will be relaunched every time you save your python code. Variable: ```webserver_debug = False```  

> **Ngrok status port number** (default for the first Ngrok tunnel you open = 4040) -- Can be useful if you run multiple Ngrok tunnels they will all have the same status URL but with a different port number (4040, 4041, 4042 etc.) Variable: ```ngrok_port = 4040```  

> **Bot token in code** instead of an environment variable (*bad practice* but if you have your reasons, I won't stop you)
How? After "my_bot_token=", replace the os.getenv with your bot token between quotes and remove the if clause after this statement.


# FAQ

- **NGROK tunnel expires after 2 hours?** Create a (free) Ngrok account and [go here](https://dashboard.ngrok.com/get-started/your-authtoken) to get your API token and see how to use it. After that, no code modifications are needed.

- **I don't want to/can use Ngrok** check out my alternative solution: [Webex Bot using Websockets](https://github.com/DJF3/Webex-Bot-with-Websockets)


# More Webex Development resources?

Go to [cs.co/webexdevinfo](http://cs.co/webexdevinfo)
