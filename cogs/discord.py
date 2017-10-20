import discord
from discord.ext import commands
import time


class Discord:
    def __init__(self, lambdabot):
        self.lambdabot = lambdabot

    @commands.command(name='joined', aliases=['joinedat'])
    async def joined(self, ctx, member: discord.Member):
        date = member.joined_at.strftime('%B %d, %Y')
        await ctx.send(f'"{member.name}" joined this server on {date}.')

    @commands.command(name='clear', aliases=['purge'])
    async def clear(self, ctx, amount: int):
        amount += 1
        if amount > 30:
            await ctx.send("That's too much. Please use a number below 30")
        else:
            await ctx.channel.purge(limit=amount)
            time.sleep(0.5)
            await ctx.send(f'I have cleared {amount - 1} messages.')

    @commands.command(name='id')
    async def id(self, ctx, *, member: discord.Member):
        await ctx.send(member.id)

    @commands.command(name='owner')
    async def owner(self, ctx):
        await ctx.send(ctx.guild.owner.mention)


def setup(lambdabot):
    lambdabot.add_cog(Discord(lambdabot))
