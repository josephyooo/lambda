from discord.ext import commands


class Owner:
    def __init__(self, lambdabot):
        self.lambdabot = lambdabot

    @commands.command(name='load', hidden=True,
                      description="A command that will load a certain cog extension.")
    @commands.is_owner()
    async def cog_load(self, ctx, *, cog: str):
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
        try:
            self.lambdabot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'**ERROR:** {type(e).__name__} - {e}')
        else:
            await ctx.send('{} successfully unloaded'.format(cog))

    @commands.command(name='reload', hidden=True,
                      description="A command that will reload a certain cog extension.")
    async def cog_reload(self, ctx, *, cog: str):
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
    async def test(self, ctx, content: str):
        await ctx.send(content)


def setup(lambdabot):
    lambdabot.add_cog(Owner(lambdabot))
