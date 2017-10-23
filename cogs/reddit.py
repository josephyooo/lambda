from discord.ext import commands
import aiohttp
from random import choice

user_pass_dict = {
    'user': 'USERNAME',
    'password': 'PASSWORD',
    'api_type': 'json'
}

class Reddit:
    def __init__(self, lambdabot):
        self.lambdabot = lambdabot

    @commands.command(name='showerthought', aliases=['showerthoughts'],
                      description="A command that will return a random new post from r/showerthoughts.")
    async def showerthoughts(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.reddit.com/r/showerthoughts/new/.json?limit=50') as r:
                if r.status == 200:
                    js = await r.json()
                    titles = [listing['data']['title'] for listing in js['data']['children']][1:]

        await ctx.send(choice(titles))


def setup(lambdabot):
    lambdabot.add_cog(Reddit(lambdabot))
