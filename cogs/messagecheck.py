from discord.ext import commands
import json
import random

with open('config/phrases.json') as phrases:
    phrases = json.load(phrases)

curses = phrases['curses']
cursephrases = phrases['cursephrases']


class Messagecheck:
    def __init__(self, lambdabot):
        self.lambdabot = lambdabot

    async def on_message(self, message):
        sender = str(message.author)
        messagecon = message.content
        text = messagecon.split(" ")
        for word in text:
            if word.lower() in curses:
                if message.author.id == 366027276975865856:
                    await message.channel.send("Stop trying to trick me!")
                else:
                    await message.channel.send(random.choice(cursephrases).format(sender[:-5]))


def setup(lambdabot):
    lambdabot.add_cog(Messagecheck(lambdabot))
