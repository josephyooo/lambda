import discord
from discord.ext import commands
import random
import json
import aiohttp
from os import remove

with open('config/phrases.json') as phr:
    phrases = json.load(phr)

eightballphrases = phrases['8ballphrases']


class General:
    def __init__(self, lambdabot):
        self.lambdabot = lambdabot

    @commands.command(name='ping',
                      description="A command that will send the bot's latency.")
    async def ping(self, ctx):
        # `ping
        await ctx.send(f'{self.lambdabot.latency * 1000} ms')

    @commands.command(name='flip', aliases=['coinflip', 'coin_flip'],
                      description="A command that will randomly send either 'Heads' or Tails'.")
    async def flip(self, ctx):
        # `flip
        await ctx.send(random.choice(("Heads", "Tails")))

    @commands.command(name='8ball', aliases=['eightball'],
                      description="A command that will send a random respond to a question.")
    async def ball(self, ctx, *question: str):
        # `8ball <question>
        ctx.trigger_typing()
        if question[-1][-1] != '?':
            await ctx.send("Is that really a question?")
        else:
            await ctx.send(random.choice(eightballphrases))

    @commands.command(name='reverse',
                      description="A command that will reverse the given text")
    async def reverse(self, ctx, *, message):
        # `reverse <message>
        await ctx.send(message[::-1])

    @commands.command(name='repeat',
                      description='A command that will repeat the text a number of times')
    async def repeat(self, ctx, amount: int, *, message):
        # `repeat <times> <message>
        if amount > 5:
            await ctx.send("That's too much. Use a number less than 5 please.")
        else:
            for i in range(amount):
                await ctx.send(message)

    @commands.command(name='gethelp',
                      description="A joke command that will send the National Suicide Prevention Line formatted with the given text.")
    async def gethelp(self, ctx, *, person: str):
        # `gethelp <name>
        person = person.title()
        await ctx.send(f"You're not alone **{person}**. Confidential help is available for free.\n"
                       "National Suicide Prevention Line\nCall **1-800-273-8255**\n"
                       "Available 24 hours everyday")

    @commands.command(name='cat',
                      description="A command that will send a random cat photo from random.cat")
    async def cat(self, ctx):
        # `cat
        filename = None
        ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            async with session.get('http://random.cat/meow') as r:
                if r.status == 200:
                    js = await r.json()
                    url = js['file']
                    filename = 'cat' + url[-4:]
                    async with session.get(url) as resp2:
                        test = await resp2.read()
                        with open(filename, 'wb') as catimg:
                            catimg.write(test)
        await ctx.send(file=discord.File(filename))
        try:
            remove(filename)
        except Exception as e:
            print(e)

    @commands.command(name='dog', description="A command that will send a random dog photo from shibe.online")
    async def dog(self, ctx):
        # `dog
        filename = None
        async with aiohttp.ClientSession() as session:
            async with session.get('http://shibe.online/api/shibes?count=1') as r:
                if r.status == 200:
                    js = await r.json()
                    url = js[0]
                    filename = 'dog' + url[-4:]
                    async with session.get(url) as resp2:
                        test = await resp2.read()
                        with open(filename, 'wb') as dogimg:
                            dogimg.write(test)
        await ctx.send(file=discord.File(filename))
        try:
            remove(filename)
        except Exception as e:
            print(e)


def setup(lambdabot):
    lambdabot.add_cog(General(lambdabot))
