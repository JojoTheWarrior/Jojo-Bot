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

helpCommandsDescription = { # matches title to short description
    "jojo 8ball":"Ask the Jojo 8Ball a question.",
    "jojo dotw":"Outputs which day of the week a specific day in history (or in the future!) lands on.",
    "jojo english number":"Converts an Arabic integer to English words.",
    "jojo guessing game":"Play a number guessing game where you must optimize your strategy to win.",
    "jojo help":"You just used it.",
    "jojo join":"Joins the Voice Channel that you are currently in. Does not do anything else as of right now.",
    "jojo roman":"Converts an Arabic integer to its Roman numeral counterpart.",
    "jojo rps":"Play a (slightly rigged) game of Rock, Paper, Scissors.",
    "jojo sarcastic":"Converts all text to sarcasm.",
    "jojo scale":"Measures a prompt/question on a scale.",
    "jojo silencer mode":"Silences all selected users (requires Admin).",
    "jojo tictactoe":"Play a game of Tic-Tac-Toe against the Jojo Bot. The starting party is randomized. \n\n(P.S. You can't win)",
    "jojo weather":"Shows a weather report of Toronto, ON (currently working on other regions)."
}

helpCommandsParameters = {
    "jojo 8ball":"**Question:** The question which you would like an answer to.",
    "jojo dotw":"**Date:** One date, represented in DD/MM/YYYY format (fill blank 0s, and do not exceed 9999 or use any invalid dates",
    "jojo english number":"**Number:** The number which you would like to be translated into English words.",
    "jojo guessing game":"**Maximum:** The highest possible value that the correct answer could be. (Note: You will have ⌈log x base 2⌉ + 1 guesses)",
    "jojo help":"Does not accept any parameters.",
    "jojo join":"Does not accept any parameters, but you must be in a Voice Channel upon sending the command. Use jojo leave to leave VC.",
    "jojo roman":"**Number:** The number which you would like to be translated into Roman numerals. Do not exceed 3999.",
    "jojo rps":"**Move:** Your move (one of 'rock', 'paper', or 'scissors). Also includes a secret move ツ.",
    "jojo sarcastic":"**Switch:** 'enabled' or 'disabled. Note: You will not be able to use other jojo commands while 'jojo sarcastic' is enabled.",
    "jojo scale":"**Question:** The prompt which you would like to be rated. Use 'jojo scaleMax' to set the maximum scale value.",
    "jojo silencer mode":"Does not accept any parameters, just toggles between enabled and disabled.",
    "jojo tictactoe":"Does not accept any parameters. Use 'jojo move' after starting a game to place your valid moves.",
    "jojo weather":"Either do not leave any parameters, or use 'jojo weather tmr', which returns the report of the following day."
}

def listCommands(opt = ""): # returns embedVar
    if opt == "": # just outputs all commands
        embedVar = discord.Embed(title="List of Commands", description="To learn more about a specific command,"
                                        " put it after 'jojo help'.\nE.g.: jojo help jojo weather", color=0x00FF00)
        for key in helpCommandsDescription:
            embedVar.add_field(name=key, value=helpCommandsDescription[key], inline=False)
        return embedVar
    else:
        if opt in helpCommandsDescription:
            embedVar = discord.Embed(title=opt, description=helpCommandsDescription[opt], color=0x00FF00)
            embedVar.add_field(name="Parameters", value=helpCommandsParameters[opt], inline=False)
            return embedVar
        else:
            embedVar = discord.Embed(title="Error", description="That is not a valid command. "
                    "Did you make sure to put 'jojo' in front of it?", color=0xFF0000)
            embedVar.add_field(name="Example", value="jojo help jojo weather", inline=False)
            return embedVar