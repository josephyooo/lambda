from datetime import timedelta
from random import randint

from discord import Embed
from discord.ext import commands
from discord import Embed
from requests import get
from aiohttp import ClientSession
from async_timeout import timeout

from config.config import fs_api_key, steam_api_key

class Gamestats:
    # Commands that retrieve game statistics.
    def __init__(self, lambdabot):
        self.lambdabot = lambdabot

    @commands.command(aliases=['csgo'])
    async def csgostats(self, ctx, id: str=''):
        """Will send the given user's basic CS:GO stats."""
        if id:
            isid = False
            for part in id.split('/'):
                part = part.split()[0]
                if len(part) == 17:
                    id = part
                    isid = True
                    break
            if isid:
                try:
                    player_summary = get(
                        f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={steam_api_key}&steamids={id}').json()['response']['players']
                    stats = get(
                        f'http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=730&key={steam_api_key}&steamid={id}').json()['playerstats']['stats']
                    player_summary = player_summary[0]
                except KeyError:
                    try:
                        player_summary = player_summary[0]
                        await ctx.send("**{}** does not own csgo".format(player_summary['personaname']))
                        return
                    except:
                        await ctx.send("That steam id does not exist")
                        return
                obtained_stats = {'total_kills': 0, 'total_deaths': 0, 'total_time_played': 0,
                                  'total_shots_hit': 0, 'total_shots_fired': 0, 'total_mvps': 0}
                wanted_stats = ['total_kills', 'total_deaths', 'total_time_played',
                                'total_shots_hit', 'total_shots_fired', 'total_mvps']
                for stat in stats:
                    if stat['name'] in wanted_stats:
                        obtained_stats[stat['name']] = stat['value']
                status_codes = {0: 'Offline', 1: 'Online', 2: 'Busy', 3: 'Away',
                                4: 'Snooze', 5: 'Looking to trade', 6: 'Looking to play'}
                user_name = player_summary['personaname']
                user_status = status_codes[player_summary['personastate']]
                embed = Embed(title=f"{user_name} - {user_status}",
                              description=f"{user_name}'s CSGO statistics", color=0x0000f7)
                embed.set_thumbnail(url=player_summary['avatarfull'])
                embed.add_field(name='Kills', value='{} total kills'.format(
                    obtained_stats['total_kills']))
                embed.add_field(name='Deaths', value='{} total deaths'.format(
                    obtained_stats['total_deaths']))
                embed.add_field(
                    name='Kill/Death Ratio', value=obtained_stats['total_kills'] / obtained_stats['total_deaths'])
                embed.add_field(name='Time Played', value='~{} hours'.format(
                    obtained_stats['total_time_played'] // 3600))
                embed.add_field(name='Number of MVPs', value='{} MVPs'.format(
                    obtained_stats['total_mvps']))
                embed.add_field(name='Accuracy Rate', value='{}% of fired bullets hit'.format(round(
                    obtained_stats['total_shots_hit'] / obtained_stats['total_shots_fired'], 3) * 100))
                await ctx.send(embed=embed)
            else:
                await ctx.send("That is not a valid steam id.")
        else:
            await ctx.send("Try entering a steam user id.")

    @commands.command()
    async def fortnitestats(self, ctx, username, mode="all"):
        """Sends back the given user's overall statistics.
        Level is the total level, not the season level."""
        mode = mode.lower()
        if mode not in [mode, 'solo', 'duo', 'squad']:
            await ctx.send(f"{mode} is not a valid mode. (All, Solo, Duo, or Squad)")
            return
        username = username.replace(' ', '+')
        async with ClientSession() as session:
            async with timeout(10):
                async with session.get(f"https://fortnite.y3n.co/v2/player/{username}", headers={"X-Key": fs_api_key}) as response:
                    if response.status == 200:
                        stats = await response.json()
                        category = mode.title() if not mode == 'all' else 'Total'
                        playtime = str(timedelta(minutes=int(
                            stats['br']['stats']['pc'][mode]['minutesPlayed'])))[:-3].split(':')
                        hours = (
                            playtime[0] + " hours") if playtime[0] != '0' else ""
                        embed = Embed(author=f"{stats['displayName']}'s Fortnite Statistics'",
                                      title=f"Level {stats['br']['profile']['level']} | {hours} and {playtime[1]} minutes played | {stats['br']['stats']['pc'][mode]['matchesPlayed']} matches | {stats['br']['stats']['pc'][mode]['kills']} kills",
                                      color=randint(0, 0xffffff))
                        embed.add_field(name=f"{category} Wins",
                                        value=f"{stats['br']['stats']['pc'][mode]['wins']} Wins")
                        embed.add_field(name=f"{category} Kill / Death Ratio",
                                        value=f"{stats['br']['stats']['pc'][mode]['kpd']} Kills per Death")
                        embed.add_field(
                            name=f"{category} Kills", value=f"{stats['br']['stats']['pc'][mode]['kills']} Kills")
                        embed.add_field(
                            name=f"{category} Win Rate", value=f"{stats['br']['stats']['pc'][mode]['winRate']}% of Played Games Won")

                        await ctx.send(embed=embed)
                    else:
                        await ctx.send(f"**ERROR:** {response.text} (That username might not be valid)")


def setup(lambdabot):
    lambdabot.add_cog(Gamestats(lambdabot))
