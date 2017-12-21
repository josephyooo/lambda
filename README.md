A dumb personal discord bot written in [Python](https://www.python.org/) 3.6 using the cogs rewrite version of [discord.py](https://github.com/Rapptz/discord.py)

I made this while also learning git and programming, so there may be mistakes

## Usage

If you want to use it, use your own [discord bot token](https://discordapp.com/developers/applications/me), [owm api key](https://home.openweathermap.org/api_keys), [google api key](https://developers.google.com/api-client-library/python/guide/aaa_apikeys), and [google custom search engine id](https://support.google.com/customsearch/answer/2649143?hl=en). Create a new file in config called 'config.json'. Inside of that file enter your keys, tokens, etc. into it following this format:
```
{
  "command_prefix": [
    "$"
  ],
  "bot_name": "lambdabot",
  "token": "TOKEN",
  "owm_api_key": "KEY",
  "cse_api_key": "KEY",
  "cse_id": "ID",
  "steam_api_key": "KEY"
}
```

## Requirements

You can install the requirements by running:
```
pip install -r requirements.txt
```
In the terminal while in the directory
