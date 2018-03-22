import asyncio

import discord
import youtube_dl

from discord.ext import commands

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'before_options': '-nostdin',
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, ytdl.extract_info, url)

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class VoiceEntry:
    def __init__(self, message, player):
        self.requester = message.author
        self.channel = message.channel
        self.player = player

    def __str__(self):
        fmt = f'***{self.player.title}*** uploaded by ***{self.player.data["uploader"]}*** and requested by ***{self.requester.display_name}***'
        duration = self.player.data['duration']
        if duration:
            fmt = fmt + ' [length: {0[0]}m {0[1]}s]'.format(divmod(duration, 60))
        return fmt


class VoiceState:
    def __init__(self, lambdabot):
        self.current = None
        self.voice = None
        self.lambdabot = lambdabot
        self.play_next_song = asyncio.Event()
        self.songs = asyncio.Queue()
        self.skip_votes = set() # a set of user_ids that voted
        self.audio_player = self.lambdabot.loop.create_task(self.audio_player_task())

    def is_playing(self):
        if self.voice is None or self.current is None:
            return False

        player = self.current.player
        return not player.is_done()

    @property
    def player(self):
        return self.current.player

    def skip(self):
        self.skip_votes.clear()
        if self.is_playing():
            self.player.stop()

    def toggle_next(self):
        self.lambdabot.loop.call_soon_threadsafe(self.play_next_song.set)

    async def audio_player_task(self):
        while True:
            self.play_next_song.clear()
            self.current = await self.songs.get()
            await self.lambdabot.send_message(self.current.channel, 'Now playing ' + str(self.current))
            self.current.player.start()
            await self.play_next_song.wait()


class Music:
    """Voice related commands."""
    def __init__(self, lambdabot):
        self.lambdabot = lambdabot
        self.voice_states = {}
    
    def get_voice_state(self, server):
        state = self.voice_states.get(server.id)
        if state is None:
            state = VoiceState(self.lambdabot)
            self.voice_states[server.id] = state

        return state

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel."""
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()
    
    @commands.command()
    async def summon(self, ctx):
        """Makes the bot join your voice channel"""
        summoned_channel = ctx.message.author.voice.channel
        if summoned_channel is None:
            await ctx.send("You aren't in a voice channel.")
            return False

        state = self.get_voice_state(ctx.message.guild)
        if state.voice is None:
            state.voice = await summoned_channel.connect()
        else:
            await state.voice.move_to(summoned_channel)
        
        return True

    # @commands.command()
    # async def play(self, ctx, *, query):
    #     """Plays a file from the local filesystem"""

    #     if ctx.voice_client is None:
    #         if ctx.author.voice.channel:
    #             await ctx.author.voice.channel.connect()
    #         else:
    #             return await ctx.send("Not connected to a voice channel.")

    #     if ctx.voice_client.is_playing():
    #         ctx.voice_client.stop()

    #     source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
    #     ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

    #     await ctx.send('Now playing: {}'.format(query))

    @commands.command()
    async def play(self, ctx, *, url):
        """
        Plays a song.
        If a link isn't provided, it will search youtube, I believe.
        The list of supported sites can be found here: https://rg3.github.io/youtube-dl/supportedsites.html
        """
        state = self.get_voice_state(ctx.message.guild)

        if state.voice is None:
            try:
                success = await ctx.invoke(self.summon)
            except:
                pass
            else:
                if not success:
                    return

        if ctx.voice_client is None:
            await ctx.send("ctx.voice_client is None")
            if ctx.author.voice.channel:
                await ctx.author.voice.channel.connect()
            else:
                return await ctx.send("Not connected to a voice channel.")

        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()

        player = await YTDLSource.from_url(url, loop=self.lambdabot.loop)
        ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        entry = VoiceEntry(ctx.message, player)
        await ctx.send(f'Now playing: {str(entry)}')
        # await state.songs.put(entry)

    # @commands.command()
    # async def volume(self, ctx, volume: int):
    #     """Changes the player's volume"""

    #     if ctx.voice_client is None:
    #         return await ctx.send("Not connected to a voice channel.")

    #     ctx.voice_client.source.volume = volume
    #     await ctx.send("Changed volume to {}%".format(volume))

    @commands.command()
    async def stop(self, ctx):
        """Stops playing audio and leaves the voice channel."""
        await ctx.voice_client.disconnect()
        await ctx.send("Disconnected")
        # server = ctx.message.guild
        # state = self.get_voice_state(server)
        
        # try:
        #     state.audio_player.cancel()
        #     del self.voice_states[server.id]
        #     await state.voice.disconnect()
        # except:
        #     pass

    @commands.command()
    async def pause(self, ctx):
        """Pauses music currently playing"""
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send(f"***{self.get_voice_state(ctx.message.guild).player.title}*** has been paused.")
        else:
            await ctx.send("Nothing's playing.")
        # if not ctx.voice_client.is_playing():
        #     await ctx.send("The currently playing song isn't playing.")
        # ctx.voice_client.pause()

    @commands.command()
    async def resume(self, ctx):
        """Resumes paused music"""
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send(f"***{self.get_voice_state(ctx.message.guild).player.title}*** has been resumed.")
        else:
            await ctx.send("Nothing's paused.")


def setup(lambdabot):
    lambdabot.add_cog(Music(lambdabot))
