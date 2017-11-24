from discord import Member
from discord.ext import commands
from json import load, dump


class Meta:

    # Meta commands (having to do with the bot/discord)
    def __init__(self, lambdabot):
        self.lambdabot = lambdabot
    
    @commands.command(name='load', hidden=True,
                      description="A command that will load a certain cog extension.")
    @commands.is_owner()
    async def cog_load(self, ctx, *, cog: str):
        if not cog[:5] == 'cogs.':
            cog = 'cogs.' + cog
        try:
            self.lambdabot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**ERROR:** {type(e).__name__} - {e}')
        else:
            await ctx.send(f'Successfully loaded {cog}')

    @commands.command(name='unload', hidden=True,
                      description="A command that will unload a certain cog extension.")
    @commands.is_owner()
    async def cog_unload(self, ctx, *, cog: str):
        if not cog[:5] == 'cogs.':
            cog = 'cogs.' + cog
        try:
            self.lambdabot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'**ERROR:** {type(e).__name__} - {e}')
        else:
            await ctx.send('{} successfully unloaded'.format(cog))

    @commands.command(name='reload', hidden=True,
                      description="A command that will reload a certain cog extension.")
    async def cog_reload(self, ctx, *, cog: str):
        if not cog[:5] == 'cogs.':
            cog = 'cogs.' + cog
        try:
            self.lambdabot.unload_extension(cog)
            self.lambdabot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**ERROR:** {type(e).__name__} - {e}')
        else:
            await ctx.send('Successfully reloaded {}'.format(cog))

    @commands.command(name='shutdown', hidden=True,
                      description="A command that will shut down the bot")
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.send('SHUTTING DOWN....')
        await self.lambdabot.logout()

    @commands.command(name='test', hidden=True,
                      description="A test command for my creator's testing needs.")
    @commands.is_owner()
    async def test(self, ctx):
        await ctx.send(type(ctx.guild.id))

    @commands.command(name='joined', aliases=['joinedat'],
                      description="A command that will send the date that a certain member has joined.")
    async def joined(self, ctx, member: Member):
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
    async def id(self, ctx, *, member: Member):
        await ctx.send(f"{member.name}'s id is <{member.id}>")

    @commands.command(name='owner',
                      description="A command that will send the guild's owner.")
    async def owner(self, ctx):
        await ctx.send(ctx.guild.owner.mention)
    
    @commands.command(name='permissions',
                      description="A command that will send the permission value of a given member.")
    async def permissions(self, ctx, member: Member):
        await ctx.send(f"{str(member)[:-5]}'s permission value is {member.roles[1].permissions.value}.\nhttps://discordapi.com/permissions.html#{member.roles[1].permissions.value}")
    
    @commands.command(name='about',
                      description="A command that send a brief description of the bot.")
    async def about(self, ctx):
        await ctx.send("***lambda bot*** was created by ***<@270611868131786762>*** as a bot that could do some things other bots couldn't and to practice using python.")
    
    @commands.command(name='request',
                      description="A command that will request for a command to be made.")
    async def request(self, ctx, *, request):
        guild_id = str(ctx.guild.id)
        member_id = str(ctx.author.id)
        idea = request.lower()
        
        with open('config/requests.json', 'r+') as requestsfile:
            requestsfilejson = load(requestsfile)
        if requestsfilejson.__contains__(guild_id):
            requester_guild = requestsfilejson[guild_id]
            if requester_guild.__contains__(member_id):
                member = requester_guild[member_id]
                for guild_key in requestsfilejson:
                    guild = requestsfilejson[guild_key]
                    for guild_member_key in guild:
                        guild_member = guild[guild_member_key]
                        if idea in guild_member:
                            await ctx.send("That request has already been filed previously.")
                            return
                member.append(idea)
            else:
               guild[member_id] = [idea]
        else:
            requestsfilejson[guild_id] = {member_id: [idea]}
        with open('config/requests.json', 'w') as requestsfile:
            dump(requestsfilejson, requestsfile)
        
        await ctx.send("Request filed!")


def setup(lambdabot):
    lambdabot.add_cog(Meta(lambdabot))
