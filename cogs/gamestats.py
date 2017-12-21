from json import load
from discord import Embed
from discord.ext import commands
from requests import get

with open('config/config.json') as cfg:
    config = load(cfg)

steam_api_key = config['steam_api_key']


class Gamestats:

    # Commands that retrieve gamestats
    def __init__(self, lambdabot):
        self.lambdabot = lambdabot

    @commands.command('csgostats', aliases=['csgo'],
                      description="A command that will send the given user's kills, deaths, time played, etc.")
    async def csgostats(self, ctx, id: str=''):
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


def setup(lambdabot):
    lambdabot.add_cog(Gamestats(lambdabot))
