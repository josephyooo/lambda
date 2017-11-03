from discord.ext import commands
import pyowm
from json import load

with open('config/config.json') as cfg:
    config = load(cfg)

owm_api_key = config['owm_api_key']


class Weather:
    def __init__(self, lambdabot):
        self.lambdabot = lambdabot

    @commands.command(name="forecast", aliases=['weather'],
                      description="A command that will send the given location's weather forecast")
    async def forecast(self, ctx, *, location: str=''):
        # forecast <unit> <location>
        owm = pyowm.OWM(owm_api_key)

        observation = owm.weather_at_place(location)
        weather = observation.get_weather()
        lat = observation.get_location().get_lat()
        lon = observation.get_location().get_lon()
        temp = weather.get_temperature('celsius')['temp']
        wind = weather.get_wind()

        await ctx.send('**Latitude:** {}, **Longitude:** {}'.format(lat, lon))
        await ctx.send('**Temperature:** {} celsius'.format(str(temp) + u'\N{DEGREE SIGN}'))
        await ctx.send('**Humidity:** {}'.format(str(weather.get_humidity()) + '%'))
        await ctx.send('**Wind Speed:** {} at {}'.format(str(wind['speed']) + ' m/s', str(wind['deg']) + u'\N{DEGREE SIGN}'))
        await ctx.send('**Detailed Status:** {}'.format(weather.get_detailed_status()))


def setup(lambdabot):
    lambdabot.add_cog(Weather(lambdabot))
