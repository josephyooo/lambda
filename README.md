A dumb personal discord bot written in [Python](https://www.python.org/) 3.6 using the cogs rewrite version of [discord.py](https://github.com/Rapptz/discord.py/tree/rewrite)

I made this while also learning git and programming, so there may be mistakes

## Usage

If you want to use it, use your own [discord bot token](https://discordapp.com/developers/applications/me), [owm api key](https://home.openweathermap.org/api_keys), [google api key](https://developers.google.com/api-client-library/python/guide/aaa_apikeys), [google custom search engine id](https://support.google.com/customsearch/answer/2649143?hl=en), [steam api key](https://steamcommunity.com/dev/apikey), and [Fortnite Tracker Network API Key](https://fortnitetracker.com/site-api). Create a new file (name it 'config.py') inside of the 'config' folder. Inside of that file enter your keys, tokens, etc. into it following this format:
```
command_prefix = {command_prefix}
bot_name = {bot_name}
token = {token}
owm_api_key = {owm_api_key}
cse_api_key = {cse_api_key}
cse_id = {cse_id}
steam_api_key = {steam_api_key}
fs_api_key = {fs_api_key}
```

## Requirements

You can install the requirements by running:
```
pip install -r requirements.txt
```
In the terminal while in the directory
