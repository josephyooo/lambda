import discord
from discord.ext import commands
import random
import json
import aiohttp
from os import remove
import time
from datetime import timedelta

with open('config/phrases.json') as phr:
    phrases = json.load(phr)

eightballphrases = phrases['8ballphrases']


class General:
    def __init__(self, lambdabot):
        self.lambdabot = lambdabot
        self.stopwatches = {}

    @commands.command(name='ping',
                      description="A command that will send the bot's latency.")
    async def ping(self, ctx):
        # ping
        await ctx.send(f'{self.lambdabot.latency * 1000} ms')

    @commands.command(name='flip', aliases=['coinflip', 'coin_flip'],
                      description="A command that will randomly send either 'Heads' or Tails'.")
    async def flip(self, ctx):
        # flip
        await ctx.send(random.choice(("Heads", "Tails")))

    @commands.command(name='8ball', aliases=['eightball'],
                      description="A command that will send a random respond to a question.")
    async def ball(self, ctx, *question: str):
        # 8ball <question>
        ctx.trigger_typing()
        if question[-1][-1] != '?':
            await ctx.send("Is that really a question?")
        else:
            await ctx.send(random.choice(eightballphrases))

    @commands.command(name='reverse',
                      description="A command that will reverse the given text")
    async def reverse(self, ctx, *, message):
        # reverse <message>
        await ctx.send(message[::-1])

    @commands.command(name='repeat',
                      description='A command that will repeat the text a number of times')
    async def repeat(self, ctx, amount: int, *, message):
        # repeat <times> <message>
        if amount > 5:
            await ctx.send("That's too much. Use a number less than 5 please.")
        else:
            for i in range(amount):
                await ctx.send(message)

    @commands.command(name='gethelp', hidden=True,
                      description="A joke command that will send the National Suicide Prevention Line formatted with the given text.")
    async def gethelp(self, ctx, *, person: str):
        # gethelp <name>
        person = person.title()
        await ctx.send(f"You're not alone **{person}**. Confidential help is available for free.\n"
                       "National Suicide Prevention Line\nCall **1-800-273-8255**\n"
                       "Available 24 hours everyday")

    @commands.command(name='cat',
                      description="A command that will send a random cat photo from random.cat")
    async def cat(self, ctx):
        # cat
        ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            async with session.get('http://random.cat/meow') as r:
                if r.status == 200:
                    js = await r.json()
                    url = js['file']
                    filename = 'cat' + url[-4:]
                    async with session.get(url) as r2:
                        image = await r2.read()
                        with open(filename, 'wb') as catimg:
                            catimg.write(image)
                    await ctx.send(file=discord.File(filename))
                    try:
                        remove(filename)
                    except Exception as e:
                        print(e)
                else:
                    await ctx.send(f"**ERROR**: Status == {r.status}")

    @commands.command(name='dog', description="A command that will send a random dog photo from shibe.online")
    async def dog(self, ctx):
        # dog
        async with aiohttp.ClientSession() as session:
            async with session.get('http://shibe.online/api/shibes?count=1') as r:
                if r.status == 200:
                    js = await r.json()
                    url = js[0]
                    filename = 'dog' + url[-4:]
                    async with session.get(url) as r2:
                        image = await r2.read()
                        with open(filename, 'wb') as dogimg:
                            dogimg.write(image)
                    await ctx.send(file=discord.File(filename))
                    try:
                        remove(filename)
                    except Exception as e:
                        print(e)
                else:
                    await ctx.send(f"**ERROR**: Status == {r.status}")

    @commands.command(name='lmgtfy',
                      description="A description that creates an lmgtfy link for you.")
    async def lmgtfy(self, ctx, *, request: str):
        # lmgtfy <request>
        request = request.replace(' ', '+')
        await ctx.send('https://lmgtfy.com/?q=' + request)

    @commands.command(name='stopwatch', aliases=['sw'],
                      description="A command that will return time elapsed between the first call and the second")
    async def stopwatch(self, ctx):
        # stopwatch
        author = ctx.message.author
        if author.id not in self.stopwatches:
            self.stopwatches[author.id] = int(time.perf_counter())
            await ctx.send('Stopwatch started!')
        else:
            time_elapsed = abs(self.stopwatches[author.id] - int(time.perf_counter()))
            time_elapsed = str(timedelta(seconds=time_elapsed))
            await ctx.send(f'Stopwatch stopped! {time_elapsed} seconds have passed.')
            self.stopwatches.pop(author.id)

    @commands.command(name='choose', aliases=['choosebetween', 'cb'],
                      description="A command that will choose between multiple choices using && to denote multiple choices")
    async def choose(self, ctx, *, choices: str=''):
        if choices > 1:
            choices = choices.split('&&')
            await ctx.send(random.choice(choices))
        else:
            await ctx.send("Not enough choices. Give me at least")

    @commands.command(name='roll',
                      description="A command that will generate a random number between 1 and user choice. Defaults to 100")
    async def roll(self, ctx, upTo: int=100):
        # roll <upTo>
        if upTo > 1:
            await ctx.send("You rolled a " + str(random.randint(1, upTo)))
        else:
            await ctx.send("Really? How about a number larger than one?")


def setup(lambdabot):
    lambdabot.add_cog(General(lambdabot))
