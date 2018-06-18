from datetime import timedelta, datetime
from random import randint
from os import environ

from discord import Embed
from discord.ext import commands
from discord import Embed
from requests import get
from aiohttp import ClientSession
from async_timeout import timeout

FS_API_KEY = environ['FS_API_KEY']
STEAM_API_KEY = environ['STEAM_API_KEY']


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
                        f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={id}').json()['response$']['players']
                    stats = get(
                        f'http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=730&key={STEAM_API_KEY}&steamid={id}').json()['playerstats']['stats']
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

    @commands.command(aliases=['fs'])
    async def fortnitestats(self, ctx, username, mode="all", platform=""):
        """Sends back the given user's overall statistics.
        Level is the total level, not the season level.
        platform can either be "pc" or "ps4"
        If someone's account is on xbox, message me their name and I'll add xbox"""
        mode = mode.lower()
        if platform == 'xbox':
            platform = "xb1"
        if mode not in ['solo', 'duo', 'squad', 'all']:
            await ctx.send(f"{mode} is not a valid mode. (All, Solo, Duo, or Squad)")
            return
        if platform not in ["pc", "ps4", "xbox", "xb1", ""]:
            await ctx.send(f"{platform} is not a valid mode. (pc, ps4, xbox/xbl)")
            return
        username = username.replace(' ', '%20')
        async with ClientSession() as session:
            async with timeout(10):
                async with session.get(f"https://fortnite.y3n.co/v2/player/{username}", headers={"X-Key": FS_API_KEY}) as resp:
                    if resp.status_code == 200:
                        stats = await resp.json()
                    else:
                        await ctx.send(f"**ERROR:** {str(resp.status_code)} - {resp.reason} (That username might not be valid)")
                        return
        if platform == "":
            if len(stats['br']['stats']) > 1:
                await ctx.send(f"{list(stats['br']['stats'].keys())} are available for this user. Choose one.")
                return
            else:
                platform = list(stats['br']['stats'].keys())[0]
        if platform not in stats['br']['stats']:
            await ctx.send(f"{platform} not available for this user. Modes {list(stats['br']['stats'].keys())} are available.")
            return
        category = mode.title() if not mode == 'all' else 'Total'
        # playtime = str(timedelta(minutes=int(
        #     stats['br']['stats'][platform][mode]['minutesPlayed'])))[:-3].split(':')
        # hours = (
        #     playtime[0] + " hours") if playtime[0] != '0' else ""
        # splittimedelta = str(timedelta(minutes=stats['br']['stats'][platform][mode]['minutesPlayed'])).split(':')
        # timemessage = f"{splittimedelta[0]} hours, {splittimedelta[1]} minutes and {splittimedelta[2]} seconds"
        # try:
        #     level = f"Level {stats['br']['profile']['level']}"
        # except KeyError:
        #     level = "Level Not Avaliable"
        # REMOVED LEVEL AND TIME UNTIL FURTHER NOTICE
        # WAS PREVIOUSLY {level} | {timemessage} played
        embed = Embed(author=f"{stats['displayName']}'s Fortnite Statistics",
                      title=f"{stats['displayName']}'s Fortnite BR stats | {stats['br']['stats'][platform][mode]['matchesPlayed']} matches | {stats['br']['stats'][platform][mode]['kills']} kills",
                      color=randint(0, 0xffffff))
        embed.add_field(
            name=f"{category} Wins",
            value=f"{stats['br']['stats'][platform][mode]['wins']} Wins")
        embed.add_field(
            name=f"{category} Kill / Death Ratio",
            value=f"{stats['br']['stats'][platform][mode]['kpd']} Kills per Death")
        embed.add_field(
            name=f"{category} Kills per Minute",
            value=f"{stats['br']['stats'][platform][mode]['kpm']} Kills per Minute")
        embed.add_field(
            name=f"{category} Win Rate",
            value=f"{stats['br']['stats'][platform][mode]['winRate']}% of Played Games Won")

        if mode != 'all':
            top = 'top10' if mode == 'solo' else 'top5' if mode == 'duo' else 'top3'
            embed.add_field(
                name=f"Number of Times in {top[:3].title()} {top[-2:]} in {category}",
                value=f"{stats['br']['stats'][platform][mode][top]}"
            )
        lastupdate = stats['lastUpdate']
        datedashsplit = lastupdate.split('-')
        day = datedashsplit[2].split('T')[0]
        time = datedashsplit[2].split('T')[1]
        # Last update UTC+11 (Default time)
        lastupdateplus11 = datetime(int(datedashsplit[0]),  # Year
                                    int(datedashsplit[1]),  # Month
                                    int(day),  # Day
                                    int(time.split(':')[0]),  # Hour
                                    int(time.split(':')[1]),  # Minute
                                    int(time.split(':')[2].split('.')[0]),  # Second
                                    int(time.split(':')[2].split('.')[1][:-1]))  # Microsecond
        # Last update UTC-5 (Eastern Standard Time)
        lastupdateeastern = lastupdateplus11 - timedelta(hours=16)
        # from datetime class to str() to datetime split into date and time ([XXX-XX-XX, XX:XX:XX.XXXXXX])
        lastupdateeastern = str(lastupdateeastern).split()
        embed.set_footer(text=f"Last Updated on {lastupdateeastern[0]} at {lastupdateeastern[1]} EST")

        await ctx.send(embed=embed)

    # old fortnite stats command that used fortnite tracker

    # @commands.command(aliases=['fs'])
    # async def fortnitestats(self, ctx, username, mode='total', platform=platform, seasonex='false'):
    #     """Gets given user's Fortnite Battle Royale statistics.
    #     Username: The player's username
    #     Mode: Can either be total, solo, duo, or squads.
    #     Platform: Can either be pc (Self Explanatory), xbl (Xbox), or psn (PlayStation).
    #     seasonex: Season exclusive, if set to true will give the player's lifetime statistics.
    #     Player's level only available for pc users. Not my fault."""

    #     # Checks if given values are valid.
    #     if mode not in ['total', 'solo', 'duo', 'squad'] or platform not in [platform, 'xbl', 'psn'] or seasonex not in ['true', 'false']:
    #         await ctx.send("Those aren't valid options. Use $help fortnitestats for more info.")
    #         return

    #     # Gets fortnite stats from tracker network.
    #     # async with ClientSession() as session:
    #     #     async with timeout(10):
    #     #         async with session.get(f"https://api.fortnitetracker.com/v1/profile/{platform}/{username}", headers={'TRN-Api-Key': FS_API_KEY}) as resp:
    #     #             if resp.status == 200:
    #     #                 stats = await resp.json()
    #     #             else:
    #     #                 await ctx.send(f"**ERROR:** {resp.text} (That username might not be valid)")
    #     #                 return
    #     resp = get(f"https://api.fortnitetracker.com/v1/profile/{platform}/{username}", headers={'TRN-Api-Key': FS_API_KEY})
    #     # if resp.status != 200:
    #     #     await ctx.send(f"**ERROR:** {resp.text} (That username might not be valid)")
    #     #     return
    #     stats = resp.json()

    #     if stats.get('error'):
    #         await ctx.send(f"**ERROR:** {stats['error']}")
    #         return

    #     if mode == 'total':
    #         embed = Embed(title=f"{stats['lifeTimeStats'][13]['value']} Played in Total | \
    #                       {stats['lifeTimeStats'][7]['value']} Matches Played in Total. | \
    #                       {stats['lifeTimeStats'][10]['value']} Total Kills.",
    #                       color=randint(0, 0xffffff))
    #         embed.set_author(name=f"{stats['epicUserHandle']}'s Fortnite Statistics")
    #         embed.add_field(name="Total wins", value=f"{stats['lifeTimeStats'][8]['value']} wins")
    #         embed.add_field(name="Total Kill / Death Ratio",
    #                         value=f"{stats['lifeTimeStats'][11]['value']} Kills per Death")
    #         embed.add_field(name="Total Win Rate",
    #                         value=f"{stats['lifeTimeStats'][9]['value']} of Played Games Won")
    #         embed.add_field(name="Total Average Survival Time",
    #                         value=f"Alive for {stats['lifeTimeStats'][14]['value']} on Average.")
    #         embed.add_field(name="Total Kills per Minute",
    #                         value=f"{stats['lifeTimeStats'][12]['value']} Kills per Minute")
            
    #         await ctx.send(embed=embed)
    #         return

    #     seasonex = True if seasonex.lower() == 'true' else False

    #     # p2 for solo, p9 for duo, and p10 for squads. I have no idea why it's like this.
    #     pmode = 'p2' if mode == 'solo' else 'p9' if mode == 'duo' else 'p10'
    #     pmode = 'curr_' + pmode if seasonex else pmode
    #     # ending is just the ending of the messages
    #     ending = 'in ' + mode.title()
    #     ending += ' this Season' if seasonex else ''

    #     embed = Embed(title=f"{stats['stats'][pmode]['top1']['displayValue']} Times Won {ending} | \
    #                   {stats['stats'][pmode]['matches']['displayValue']} Played {ending} | \
    #                   {stats['stats'][pmode]['kills']['displayValue']} Kills {ending}",
    #                   color=randint(0, 0xffffff))
    #     embed.set_author(name=f"{stats['epicUserHandle']}'s Fortnite Statistics {ending}")
    #     embed.add_field(name=f"Kill / Death Ratio {ending}",
    #                     value=f"{stats['stats'][pmode]['kd']['displayValue']} Kills per Death {ending}")
    #     try:
    #         embed.add_field(name=f"Win Ratio {ending}",
    #                         value=f"{stats['stats'][pmode]['winRatio']['value']}% of Played Games Won")
    #     except KeyError:
    #         embed.add_field(name=f"Win Ratio {ending}",
    #                         value="Unavailable.")
    #     embed.add_field(name=f"Average Survival Time {ending}",
    #                     value=f"Alive for {stats['stats'][pmode]['avgTimePlayed']['displayValue']} on Average {ending}")
        
    #     await ctx.send(embed=embed)


def setup(lambdabot):
    lambdabot.add_cog(Gamestats(lambdabot))
