# Annoncement Bot originally made for EU-81's CroissantFR guild on Isekai Slow Life
## Made by vicic8484/DalKael

## Setup :
```sh
cp .env.example .env
nano .env # put your token and timezone in the .env file
pip3 install -r requirements.txt
python3 bot.py
```
>**Important** if you have discord.py installed, uninstall it or use a virtual environment to avoid conflicts.

## Usage :
It is made to be used with the following slash commands but it is also possible to directly edit the messages.txt file and restart the bot to update the messages.
>**Important :** you need to have a role named "staff" to use the commands.

/list : List all the programmed messages for the current server with the correspond timestamp and a link to the channel.

/add [timecode] [channel_id] [message] Add a message to the list with the provided timecode that will be sent to the provided channel_id.

>note : you can add pings by using <@&"role_id"> or <@!"user_id"> in the message (replacing "role_id" or "user_id" by their corresponding values).

>note : the timecode is in the format "HH:MM" or "HH:MM:SS" and the timezone can be defined in the .env file.

/remove [index] Remove the message at the provided index (refer to /list for the index of each message, they are independant per server).

/reload_messages Reload the messages from the messages.txt file.

## Dependencies :
Outside of the standard library, the bot uses the following dependencies :
- py-cord : to interact with the discord API.
- python-dotenv : to load the token from the .env file.
- pytz : to handle timezones. 


It isn't perfect but we had problem with the bot we used before so I made this one to replace it as coding practice and because I wanted to try working with the discord API and slash commands.

Sorry if something is broken and I didn't catch it.