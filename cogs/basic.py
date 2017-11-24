import discord
from discord.ext import commands
import random
from json import load
from aiohttp import ClientSession
from os import remove
from time import perf_counter
from datetime import timedelta
from googleapiclient.discovery import build
from asyncio import sleep
from urllib.parse import quote
from bs4 import BeautifulSoup

with open('config/config.json') as cfg:
    config = load(cfg)

with open('config/phrases.json') as phr:
    phrases = load(phr)

cse_api_key = config['cse_api_key']
cse_id = config['cse_id']
eightballphrases = phrases['8ballphrases']


class Basic:

    # Basic Commands
    def __init__(self, lambdabot):
        self.lambdabot = lambdabot
        self.stopwatches = {}

    @commands.command(name='ping',
                      description="A command that will send the bot's latency.")
    async def ping(self, ctx):
        await ctx.send(f'{self.lambdabot.latency * 1000} ms')

    @commands.command(name='flip', aliases=['coinflip', 'coin_flip'],
                      description="A command that will randomly send either 'Heads' or Tails'.")
    async def flip(self, ctx):
        await ctx.send(random.choice(("Heads", "Tails")))

    @commands.command(name='8ball', aliases=['eightball'],
                      description="A command that will send a random respond to a question.")
    async def ball(self, ctx, *question: str):
        ctx.trigger_typing()
        if question[-1][-1] != '?':
            await ctx.send("Is that really a question?")
        else:
            await ctx.send(random.choice(eightballphrases))

    @commands.command(name='reverse',
                      description="A command that will reverse the given text")
    async def reverse(self, ctx, *, message):
        await ctx.send(message[::-1])

    @commands.command(name='repeat',
                      description='A command that will repeat the text a number of times')
    async def repeat(self, ctx, amount: int, *, message):
        if amount > 5:
            await ctx.send("That's too much. Use a number less than 5 please.")
        else:
            for i in range(amount):
                await ctx.send(message)

    @commands.command(name='gethelp', hidden=True,
                      description="A joke command that will send the National Suicide Prevention Line formatted with the given text.")
    async def gethelp(self, ctx, *, name: str):
        name = name.title()
        await ctx.send(f"You're not alone **{name}**. Confidential help is available for free.\n"
                       "National Suicide Prevention Line\nCall **1-800-273-8255**\n"
                       "Available 24 hours everyday")

    @commands.command(name='cat',
                      description="A command that will send a random cat photo from random.cat")
    async def cat(self, ctx):
        ctx.trigger_typing()
        async with ClientSession() as session:
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

    @commands.command(name='dog', description="A command that will send a random dog photo from random.dog")
    async def dog(self, ctx):
        async with ClientSession() as session:
            async with session.get('https://random.dog/woof.json') as r:
                if r.status == 200:
                    js = await r.json()
                    url = js['url']
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

    @commands.command(name='shibe', description="A command that will send a random shibe photo from shibe.online")
    async def shibe(self, ctx):
        async with ClientSession() as session:
            async with session.get('http://shibe.online/api/shibes?count=1') as r:
                if r.status == 200:
                    js = await r.json()
                    url = js[0]
                    filename = 'shibe' + url[-4:]
                    async with session.get(url) as r2:
                        image = await r2.read()
                        with open(filename, 'wb') as shibeimg:
                            shibeimg.write(image)
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
        request = request.replace(' ', '+')
        await ctx.send('https://lmgtfy.com/?q=' + request)

    @commands.command(name='stopwatch', aliases=['sw'],
                      description="A command that will return time elapsed between the first call and the second")
    async def stopwatch(self, ctx):
        author = ctx.message.author
        if author.id not in self.stopwatches:
            self.stopwatches[author.id] = int(perf_counter())
            await ctx.send('Stopwatch started!')
        else:
            time_elapsed = abs(self.stopwatches[author.id] - int(perf_counter()))
            time_elapsed = str(timedelta(seconds=time_elapsed))
            await ctx.send(f'Stopwatch stopped! {time_elapsed} seconds have passed.')
            self.stopwatches.pop(author.id)

    @commands.command(name='choose', aliases=['choosebetween', 'cb'],
                      description="A command that will choose between multiple choices using && to denote multiple choices")
    async def choose(self, ctx, *, choices: str=''):
        if not choices:
            await ctx.send("What's the point?")
            return
        choices = choices.split('&&')
        if len(choices) > 1:
            await ctx.send(random.choice(choices))
        else:
            await ctx.send("Not enough choices. Give me at least 2 choices to pick from.")

    @commands.command(name='roll',
                      description="A command that will generate a random number between 1 and user choice. Defaults to 100")
    async def roll(self, ctx, upTo: int=100):
        if upTo > 1:
            await ctx.send("You rolled a " + str(random.randint(1, upTo)))
        else:
            await ctx.send("Really? How about a number larger than one?")
    
    @commands.command(name='google', aliases=['g'],
                      description="A command that will send a specified amount of search results from google.")
    async def google(self, ctx, results: str, *, query: str=''):
        try:
            results = int(results)
        except ValueError:
            await ctx.send("How many results do you want? ($google ***<results>*** <query>)")
            return
        if results > 10:
           await ctx.send("Less than 10 results please.") 
           return
        elif query:
            service = build("customsearch", "v1", developerKey=cse_api_key)
            results = service.cse().list(q=query, cx=cse_id, num=results).execute()['items']
            embed = discord.Embed(title="Search Results", color=0x00E9FF)
            for result in results:
                embed.add_field(name=result['title'], value=result['link'], inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("What do you want me to search for you?")
    
    @commands.command(name='urbandictionary', aliases=['ub'],
                      description="A command that will send a search result of the given request in urban dictionary.")
    async def urbandictionary(self, ctx, results: str, *, query: str=''):
        try:
            results = int(results)
            if results < 1:
                await ctx.send("What's the point of getting no results back?")
        except ValueError:
            await ctx.send("How many results do you want? ($urbandictionary ***<results>*** <query>)")
            return
        if results > 20:
            await ctx.send("Less than 20 results please.")
            return
        elif query:
            async with ClientSession() as session:
                async with session.get(f'https://api.urbandictionary.com/v0/define?term={quote(query)}') as r:
                    if r.status == 200:
                        json = await r.json()
                        definitions = json['list']
                        embed = discord.Embed(title="Search Results", color=0x0000ff)
                        for item in definitions[0:results]:
                            embed.add_field(name=f"Result #{str(definitions.index(item) + 1)}", value=item['definition'], inline=False)
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send(f"**ERROR**: Status == {r.status}")
        else:
            await ctx.send("Try giving me something to search.")
    
    @commands.command(name='fact', aliases=['randomfact'],
                      description="Sends a random fact")
    async def fact(self, ctx):
        async with ClientSession() as session:
            async with session.get('http://unkno.com/') as r:
                soup = BeautifulSoup(await r.text(), "html.parser")
                facts = soup.find('div', attrs={'id': 'content'})
                for fact in facts:
                    await ctx.send(fact)

    @commands.command(name='texttobinary', aliases=['binaryfromtext', 'ttb', 'bft'],
                      description="Translates text into binary")
    async def texttobinary(self, ctx, *, text):
        if text:
            bits = bin(int.from_bytes(text.encode('utf-8', 'surrogatepass'), 'big'))[2:]
            bits = bits.zfill(8 * ((len(bits) + 7) // 8))
            result = ''
            for n in range(len(bits) // 8):
                result += bits[:8] + ' '
                bits = bits[8:]
            await ctx.send(result)
        else:
            await ctx.send("What do you want me to translate?")

    @commands.command(name='binarytotext', aliases=['textfrombinary', 'btt', 'tfb'])
    async def binarytotext(self, ctx, *, binary):
            binary = ''.join(binary.split())
            try:
                n = int(binary, 2)
            except ValueError:
                await ctx.send("I need binary, not text")
                return
            await ctx.send(n.to_bytes((n.bit_length() + 7) // 8, 'big').decode('utf-8', 'surrogatepass') or '\0')


def setup(lambdabot):
    lambdabot.add_cog(Basic(lambdabot))