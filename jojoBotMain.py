# importing stuff
import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
from jojoSarcastic import jojoSarcastic
import random
import math
import http.client
import ssl
import json
from jojoTicTacToe import TTT
import jojoTicTacToe
from jojoWeekday import getDay
from jojoWeekday import getName
from jojoRomanNumerals import toRoman
from jojoEnglishNumber import toWord
from jojoHelp import listCommands
import re

TOKEN = "[redacted]"
bot = commands.Bot(command_prefix='', intents=discord.Intents.all())
client = discord.Client(intents=discord.Intents.all())

API_KEY = "KMVE9NMZUUQSZMM9YZ6LA8JUM"
HOST = "weather.visualcrossing.com"
URL = "/VisualCrossingWebServices/rest/services/timeline/"


# method that obtains a report for a specified city + country
def get_weather_report(city, country):
    conn = http.client.HTTPSConnection(HOST, context=ssl._create_unverified_context())
    conn.request("GET", f"{URL}{city},{country}?key={API_KEY}")

    res = conn.getresponse()
    if res.status == 200:
        data = res.read().decode("utf-8")
        return json.loads(data)
    else:
        return res.status, res.reason


torontoWeather = get_weather_report("Toronto", "CA")
sunriseTime = torontoWeather['days'][0]['sunrise'].split(":")
sunRHour = sunriseTime[0]
sunRMin = sunriseTime[1]

sunsetTime = torontoWeather['days'][0]['sunset'].split(":")
sunSHour = sunsetTime[0]
sunSMin = sunsetTime[1]

# tmr
torontoWeather2 = get_weather_report("Toronto", "CA")
sunriseTime2 = torontoWeather['days'][1]['sunrise'].split(":")
sunRHour2 = sunriseTime[0]
sunRMin2 = sunriseTime[1]

sunsetTime2 = torontoWeather['days'][0]['sunset'].split(":")
sunSHour2 = sunsetTime[0]
sunSMin2 = sunsetTime[1]

memberIdentifications = {
    "Justin": 969408908273811476,
    "Avery Lee": 490636564909522965,
    "Joshua": 969433849195024394,
    "Nirvan": 776879034842742815,
    "Antonio": 892219565390594108,
    "Brian": 911391692123410432,
    "Luka": 326116423556530187
}

memberIdentificationsList = [
    969408908273811476, 490636564909522965, 969433849195024394, 776879034842742815, 892219565390594108,
    911391692123410432, 569703366909886502, 724786341946195990, 822607717738348584
]

# tic tac toe
currentPlayers = {}
playersGuesses = {}
playersAnswers = {}
guessCounts = {}
playersMaximum = {}
playersMinimum = {}
playersTotalGuess = {}
ticTacToePlayers = {}

# sarcastic typer
chadTalk = []

eightBallAnswers = [
    "Definitely",
    "Maybe?",
    "Do squirrels chew grass?",
    "No chance lol",
    "If you're lucky enough, then yes",
    "Absolutely not",
    "Who do you think you are?",
    "Not in a million years",
    "Yep, of course, it's inevitable",
    "You should probably give up on that",
    "Even a third-grader will say \"yes\""
]

theBiggest = 10
henryWins = 0
beQuietForASec = False


@bot.event
async def on_ready():
    print('Bot connected as %s' % bot.user)


# this actually works btw, the first on_ready function calls the bot's username
# this next function checks for the message's content (I already know how to do that)
# then, after sending the response, it awaits bot.process_commands
# can also do, commands.has_role("whatever role")

async def removeName(x):
    ticTacToePlayers[x].resetBoard(x)
    ticTacToePlayers.pop(x)


@bot.event
async def on_message(message):
    global theBiggest
    global beQuietForASec
    global henryWins

    # fun command for silencing people
    if message.author.id == 665613286636650557:
        if message.content == "jojo silencer mode":
            if not beQuietForASec:
                beQuietForASec = True
                embedVar = discord.Embed(title="You got it, boss", description="Silencer Mode: Enabled",
                                         color=0x230B5C)
                await message.channel.send(embed=embedVar)
                await bot.process_commands(message)
            else:
                beQuietForASec = False
                embedVar = discord.Embed(title="You got it, boss", description="Silencer Mode: Disabled",
                                         color=0x230B5C)
                await message.channel.send(embed=embedVar)
                await bot.process_commands(message)

    # test command
    if beQuietForASec and message.author.id in memberIdentificationsList:
        await message.delete()
        await message.channel.send(f"**{message.author.name}:** {message.content[0:1]}")
        await bot.process_commands(message)

    # we do not want the bot to reply to itself
    if message.author == bot.user:
        return

    if message.content == "jojo sarcastic enable":
        if chadTalk.__contains__(message.author.id):
            embedVar = discord.Embed(title="Error", description="You have already enabled jojo sarcastic!\n\nUse 'j"
                                                                "ojo sarcastic disable to disable it.",
                                     color=0xFF0000)
        else:
            embedVar = discord.Embed(title=f"{message.author.name} Sarcastic Enabled",
                                     description="To disable this, use \"jojo sarcastic disable\".", color=0x00FF00)
            embedVar.add_field(name="Note:", value="You will not be able to use any other jojo commands if jojo "
                                                   "sarcastic is enabled.", inline=False)
            chadTalk.append(message.author.id)
        await message.channel.send(embed=embedVar)
    await bot.process_commands(message)

    if message.content == "jojo sarcastic disable":
        if chadTalk.__contains__(message.author.id):
            embedVar = discord.Embed(title=f"Removed {message.author.name} from Jojo Sarcastic",
                                     description="Use \"jojo sarcastic enable\" to re-enable it.", color=0x00FF00)
            chadTalk.remove(message.author.id)
        else:
            embedVar = discord.Embed(title="Error",
                                     description="You did not enable Jojo Sarcastic!\n\nUse \"jojo sarcastic enable\" "
                                                 "to enable it.", color=0xFF0000)
        await message.channel.send(embed=embedVar)
    await bot.process_commands(message)

    if chadTalk.__contains__(message.author.id) and not message.content == "jojo sarcastic disable" and not \
            message.content == "jojo sarcastic enable":
        await message.delete()
        await message.channel.send(f"**{message.author.name}:** {jojoSarcastic(message.content)}")
        return
    await bot.process_commands(message)

    if currentPlayers.get(message.author.id) and message.content.startswith("jojo guess"):
        userMessage = message.content.split(" ", 2)
        if userMessage[2].isdigit:
            currentGuess = int(2)
            print(currentGuess)
        else:
            await message.channel.send("Enter a number as your next guess.")
        await bot.process_commands(message)

    if message.content.startswith('jojo 8ball'):
        eightBallMessage = message.content.split(" ", 2)
        print(eightBallMessage[2])
        # boolean for adding another question mark
        extraMark = "?"
        if message.content.endswith('?'):
            extraMark = ""
        await message.channel.send(
            "**" + eightBallMessage[2] + extraMark + "**\n\n" + random.choice(eightBallAnswers))
        await bot.process_commands(message)

    # if he's in a game now
    if message.content.startswith("jojo move ") and ticTacToePlayers.__contains__(message.author.id):
        userMessage = message.content.split()
        if len(userMessage) > 3:
            embedVar = discord.Embed(title="Error", description="Wrong format! You must enter a single number."
                                                                "\nYour game was terminated.",
                                     color=0xFF0000)
            await removeName(message.author.id)
        elif not userMessage[2].isdigit():
            # if the message is not a number
            embedVar = discord.Embed(title="Error", description="Wrong format! You must enter a number."
                                                                "\nYour game was terminated.",
                                     color=0xFF0000)
            await removeName(message.author.id)
        elif not ticTacToePlayers[message.author.id].userCanMove(int(userMessage[2])):
            embedVar = discord.Embed(title="Error", description="Invalid move! You cannot go there."
                                                                "\nYour game was terminated.",
                                     color=0xFF0000)
            await removeName(message.author.id)
        else:
            # actually worked
            ticTacToePlayers[message.author.id].userMove(int(userMessage[2]))
            # checks for a draw
            if len(ticTacToePlayers[message.author.id].remainingMoves) == 0:
                embedVar = discord.Embed(title=f"{message.author.name}'s Board",
                                         description=ticTacToePlayers[message.author.id].printBoard(),
                                         color=0xFFFFFF)
                embedVar.add_field(name="Game Over!", value="We tied! GGWP", inline=False)
                await removeName(message.author.id)
                # birthday special
                if message.author.id == 448279180304580608 or 665613286636650557:
                    henryWins += 1
                    embedVar.add_field(name="Henry's Wins:", value=henryWins, inline=False)
                    if henryWins == 10:
                        embedVar.add_field(name="Next:", value='https://screenmessage.com/nmfi', inline=False)
            elif ticTacToePlayers[message.author.id].hasWon():
                # user won
                embedVar = discord.Embed(title=f"{message.author.name}'s Board",
                                         description=ticTacToePlayers[message.author.id].printBoard(),
                                         color=0x00FF00)
                embedVar.add_field(name="Game Over!", value="Congratulations, you won!", inline=False)
                await removeName(message.author.id)
            else:
                ticTacToePlayers[message.author.id].computerMove()
                # user tied
                if len(ticTacToePlayers[message.author.id].remainingMoves) == 0:
                    embedVar = discord.Embed(title=f"{message.author.name}'s Board",
                                             description=ticTacToePlayers[message.author.id].printBoard(),
                                             color=0xFFFFFF)
                    embedVar.add_field(name="Game Over!", value="We tied! GGWP", inline=False)
                    await removeName(message.author.id)
                    if message.author.id == 448279180304580608 or 665613286636650557:
                        henryWins += 1
                        embedVar.add_field(name="Henry's Wins:", value=henryWins, inline=False)
                        if henryWins == 3:
                            embedVar.add_field(name="Next:", value='https://screenmessage.com/nmfi', inline=False)
                elif ticTacToePlayers[message.author.id].hasWon():
                    embedVar = discord.Embed(title=f"{message.author.name}'s Board",
                                             description=ticTacToePlayers[message.author.id].printBoard(),
                                             color=0xFF0000)
                    embedVar.add_field(name="Game Over!", value="You lost! Better luck next time =P", inline=False)
                    await removeName(message.author.id)
                    henryWins = 0
                else:
                    embedVar = discord.Embed(title=f"{message.author.name}'s Board",
                                             description=ticTacToePlayers[message.author.id].printBoard(),
                                             color=0x00FF00)
        await message.channel.send(embed=embedVar)
        await bot.process_commands(message)

    if message.content.startswith('jojo rps'):
        userMessage = message.content.split(" ", 2)
        print(userMessage[2])
        userChoice = userMessage[2]
        if userChoice == "rock":
            print("paper")
            await message.channel.send("paper")
        elif userChoice == "paper":
            print("scissors")
            await message.channel.send("scissors")
        elif userChoice == "scissors":
            print("rock")
            await message.channel.send("rock")
        else:
            print("have you never played rock paper scissors before? :man_facepalming:")
            await message.channel.send("have you never played rock paper scissors before? :man_facepalming:")
        await bot.process_commands(message)

    if message.content.startswith('jojo scale '):
        userMessage = message.content.split(" ", 2)
        embedVar = " "
        if len(userMessage) >= 3:
            embedVar = discord.Embed(title="Jojo's Scale Machine", description="**" + userMessage[
                2] + "**" + "\n\nOn a scale of 1 to 10, I rate that a " + str(random.randint(0, theBiggest)))
        await message.channel.send(embed=embedVar)
        await bot.process_commands(message)

    # command for changing the scale
    if message.content.startswith('jojo scaleMax'):
        userMessage = message.content.split(" ", 2)
        if not userMessage[2].isdigit:
            embedVar = discord.Embed(title="Error", description="Wrong format, maximum must be a number",
                                     color=0xFF0000)
        else:
            theBiggest = int(userMessage[2])
            embedVar = discord.Embed(title="Jojo's Scale Machine Maximum",
                                     description="Successfully changed the max value to " + str(theBiggest))
        await message.channel.send(embed=embedVar)
        await bot.process_commands(message)

    if message.content == ('checkers'):
        embedVar = discord.Embed(title="User Information", description=" ", color=0x00ff10)
        embedVar.add_field(name="Author Name", value=message.author.name, inline=False)
        embedVar.add_field(name="Author ID", value=message.author.id, inline=False)
        embedVar.add_field(name="Author Ping", value=message.author.mention, inline=False)

        authorsID = message.author.id
        embedVar.add_field(name="Information", value="<@" + str(authorsID) + ">", inline=False)
        embedVar.add_field(name="Nickname in Server", value=message.author.nick, inline=False)

        await message.channel.send(embed=embedVar)
        await message.channel.send("<@" + str(message.author.id) + ">")
    await bot.process_commands(message)

    if message.content == "jojo super secret epic command :))":
        await message.channel.send("omg hi omg u have the super secret epic command :)))" + bot.fetch_guild())

    if message.content.startswith("jojo roman"):
        userInput = message.content.split(" ")
        if len(userInput) != 3:  # too many fields
            embedVar = discord.Embed(title="Error", description="Improper format!", color=0xFF0000)
            embedVar.add_field(name="Example:", value="jojo roman 69", inline=False)
            await message.channel.send(embed=embedVar)
        else:
            ret = toRoman(int(userInput[2]))
            if ret == -1:  # too big number, or if <= 0
                embedVar = discord.Embed(title="Error", description="Improper number!", color=0xFF0000)
                embedVar.add_field(name="Did you know that...", value="Although there are many different systems of "
                                                                      "Roman Numerals, a general rule is that you "
                                                                      "cannot represent:\n\t1. Negative numbers,\n\t2. "
                                                                      "Numbers greater than 3999,\n\t3. Zero\n\n**Now you do!**",
                                   inline=False)
                await message.channel.send(embed=embedVar)
            else:
                embedVar = discord.Embed(title=(message.author.name + "'s Roman Numeral"),
                                         description=f"{userInput[2]} "
                                                     f"is {ret} in Roman Numerals.", color=0x00FF00)
                await message.channel.send(embed=embedVar)
        await bot.process_commands(message)

    # code for if you can guess
    if message.content.startswith('jojo guess ') and currentPlayers.get(message.author.id) == True:
        userMessage = message.content.split(" ")

        if len(userMessage) != 3 or not userMessage[2].isdigit():
            # branching for if your format is wrong
            await message.channel.send("Incorrect Format")
        else:
            # now you know that you are in the game
            guess = int(userMessage[2])

            if guess > playersAnswers.get(message.author.id):
                # too high
                currentGuesses = guessCounts.pop(message.author.id)
                guessCounts[message.author.id] = currentGuesses + 1;

                embedVar = discord.Embed(title=message.author.name + "'s Guessing Game",
                                         description="Too high!",
                                         color=0xff0000)

                # if the guess is lower than the previous maximum
                if guess < playersMaximum.get(message.author.id):
                    playersMaximum.pop(message.author.id)
                    playersMaximum[message.author.id] = guess

                embedVar.add_field(name="Guesses:", value="You have " + str(
                    playersGuesses.get(message.author.id) - guessCounts.get(
                        message.author.id)) + " guesses left", inline=False)
                embedVar.add_field(name="Range:", value=str(playersMinimum.get(message.author.id)) + " < n < "
                                                        + str(playersMaximum.get(message.author.id)), inline=False)
                await message.channel.send(embed=embedVar)

            elif guess < playersAnswers.get(message.author.id):
                # too low
                currentGuesses = guessCounts.pop(message.author.id)
                guessCounts[message.author.id] = currentGuesses + 1;

                embedVar = discord.Embed(title=message.author.name + "'s Guessing Game",
                                         description="Too low!",
                                         color=0xff0000)

                # if the guess is higher than the previous minimum
                if guess > playersMinimum.get(message.author.id):
                    playersMinimum.pop(message.author.id)
                    playersMinimum[message.author.id] = guess

                embedVar.add_field(name="Guesses:", value="You have " + str(
                    playersGuesses.get(message.author.id) - guessCounts.get(
                        message.author.id)) + " guesses left", inline=False)
                embedVar.add_field(name="Range:", value=str(playersMinimum.get(message.author.id)) + " < n < "
                                                        + str(playersMaximum.get(message.author.id)), inline=False)
                await message.channel.send(embed=embedVar)
            else:
                # user won
                embedVar = discord.Embed(title=f"{message.author.name}'s Guessing Game", description="You won!",
                                         color=0x00FF00)
                embedVar.add_field(name="Score:", value=playersGuesses.get(message.author.id) -
                                                        guessCounts.get(message.author.id), inline=False)
                if playersTotalGuess[message.author.id] == 130321:
                    embedVar.add_field(name="Henry:", value='https://screenmessage.com/kmqg', inline=False)
                await message.channel.send(embed=embedVar)
                currentPlayers.pop(message.author.id)

            if guessCounts.get(message.author.id) >= playersGuesses.get(message.author.id):
                embedVar = discord.Embed(title=message.author.name + "'s Guessing Game", description="You lost!",
                                         color=0xff0000)
                embedVar.add_field(name="The correct answer was: ",
                                   value=str(playersAnswers.get[message.author.id]),
                                   inline=False)
                await message.channel.send(embed=embedVar)
        await bot.process_commands(message)

    if message.content.startswith('jojo guessing game'):
        userMessage = message.content.split(" ")
        # branching for if the parameters are not right
        if len(userMessage) != 4 or not userMessage[3].isdigit():
            embedVar = discord.Embed(title="Incorrect Format!",
                                     description="Please provide the maximum range you would like.",
                                     color=0xff0000)
            embedVar.add_field(name="Example:", value="gg guessing game 128",
                               inline=False)
            await message.channel.send(embed=embedVar)
        else:
            # assume that the game runs now
            # running the game
            totalGuess = int(userMessage[3])

            # adding the game to the dicts
            currentPlayers[message.author.id] = True
            playersGuesses[message.author.id] = math.ceil(math.log(totalGuess, 2)) + 1
            playersAnswers[message.author.id] = random.randint(0, totalGuess)
            playersMaximum[message.author.id] = totalGuess
            playersTotalGuess[message.author.id] = totalGuess
            playersMinimum[message.author.id] = 0
            guessCounts[message.author.id] = 0

            print(currentPlayers, "\n", playersGuesses, "\n", playersAnswers)

            embedVar = discord.Embed(title=message.author.name + "'s Guessing Game",
                                     description="Your number is between 0 and " + str(totalGuess) + "\nUse \"jojo "
                                                                                                     "guess _\" to make your guesses.",
                                     color=0x00ff00)
            embedVar.add_field(name="Guesses:",
                               value="You have " + str(playersGuesses.get(message.author.id)) + " guesses",
                               inline=False)
            await message.channel.send(embed=embedVar)
        await bot.process_commands(message)

    if message.content == "jojo join":
        if message.author.voice and not bot.voice_clients:
            channel = message.author.voice.channel
            await channel.connect()
        elif not message.author.voice:
            embedVar = discord.Embed(title="Error", description="You need to be in a voice channel first.",
                                     color=0xFF0000)
            await message.channel.send(embed=embedVar)
        else:
            embedVar = discord.Embed(title="Error", description="The bot is already connected to a voice channel.",
                                     color=0xFF0000)
            await message.channel.send(embed=embedVar)
        await bot.process_commands(message)

    if message.content == "jojo leave":
        if not bot.voice_clients:
            # if the bot is not in vc
            embedVar = discord.Embed(title="Error", description="I am not in your voice channel.",
                                     color=0xFF0000)
            await message.channel.send(embed=embedVar)
        elif not message.author.voice.channel:
            # if the author is not in vc
            embedVar = discord.Embed(title="Error", description="You need to be in a voice channel first.",
                                     color=0xFF0000)
            await message.channel.send(embed=embedVar)
        else:
            # if the bot and the user are both in the same vc
            server = message.guild.voice_client
            await server.disconnect()
            embedVar = discord.Embed(title="Left Voice Channel", description="Disconnected from the voice channel.",
                                     color=0x00FF00)
            await message.channel.send(embed=embedVar)
        await bot.process_commands(message)

    if message.content == "jojo weather":
        report = torontoWeather['days'][0]
        temp = report['temp']
        # branching for the color of the message
        if temp > 68:
            texCol = 0xFFA500
        else:
            texCol = 0x0096FF
        embedVar = discord.Embed(title=f"**Report for {report['datetime']}**", description="\n", color=texCol)
        embedVar.add_field(name="**Temperature:**", value=f"Low of {report['tempmin']}F\nHigh of " +
                                                          f"{report['tempmax']}F\n" + f"Currently {report['temp']}F")
        # branching for yes precipitation or no
        if report['precip'] == 0:
            embedVar.add_field(name="**Precipitation:**", value="There is no precipitation today.", inline=False)
        else:
            embedVar.add_field(name="**Precipitation:**", value=f"Precipitation: {report['precip']} mm\n" +
                                                                f"Precipitation Chance: {report['precipprob']}",
                               inline=False)
        embedVar.add_field(name="**Wind:**", value=f"Current Wind Speed: {report['windspeed']} Knots\n" +
                                                   f"Current Wind Direction: " + f"{report['winddir']}",
                           inline=False)
        embedVar.add_field(name="**Sun:**",
                           value=f"Sunrise: {sunRHour}:{sunRMin} AM\nSunset: {sunSHour}:{sunSMin} PM",
                           inline=False)
        embedVar.add_field(name="**Conditions:**", value=f"{report['conditions']}",
                           inline=False)
        await message.channel.send(embed=embedVar)
        await bot.process_commands(message)

    if message.content == "jojo weather tmr":
        report = torontoWeather['days'][1]
        temp = report['temp']
        # branching for the color of the message
        if temp > 68:
            texCol = 0xFFA500
        else:
            texCol = 0x0096FF
        embedVar = discord.Embed(title=f"**Report for {report['datetime']}**", description="\n", color=texCol)
        embedVar.add_field(name="**Temperature:**", value=f"Low of {report['tempmin']}F\nHigh of " +
                                                          f"{report['tempmax']}F\n" + f"Currently {report['temp']}F")
        # branching for yes precipitation or no
        if report['precip'] == 0:
            embedVar.add_field(name="**Precipitation:**", value="There is no precipitation tomorrow.", inline=False)
        else:
            embedVar.add_field(name="**Precipitation:**", value=f"Precipitation: {report['precip']} mm\n" +
                                                                f"Precipitation Chance: {report['precipprob']}",
                               inline=False)
        embedVar.add_field(name="**Wind:**", value=f"Current Wind Speed: {report['windspeed']} Knots\n" +
                                                   f"Current Wind Direction: " + f"{report['winddir']}",
                           inline=False)
        embedVar.add_field(name="**Sun:**",
                           value=f"Sunrise: {sunRHour}:{sunRMin} AM\nSunset: {sunSHour}:{sunSMin} PM",
                           inline=False)
        embedVar.add_field(name="**Conditions:**", value=f"{report['conditions']}",
                           inline=False)
        await message.channel.send(embed=embedVar)
        await bot.process_commands(message)

    # tic-tac-toe section
    if message.content == "jojo tictactoe":
        if ticTacToePlayers.__contains__(message.author.id):
            # if he's already playing
            embedVar = discord.Embed(title="Error", description="You are already in a game!", color=0xFF0000)
            await message.channel.send(embed=embedVar)
        else:
            # not yet playing, he gets added to the game
            ticTacToePlayers[message.author.id] = TTT(userId=message.author.id)
            embedVar = discord.Embed(title=f"Tic-Tac-Toe", description="Welcome to Tic-Tac-Toe!",
                                     color=0x00FF00)
            embedVar.add_field(name="Rules:", value="• The computer uses \"X\"\n• You, the player, will use \"@\"\n"
                                                    "• The computer will go first")
            embedVar.add_field(name="\tHow to Play:",
                               value="\t• Type \"jojo move _\" with any available space to move there"
                                     "\n\t• Invalid moves will terminate the game\n")
            embedVar.add_field(name="Good luck!", value="Note: Remember to use \"jojo move\" before your command",
                               inline=False)
            await message.channel.send(embed=embedVar)
            # prints the board
            if random.randint(0, 100) <= 50:
                ticTacToePlayers[message.author.id].computerMove()
                embedVar = discord.Embed(title=f"{message.author.name}'s Board",
                                         description=ticTacToePlayers[message.author.id].printBoard(),
                                         color=0x00FF00)
                embedVar.add_field(name="Moves", value="I'm going first!", inline=False)
            else:
                embedVar = discord.Embed(title=f"{message.author.name}'s Board",
                                         description=ticTacToePlayers[message.author.id].printBoard(),
                                         color=0x00FF00)
                embedVar.add_field(name="Moves", value="You're going first!", inline=False)
            # available moves
            await message.channel.send(embed=embedVar)
        await bot.process_commands(message)

    if message.content.startswith("jojo dotw"):
        datePattern = '\d\d/\d\d/\d\d\d\d$'
        userMessage = message.content.split(" ")
        if len(userMessage) != 3 or not bool(re.match(datePattern, userMessage[2])):
            embedVar = discord.Embed(title="Error", description="Wrong format! Dates should be provided as DD/MM/YYYY."
                                                                "\nMake sure to include blank 0s, too.", color=0xFF0000)
            embedVar.add_field(name="Example", value="jojo dotw 08/28/2007", inline=False)
        elif getDay(int(userMessage[2][:2]), int(userMessage[2][3:5]), int(userMessage[2][6:])) == False:
            embedVar = discord.Embed(title="Error", description="That day is out of range!", color=0xFF0000)
        else:
            # declaring variables
            DD = int(userMessage[2][:2])
            MM = int(userMessage[2][3:5])
            YYYY = int(userMessage[2][6:])

            # actually works
            embedVar = discord.Embed(title=f"{message.author.name}'s Day-of-the-Week",
                                     description=f"{getName(DD, MM, YYYY)} is on a {getDay(DD, MM, YYYY)}",
                                     color=0x00FF00)
        await message.channel.send(embed=embedVar)
    await bot.process_commands(message)

    if message.content.startswith("jojo english number"):
        usm = message.content.split(" ")
        if len(usm) <= 3 or len(usm) >= 5:
            embedVar = discord.Embed(title="Error!", description="Incorrect format. You must include a positive integer "
                                                                 "no longer than 66 digits", color=0xFF0000)
            embedVar.add_field(name="Example:", value="jojo english number 828", inline=False)
        else:
            givenNumber = str(usm[3])
            if len(givenNumber) > 66 or not givenNumber.isdigit():
                embedVar = discord.Embed(title="Error!",
                                         description="Incorrect format. You must include a positive integer "
                                                     "no longer than 66 digits.",
                                         color=0xFF0000)
            else:
                embedVar = discord.Embed(title=f"{message.author.name}'s Number to English", description=
                f"{givenNumber} written in English is:\n{toWord(givenNumber)}.", color=0x00FF00)
        await message.channel.send(embed=embedVar)
    await bot.process_commands(message)

    if message.content.startswith("jojo help"):
        userMessage = message.content.split(" ")
        if len(userMessage) == 2:
            await message.channel.send(embed=listCommands(""))
        else:
            await message.channel.send(embed=listCommands(message.content[10:]))
    await bot.process_commands(message)


@bot.event
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        embedVar = discord.Embed(title="Error", description="You need to be in a voice channel first.",
                                 color=0xFF0000)
        await ctx.send(embed=embedVar)


async def leave(ctx):
    if ctx.voice_client:
        vc = ctx.message.guild.voice_client
        await vc.disconnect()


bot.run(TOKEN)
