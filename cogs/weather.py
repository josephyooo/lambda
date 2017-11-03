from discord.ext import commands
import pyowm
from json import load

with open('config/config.json') as cfg:
    config = load(cfg)

owm_api_key = config['owm_api_key']


class Weather:
    def __init__(self, lambdabot):
        self.lambdabot = lambdabot

    @commands.command(name="forecast",
                      description="A command that will send the given location's weather forecast. unit parameter is optional")
    async def forecast(self, ctx, *, location: str=''):
        # forecast <unit> <location>
        owm = pyowm.OWM(owm_api_key)

        observation = owm.weather_at_place(location)
        weather = observation.get_weather()
        foundloc = observation.get_location().get_name()
        temp = weather.get_temperature('celsius')['temp']
        windspd = str(weather.get_wind()['speed'])

        await ctx.send('**Found Location:** {}'.format(foundloc))
        await ctx.send('**Temperature:** {} celsius'.format(str(temp) + u'\N{DEGREE SIGN}'))
        await ctx.send('**Humidity:** {}'.format(str(weather.get_humidity()) + '%'))
        await ctx.send('**Wind Speed:** {}'.format(windspd + ' m/s'))
        await ctx.send('**Detailed Status:** {}'.format(weather.get_detailed_status()))


def setup(lambdabot):
    lambdabot.add_cog(Weather(lambdabot))
