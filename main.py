import json
import discord
from discord.ext import commands
from os.path import isfile
from discord.errors import LoginFailure

if not isfile('config/config.json'):
    input('PLEASE REREAD THE README.md @ https://github.com/Polokniko/lambda AGAIN\n')
with open('config/config.json') as cfg:
    config = json.load(cfg)

try:
    token = config['token']
    prefix = config['command_prefix']
    for prefix in prefix:
        if prefix.replace(' ', '') == '':
            input('You need something as your prefix')
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
    'cogs.music',
    'cogs.translations'
)


def get_prefix(bot, message):
    prefixes = prefix

    if message.guild.id is None:
        return '!'

    return commands.when_mentioned_or(*prefixes)(bot, message)


lambdabot = commands.Bot(command_prefix=get_prefix)


def main():

    # Runs when the bot starts up. Right now, it's going to print the username,
    # userid, number of servers it's on, and number of user it's connected to
    @lambdabot.event
    async def on_ready():
        print(f'\nLogged in as {lambdabot.user.name} (ID: {lambdabot.user.id})')
        print(f'Connected to {len(lambdabot.guilds)} servers')
        print(f'Connected to {str(len(set(lambdabot.get_all_members())))} users')
        print(f'Version: {discord.__version__}')
        print('-' * 20)

        await lambdabot.change_presence(game=discord.Game(name="$help"))
    
    @lambdabot.event
    async def on_command_error(ctx, error):
        await ctx.send(f"**ERROR:** {error}")

    for extension in extensions:
        try:
            lambdabot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension: {extension}\n{e}')
        else:
            print(f'Successfully loaded extension: {extension}')

    try:
        lambdabot.run(token)
    except LoginFailure as e:
        print(e)
        print('Are you sure your token is correct?')


if __name__ == '__main__':
    main()
