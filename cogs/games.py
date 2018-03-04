from discord.ext import commands
from random import randint


class Games:

    # Game commands
    def __init__(self, lambdabot):
        self.lamdabot = lambdabot

    @commands.command(aliases=["guessinggame", "guessing_game"])
    async def guess(self, ctx):
        """Plays a guessing game with the author of the command."""
        async def play():
            try:
                await ctx.send("Let's play the guessing game! What number would you like to guess to?")
                upto = await self.lamdabot.wait_for('message', check=lambda message: message.author == ctx.author)
                if upto.content == 'quit':
                    return
                if int(upto.content) < 3:
                    await ctx.send("That's too low, please use a number above 3.")
                    await play()
                answer = randint(1, int(upto.content))
                await ctx.send(f"Alright! You have **5** tries to guess a number between 1 and {int(upto.content)}")
                guess = await self.lamdabot.wait_for('message', check=lambda message: message.author == ctx.author)
                attempts = 1

                while int(guess.content) != answer:
                    if attempts == 5:
                        await ctx.send("You have no more tries! Game over!")
                        break
                    else:
                        attempts += 1
                        if int(guess.content) > answer:
                            await ctx.send(f"Your guess is too high, try again!")
                            guess = await self.lamdabot.wait_for('message',
                                                                 check=lambda message: message.author == ctx.author)
                        else:
                            await ctx.send(f"Your guess is too low, try again!")
                            guess = await self.lamdabot.wait_for('message',
                                                                 check=lambda message: message.author == ctx.author)
                else:
                    if attempts <= 1:
                        await ctx.send("Nice! It only took you one try to get it right!")
                    else:
                        await ctx.send(f"Nice! It took you **{attempts}** tries to get it right!")
                    await gameover()
            except ValueError:
                await ctx.send("Please return a number.\nEnding game...")

        async def gameover():
            await ctx.send("Would you like to play another game? **Yes** / **No**")
            response = await self.lamdabot.wait_for('message', check=lambda message: message.author == ctx.author)
            response = response.content.lower()

            if response == 'yes':
                await ctx.send("Alright! Starting a new game!")
                await play()
            elif response == 'no':
                await ctx.send("Alright! Thanks for playing!")
            else:
                await ctx.send("Not a choice, **Yes** / **No**")
                await gameover()

        await play()

    @commands.command(aliases=["rockpaperscissors", "rock_paper_scissors"])
    async def rps(self, ctx):
        """Plays a game of rps with the author of the command."""
        async def play():
            await ctx.send("Let's play **RPS**! Choose your weapon of choice.")
            choices = ('rock', 'paper', 'scissors')
            bot_choice = choices[randint(0, 2)]
            player_choice = await self.lamdabot.wait_for('message', check=lambda message: message.author == ctx.author)
            player_choice = player_choice.content.lower()

            beats = {
                'rock': ['scissors'],
                'paper': ['rock'],
                'scissors': ['paper']
            }

            if bot_choice and player_choice in choices:
                if bot_choice == player_choice:
                    await ctx.send(f"**Tie!** You both chose **{bot_choice.title()}**")
                    await gameover()
                elif player_choice in beats[bot_choice]:
                    await ctx.send(f"**You won!** Lambda chose **{bot_choice.title()}** and you chose **{player_choice.title()}**!")
                    await gameover()
                else:
                    await ctx.send(f"**You lost!** Lambda chose **{bot_choice.title()}** and you chose **{player_choice.title()}**!")
                    await gameover()
            else:
                await ctx.send("Please choose **Rock, Paper, or Scissors**.\nEnding game...")

        async def gameover():
            await ctx.send("Would you like to play again? **Yes** / **No**")
            response = await self.lamdabot.wait_for('message', check=lambda message: message.author == ctx.author)
            response = response.content.lower()

            if response == 'yes':
                await ctx.send("Alright! Starting new game...")
                await play()
            elif response == 'no':
                await ctx.send("Thanks for playing **RPS**!")
            else:
                await ctx.send("Not a choice, **Yes** / **No**")
                await gameover()

        await play()


def setup(lambdabot):
    lambdabot.add_cog(Games(lambdabot))
