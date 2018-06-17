from os.path import environ
from sys import exit

from discord import __version__, Game
from discord.ext import commands
from discord.errors import LoginFailure
from discord.ext.commands.errors import CommandNotFound


try:
    TOKEN = environ['TOKEN']
    COMMAND_PREFIX = environ['COMMAND_PREFIX']
    if COMMAND_PREFIX.replace(' ', '') == '':
        print("You need something as your prefix.")
        exit()
except Exception as e:
    print(e)
    input('Are you sure you read the README.md @ https://github.com/Polokniko/lambda properly? (hint: your token or prefix cannot be found)\n')
    exit()

extensions = (
    'cogs.basic',
    'cogs.meta',
    'cogs.games',
    'cogs.reddit',
    'cogs.weather',
    'cogs.gamestats',
    'cogs.translations'
)


def get_prefix(bot, message):
    prefixes = COMMAND_PREFIX

    if message.guild.id is None:
        return '!'

    return commands.when_mentioned_or(*prefixes)(bot, message)


lambdabot = commands.Bot(COMMAND_PREFIX=get_prefix)


def main():

    # Runs when the bot starts up. Right now, it's going to print the username,
    # userid, number of servers it's on, and number of user it's connected to

    @lambdabot.event
    async def on_ready():
        print(f'\nLogged in as {lambdabot.user.name} (ID: {lambdabot.user.id})')
        print(f'Connected to {len(lambdabot.guilds)} servers')
        print(f'Connected to {str(len(set(lambdabot.get_all_members())))} users')
        print(f'Version: {__version__}')
        print('-' * 20)

        await lambdabot.change_presence(activity=Game(name=f"{COMMAND_PREFIX}help"))

    # Error handling    
    @lambdabot.event
    async def on_command_error(ctx, error):
        if isinstance(error, CommandNotFound):
            await ctx.send(f"That isn't a command. Use `{COMMAND_PREFIX}help` to view full list of commands.")
            return
        await ctx.send(f"**ERROR:** {error}")

    # Loading extensions (cogs)
    for extension in extensions:
        try:
            lambdabot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension: {extension}\n{e}')
        else:
            print(f'Successfully loaded extension: {extension}')

    try:
        lambdabot.run(TOKEN)
    except LoginFailure as e:
        print(e)
        print('Are you sure your token is correct?')


if __name__ == '__main__':
    main()
