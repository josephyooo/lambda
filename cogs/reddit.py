from random import choice
from re import findall
import discord
from discord.ext import commands
import aiohttp
from async_timeout import timeout


class Reddit:
    # A command that gets stuff from reddit
    def __init__(self, lambdabot):
        self.lambdabot = lambdabot

    @commands.command()
    async def reddit(self, ctx, subreddit: str='', limit: str='1', sort: str='hot', oftop: int=50):
        """
        Will send a semi-random reddit post from the given subreddit.
        By default, it'll send the title, selftext, url, and score of a random post in the top 50 of the given subreddit.
        """
        if not subreddit:
            await ctx.send('Please enter a subreddit.')
        async with aiohttp.ClientSession() as session:
            with timeout(10):
                async with session.get(f'https://reddit.com/r/{subreddit}/{sort}/.json?limit={oftop}') as response:
                    json = await response.json()
            for post in json['data']['children']:
                if post['data']['stickied']:
                    json['data']['children'].remove(post)
            for i in limit:
                post = choice(json['data']['children'])
                embed = discord.Embed(title=post['data']['title'], description='Author: {}, Score: {} points'.format(
                    post['data']['author'], post['data']['score']))
                await ctx.send(embed=embed)
                selftext = post['data']['selftext']
                if selftext:
                    while len(selftext) > 2000:
                        await ctx.send(selftext[:2000])
                        selftext = selftext[2000:]
                    if selftext:
                        await ctx.send(selftext)
                await ctx.send(post['data']['url']) if not findall(r'r/([a-zA-Z]*)/comments', post['data']['url']) else None

            '''
            for post in json['data']['children']:
                post = random.choice(json['data']['children'])
                if not post['data']['stickied']:
                    for i in limit:
                        embed = discord.Embed(title=post['data']['title'], description='Author: {}, Score: {} points'.format(
                            post['data']['author'], post['data']['score']))
                        embed.add_field(
                            name="Text", value=post['data']['selftext']) if post['data']['selftext'] else None
                        await ctx.send(embed=embed)
                        await ctx.send(post['data']['url'])
            '''


def setup(lambdabot):
    lambdabot.add_cog(Reddit(lambdabot))
