import discord
from discord.ext import commands
import time


class Discord:

    # Commands that have to do with discord
    def __init__(self, lambdabot):
        self.lambdabot = lambdabot

    @commands.command(name='joined', aliases=['joinedat'],
                      description="A command that will send the date that a certain member has joined.")
    async def joined(self, ctx, member: discord.Member):
        date = member.joined_at.strftime('%B %d, %Y')
        await ctx.send(f'"{member.name}" joined this server on {date}.')

    @commands.command(name='clear',
                      description="A command that will clear a specified number of messages from a channel.")
    async def clear(self, ctx, amount: int):
        if (8192 & int(ctx.author.roles[1].permissions.value)) > 0:
            amount += 1
            await ctx.channel.purge(limit=amount)
            await ctx.send(f"I have cleared {amount - 1} messages.", delete_after=10)
        else:
            await ctx.send(f"Sorry, but you don't have the permissions to do so, {ctx.author.mention}")

    @commands.command(name='id',
                      description="A command that will send the given member's id")
    async def id(self, ctx, *, member: discord.Member):
        await ctx.send(f"{member.name}'s id is <{member.id}>")

    @commands.command(name='owner',
                      description="A command that will send the guild's owner.")
    async def owner(self, ctx):
        await ctx.send(ctx.guild.owner.mention)
    
    @commands.command(name='permissions',
                      description="A command that will send the permission value of a given member.")
    async def permissions(self, ctx, member: discord.Member):
        await ctx.send(f"{member}'s permission value is {member.roles[1].permissions.value}.")


def setup(lambdabot):
    lambdabot.add_cog(Discord(lambdabot))
