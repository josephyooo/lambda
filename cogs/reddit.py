import discord
from discord.ext import commands
import aiohttp
import random
from os import remove
from json import load

with open('config/config.json') as cfg:
    config = load(cfg)

reddit_user = config['reddit_user']
reddit_password = config['reddit_password']

user_pass_dict = {
    'user': reddit_user,
    'password': reddit_password,
    'api_type': 'json'
}


class Reddit:

    # Commands that get stuff from reddit
    def __init__(self, lambdabot):
        self.lambdabot = lambdabot

    @commands.command(name='showerthought', aliases=['showerthoughts'],
                      description="A command that will send a random new post from r/showerthoughts.")
    async def showerthoughts(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.reddit.com/r/showerthoughts/new/.json?limit=50') as r:
                if r.status == 200:
                    js = await r.json()
                    titles = [listing['data']['title']
                              for listing in js['data']['children']][1:]
                    await ctx.send(random.choice(titles))
                else:
                    await ctx.send(f'**ERROR**: Status == {r.status}')

    @commands.command(name='meme', aliases=["memes"],
                      description="A command that will send a random post from r/dankmemes.")
    async def meme(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.reddit.com/r/dankmemes/.json?limit=50') as r:
                if r.status == 200:
                    js = await r.json()
                    titles = [listing['data']['title']
                              for listing in js['data']['children']][1:]
                    links = [listing['data']['url']
                             for listing in js['data']['children']][1:]
                    title = random.choice(titles)
                    url = links[titles.index(title)]
                    filename = 'meme' + url[-4:]
                    if url[-4:] == '.png' or url[-4:] == '.jpg' or url[-4:] == '.gif':
                        async with session.get(url) as r2:
                            image = await r2.read()
                            with open(filename, 'wb') as imgfile:
                                imgfile.write(image)
                        await ctx.send(title, file=discord.File(filename))
                        try:
                            remove(filename)
                        except Exception as e:
                            print(e)
                    else:
                        await ctx.send(title + '\n' + url)
                else:
                    await ctx.send(f"**ERROR**: Status == {r.status}")

    @commands.command(name='boottoobig',
                      description="A command that will send a random post from r/boottoobig")
    async def boottoobig(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://reddit.com/r/boottoobig/.json?limit=50') as r:
                if r.status == 200:
                    js = await r.json()
                    titles = [listing['data']['title']
                              for listing in js['data']['children']][1:]
                    links = [listing['data']['url']
                             for listing in js['data']['children']][1:]
                    title = random.choice(titles)
                    url = links[titles.index(title)]
                    filename = 'boottoobig' + url[-4:]
                    if url[-4:] == '.png' or url[-4:] == '.jpg' or url[-4:] == '.gif':
                        async with session.get(url) as r2:
                            image = await r2.read()
                            with open(filename, 'wb') as imgfile:
                                imgfile.write(image)
                        await ctx.send(title, file=discord.File(filename))
                        try:
                            remove(filename)
                        except Exception as e:
                            print(e)
                    else:
                        await ctx.send(title + '\n' + url)
                else:
                    await ctx.send(f"**ERROR**: Status == {r.status}")


def setup(lambdabot):
    lambdabot.add_cog(Reddit(lambdabot))
