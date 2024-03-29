from os import remove
from time import perf_counter
from random import randint, choice
from datetime import timedelta

from discord import File, Embed
from discord.ext import commands
from aiohttp import ClientSession
from googleapiclient.discovery import build
from urllib.parse import quote
from bs4 import BeautifulSoup

from config.config import cse_api_key, cse_id
from config.phrases import eightballphrases


class Basic:
    # Basic commands
    def __init__(self, lambdabot):
        self.lambdabot = lambdabot
        self.stopwatches = {}

    @commands.command(aliases=['coinflip', 'coin_flip'])
    async def flip(self, ctx):
        """Will randomly send either 'Heads' or 'Tails'."""
        await ctx.send(choice(("Heads", "Tails")))

    @commands.command(name='8ball', aliases=['eightball'])
    async def ball(self, ctx, *, question: str):
        """Will send a random response to a question."""
        # ctx.trigger_typing()
        # if question[-1][-1] != '?':
        #     await ctx.send("Is that really a question?")
        # else:
        if question.replace(' ', '') == '':
            await ctx.send("At least send something.")
        await ctx.send(choice(eightballphrases))

    @commands.command()
    async def reverse(self, ctx, *, message):
        """Will reverse the given text"""
        await ctx.send(message[::-1])

    # @commands.command()
    # async def repeat(self, ctx, amount: int, *, message):
    #     """Will repeat a given text a number of times"""
    #     if amount > 5:
    #         await ctx.send("That's too much. Use a number less than 5 please.")
    #     else:
    #         for i in range(amount):
    #             await ctx.send(message)

    @commands.command(hidden=True)
    async def gethelp(self, ctx, *, name: str):
        """A joke command that will send the National Suicide Prevention Line formatted with the given text."""
        name = name.title()
        await ctx.send(f"You're not alone **{name}**. Confidential help is available for free.\n"
                       "National Suicide Prevention Line\nCall **1-800-273-8255**\n"
                       "Available 24 hours everyday")

    @commands.command()
    async def cat(self, ctx):
        """Will send a random cat photo from random.cat"""
        ctx.trigger_typing()
        async with ClientSession() as session:
            async with session.get('http://aws.random.cat/meow') as r:
                if r.status == 200:
                    js = await r.json()
                    url = js['file']
                    filename = 'cat' + url[-4:]
                    async with session.get(url) as r2:
                        image = await r2.read()
                        with open(filename, 'wb') as catimg:
                            catimg.write(image)
                    await ctx.send(file=File(filename))
                    try:
                        remove(filename)
                    except Exception as e:
                        print(e)
                else:
                    await ctx.send(f"**ERROR**: Status == {r.status} Body == {r.text}")

    @commands.command()
    async def dog(self, ctx):
        """Will send a random dog photo from random.dog"""
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
                    await ctx.send(file=File(filename))
                    try:
                        remove(filename)
                    except Exception as e:
                        print(e)
                else:
                    await ctx.send(f"**ERROR**: Status == {r.status}")

    @commands.command()
    async def shibe(self, ctx):
        """Will send a random shibe photo from shibe.online"""
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
                    await ctx.send(file=File(filename))
                    try:
                        remove(filename)
                    except Exception as e:
                        print(e)
                else:
                    await ctx.send(f"**ERROR**: Status == {r.status}")

    @commands.command()
    async def lmgtfy(self, ctx, *, request: str):
        """A description that generates and sends an lmgtfy link for you."""
        request = request.replace(' ', '+')
        await ctx.send('https://lmgtfy.com/?q=' + request)

    @commands.command(aliases=['sw'])
    async def stopwatch(self, ctx):
        """Will return time elapsed between the first call and the second."""
        author = ctx.message.author
        if author.id not in self.stopwatches:
            self.stopwatches[author.id] = int(perf_counter())
            await ctx.send('Stopwatch started!')
        else:
            time_elapsed = abs(
                self.stopwatches[author.id] - int(perf_counter()))
            time_elapsed = str(timedelta(seconds=time_elapsed))
            await ctx.send(f'Stopwatch stopped! {time_elapsed} seconds have passed.')
            self.stopwatches.pop(author.id)

    @commands.command(aliases=['choosebetween', 'cb'])
    async def choose(self, ctx, *, choices: str=''):
        """Will choose between multiple choices using && to denote between multiple choices"""
        if not choices:
            await ctx.send("What's the point?")
            return
        choices = choices.split('&&')
        if len(choices) > 1:
            await ctx.send(choice(choices))
        else:
            await ctx.send("Not enough choices. Give me at least 2 choices to pick from.")

    @commands.command()
    async def roll(self, ctx, upTo: int=6):
        """
        Will generate a random number between 1 and user choice.
        Defaults to 6.
        """
        if upTo > 1:
            await ctx.send("You rolled a " + str(randint(1, upTo)))
        else:
            await ctx.send("Really? How about a number larger than one?")

    @commands.command(aliases=['g'])
    async def google(self, ctx, results: str, *, query: str=''):
        """
        Searches using google
        Will send a specified amount of search results from google.
        """
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
            results = service.cse().list(q=query, cx=cse_id,
                                         num=results).execute()['items']
            embed = Embed(title="Search Results", color=randint(0, 0xffffff))
            for result in results:
                embed.add_field(name=result['title'],
                                value=result['link'], inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("What do you want me to search for you?")

    @commands.command(aliases=['ub'])
    async def urbandictionary(self, ctx, results: str, *, query: str=''):
        """
        Searches Urban Dictionary
        Will send a specified amount of search results from urban dictionary.
        """
        try:
            results = int(results)
            if results < 1:
                await ctx.send("What's the point of getting no results back?")
        except ValueError:
            await ctx.send("How many results do you want? ($urbandictionary ***<results>*** <query>)")
            return
        if results > 10:
            await ctx.send("Less than 20 results please.")
            return
        elif query:
            async with ClientSession() as session:
                async with session.get(f'https://api.urbandictionary.com/v0/define?term={quote(query)}') as r:
                    if r.status == 200:
                        json = await r.json()
                        definitions = json['list']
                        embed = Embed(
                            title="Search Results", color=randint(0, 0xffffff))
                        for item in definitions[0:results]:
                            embed.add_field(
                                name=f"Result #{str(definitions.index(item) + 1)}", value=item['definition'], inline=False)
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send(f"**ERROR**: Status == {r.status}")
        else:
            await ctx.send("Try giving me something to search.")

    @commands.command(aliases=['randomfact'])
    async def fact(self, ctx):
        """Sends a random fact from unkno.com"""
        async with ClientSession() as session:
            async with session.get('http://unkno.com/') as r:
                soup = BeautifulSoup(await r.text(), "html.parser")
                facts = soup.find('div', attrs={'id': 'content'})
                for fact in facts:
                    await ctx.send(fact)
    
    # @commands.command()
    # async def trivia(self, ctx, difficulty='easy', count='1'):
    #     """
    #     Sends a random trivia question.
    #     Difficulty options are 'easy', 'medium', 'hard'
    #     Count is just the number of questions
    #     """
    #     async with ClientSession() as session:
    #         async with session.get(f'https://opentdb.com/api.php?amount={count}&difficulty={difficulty}') as resp:
    #             if r.status = 200:
    #                 json = await r.json()


def setup(lambdabot):
    lambdabot.add_cog(Basic(lambdabot))
