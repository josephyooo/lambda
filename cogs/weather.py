from discord.ext import commands
import discord
import pyowm
from json import load
from pyowm.exceptions.not_found_error import NotFoundError

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
        try:
            owm = pyowm.OWM(owm_api_key)
    
            observation = owm.weather_at_place(location)
            weather = observation.get_weather()
            lat = observation.get_location().get_lat()
            lon = observation.get_location().get_lon()
            ctemp = str(weather.get_temperature('celsius')['temp']) + U'\N{DEGREE SIGN}'
            ftemp = str(weather.get_temperature('fahrenheit')['temp']) + U'\N{DEGREE SIGN}'
            ktemp = str(weather.get_temperature('kelvin')['temp']) + U'\N{DEGREE SIGN}'
            wind = weather.get_wind
    
            embed = discord.Embed(title="Weather forecast for {}, ({}, {})".format(location, lat, lon), description="{} ({}% Cloud Coverage)".format(weather.get_detailed_status().title(), weather.get_clouds()), color=0x00ff80)
            embed.add_field(name='Temperature', value='{}C | {}F | {}K'.format(ctemp, ftemp, ktemp), inline=True)
            embed.add_field(name='Humidity', value='{}%'.format(weather.get_humidity()), inline=True)
            embed.add_field(name='Wind Speed',value='{}km/h | {}mph at {}'.format(round((wind('meters_sec')['speed'] * 3.6)), round(wind('miles_hour')['speed']), str(round(wind()['deg'])) + U'\N{DEGREE SIGN}'), inline=True)
            embed.add_field(name='Pressure', value='{}kPA'.format(weather.get_pressure()['press']), inline=True)
            embed.set_footer(text='Information provided by OpenWeatherMap')
    
            await ctx.send(embed=embed)
        except NotFoundError as e:
            await ctx.send(f"**ERROR**: {e}")


def setup(lambdabot):
    lambdabot.add_cog(Weather(lambdabot))
