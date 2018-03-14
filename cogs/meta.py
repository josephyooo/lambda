from discord import Member, Embed, VoiceChannel
from discord.ext import commands
from json import load, dump
from asyncio import sleep


class Meta:
    # Meta commands (having to do with the bot/discord).
    def __init__(self, lambdabot):
        self.lambdabot = lambdabot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def test(self, ctx, channel: VoiceChannel):
        """A test command. Only the bot's host can use this command."""
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
        sleep(1)
        await channel.connect()
        await ctx.voice_client.disconnect()

    @commands.command(hidden=True)
    @commands.is_owner()
    async def cog_load(self, ctx, *, cog: str):
        """Will load a certain cog extension. Only the bot's host can use this command."""
        if not cog[:5] == 'cogs.':
            cog = 'cogs.' + cog
        try:
            self.lambdabot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**ERROR:** {type(e).__name__} - {e}')
        else:
            await ctx.send(f'Successfully loaded {cog}')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def cog_unload(self, ctx, *, cog: str):
        """Will unload a certain cog extension. Only the bot's host can use this command."""
        if not cog[:5] == 'cogs.':
            cog = 'cogs.' + cog
        try:
            self.lambdabot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'**ERROR:** {type(e).__name__} - {e}')
        else:
            await ctx.send('{} successfully unloaded'.format(cog))

    @commands.command(hidden=True)
    async def cog_reload(self, ctx, *, cog: str):
        """Will reload a certain cog extension. Only the bot's host can use this command."""
        if not cog[:5] == 'cogs.':
            cog = 'cogs.' + cog
        try:
            self.lambdabot.unload_extension(cog)
            self.lambdabot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**ERROR:** {type(e).__name__} - {e}')
        else:
            await ctx.send('Successfully reloaded {}'.format(cog))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def shutdown(self, ctx):
        """Will shut down the bot. Only the bot's host can use this command."""
        await ctx.send('SHUTTING DOWN....')
        await self.lambdabot.logout()

    @commands.command(aliases=['joinedat'])
    async def joined(self, ctx, member: Member):
        """Will send the date that a certain member has joined."""
        date = member.joined_at.strftime('%B %d, %Y')
        await ctx.send(f'"{member.name}" joined this server on {date}.')

    @commands.command()
    async def clear(self, ctx, amount: int):
        """Will clear a specified number of messages from a channel."""
        if ((8192 & int(ctx.author.roles[1].permissions.value)) > 0) or ((8 & int(ctx.author.roles[1].permissions.value)) > 0):
            amount += 1
            await ctx.channel.purge(limit=amount)
            await ctx.send(f"I have cleared {amount - 1} messages.", delete_after=10)
        else:
            await ctx.send(f"Sorry, but you don't have the permissions to do so, {ctx.author.mention}. This may be due to one of your roles not having the *'Manage Messages'* permission.")

    @commands.command()
    async def id(self, ctx, *, member: Member):
        """Will send the given member's id"""
        await ctx.send(f"{member.name}'s id is <{member.id}>")

    @commands.command()
    async def owner(self, ctx):
        """Will send the guild's owner"""
        await ctx.send(ctx.guild.owner.mention)

    @commands.command()
    async def permissions(self, ctx, member: Member):
        """Will send the permissions value of a given member."""
        await ctx.send(f"{str(member)[:-5]}'s permission value is {member.roles[1].permissions.value}.\nhttps://discordapi.com/permissions.html#{member.roles[1].permissions.value}")

    @commands.command()
    async def about(self, ctx):
        """Tells you information about the bot."""
        await ctx.send("***lambda bot*** was created by ***<@270611868131786762>*** as a bot that could do some things other bots couldn't.")

    # doesn't even work properly
    @commands.command()
    async def request(self, ctx, *, request):
        """Use this command to request a command to be made."""
        guild_id = str(ctx.guild.id)
        member_id = str(ctx.author.id)
        idea = request.lower()

        with open('config/requests.json', 'r+') as requestsfile:
            requestsfilejson = load(requestsfile)
            requestsfile.seek(0)
            requestsfile.truncate()
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
                                dump(requestsfilejson, requestsfile)
                                return
                    member.append(idea)
                    dump(requestsfilejson, requestsfile)
                else:
                    guild[member_id] = [idea]
                    dump(requestsfilejson, requestsfile)
            else:
                requestsfilejson[guild_id] = {member_id: [idea]}
                dump(requestsfilejson, requestsfile)

        await ctx.send("Request filed!")

    @commands.command(aliases=['textformatting'])
    async def markdown(self, ctx):
        """Gives you help on Discord's text markdown."""
        embed = Embed(title="Text Markdown 101",
                      description="!!! Bold, italics, code blocks, and syntax highlights don't show up on embedded messages.", color=0x064fe0)
        embed.add_field(name='*Italics*', value='\*Italics\*')
        embed.add_field(name='**Bold**', value='\*\*Bold\*\*')
        embed.add_field(name='***Bold Italics***',
                        value='\*\*\*Bold Italics\*\*\*')
        embed.add_field(name='__Underline__', value='\_\_underline\_\_')
        embed.add_field(name='__*Underline Italics*__',
                        value='\_\_\*Underline Italics\*\_\_')
        embed.add_field(name='__**Underline Bold**__',
                        value='\_\_\*\*Underline Bold\*\*\_\_')
        embed.add_field(name='__***Underline Bold Italics***__',
                        value='\_\_\*\*\*Underline Bold Italics\*\*\*\_\_')
        embed.add_field(name='~~Strikethrough~~',
                        value='\~\~Strikethrough\~\~')
        embed.add_field(name='`Code Blocks`', value='\`Code Blocks\`')
        embed.add_field(name='```Multi-line\nCode Blocks```',
                        value='\`\`\`\nMulti-line\nCode Blocks!!!\n\`\`\`')
        embed.add_field(name='Syntax Highlighting',
                        value='\`\`\`python\neven_numbers = [n for n in range(10) if n % 2 == 0]\n\`\`\`')

        await ctx.send(embed=embed)


def setup(lambdabot):
    lambdabot.add_cog(Meta(lambdabot))
