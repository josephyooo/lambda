import json
import discord
from discord.ext import commands

with open('config/config.json') as cfg:
    config = json.load(cfg)

token = config['token']
prefix = config['command_prefix']

extensions = (
    'cogs.default',
    'cogs.reddit',
    'cogs.owner',
    'cogs.discord',
    'cogs.messagecheck',
    'cogs.games'
)


def get_prefix(bot, message):
    prefixes = prefix

    if message.guild.id is None:
        return '!'

    return commands.when_mentioned_or(*prefixes)(bot, message)


lambdabot = commands.Bot(command_prefix=get_prefix)


def main():
    # Runs when the bot starts up. Right now, it's going to print the username, userid, number
    # of servers it's on, and number of user it's connected to
    @lambdabot.event
    async def on_ready():
        print(f'\nLogged in as {lambdabot.user.name} (ID: {lambdabot.user.id})')
        print(f'Connected to {str(len(set(lambdabot.get_all_members())))} users')
        print(f'Version: {discord.__version__}')
        print('-' * 20)

        await lambdabot.change_presence(game=discord.Game(name="$help"))

    for extension in extensions:
        try:
            lambdabot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension: {extension}\n{e}')
        else:
            print(f'Successfully loaded extension: {extension}')

    lambdabot.run(token)


if __name__ == '__main__':
    main()
