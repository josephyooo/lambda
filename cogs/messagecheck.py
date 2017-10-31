from discord.ext import commands
import json
import random

with open('config/phrases.json') as phrases:
    phrases = json.load(phrases)

# with open('config/markov_models.json') as models:
#     models = json.load(models)

curses = phrases['curses']
cursephrases = phrases['cursephrases']


class Messagecheck:
    def __init__(self, lambdabot):
        self.lambdabot = lambdabot

    async def on_message(self, message):
        if not message.author.bot:
            sender = str(message.author)
            messagecon = message.content
            text = messagecon.split(" ")
            for word in text:
                if word.lower() in curses:
                    await message.channel.send(random.choice(cursephrases).format(sender[:-5]))
            # model = models[str(sender.id)]
            # model += messagecon


def setup(lambdabot):
    lambdabot.add_cog(Messagecheck(lambdabot))
