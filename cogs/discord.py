import discord
from discord.ext import commands
import time


class Discord:
    def __init__(self, lambdabot):
        self.lambdabot = lambdabot

    @commands.command(name='joined', aliases=['joinedat'],
                      description="A command that will send the date that a certain member has joined.")
    async def joined(self, ctx, member: discord.Member):
        # `joined <member>
        date = member.joined_at.strftime('%B %d, %Y')
        await ctx.send(f'"{member.name}" joined this server on {date}.')

    @commands.command(name='clear',
                      description="A command that will clear a specified number of messages from a channel.")
    async def clear(self, ctx, amount: int):
        # `clear <amount>
        amount += 1
        if amount > 30:
            await ctx.send("That's too much. Please use a number below 30")
        else:
            await ctx.channel.purge(limit=amount)
            time.sleep(0.5)
            await ctx.send(f'I have cleared {amount - 1} messages.')

    @commands.command(name='id',
                      description="A command that will send the given member's id")
    async def id(self, ctx, *, member: discord.Member):
        # `id <member>
        await ctx.send(f"{member.name}'s id is <{member.id}>")

    @commands.command(name='owner',
                      description="A command that will send the guild's owner.")
    async def owner(self, ctx):
        # `owner
        await ctx.send(ctx.guild.owner.mention)


def setup(lambdabot):
    lambdabot.add_cog(Discord(lambdabot))
