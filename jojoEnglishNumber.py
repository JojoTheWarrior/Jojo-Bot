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

diggity = {
    9:"Nine",
    8:"Eigh",
    7:"Seven",
    6:"Six",
    5:"Five",
    4:"Four",
    3:"Three",
    2:"Two",
    1:"One",
    0:""
}

diggity8 = {
    9:"Nine",
    8:"Eight",
    7:"Seven",
    6:"Six",
    5:"Five",
    4:"Four",
    3:"Three",
    2:"Two",
    1:"One"
}

diggity[20] = "Twenty"
diggity[30] = "Thirty"
diggity[40] = "Forty"
diggity[50] = "Fifty"

for j in range(6, 10):
    diggity[j * 10] = diggity[j] + "ty"

for j in range(1, 10):
    for i in range(6, 10):
        diggity[10 * i + j] = diggity[i] + "ty" + diggity8[j]
    diggity[20 + j] = "Twenty" + diggity8[j]
    diggity[30 + j] = "Thirty" + diggity8[j]
    diggity[40 + j] = "Forty" + diggity8[j]
    diggity[50 + j] = "Fifty" + diggity8[j]

diggity[10] = "Ten"
diggity[11] = "Eleven"
diggity[12] = "Twelve"
diggity[13] = "Thirteen"
diggity[14] = "Fourteen"
diggity[15] = "Fifteen"

for i in range(6, 10):
    diggity[10 + i] = diggity[i] + "teen"

diggity[8] = "Eight"

groupings = [
    "", "Thousand", "Million", "Billion", "Trillion", "Quadrillion", "Quintillion", "Quintillion",
    "Sextillion", "Septillion", "Octillion", "Nonillion", "Decillion", "Undecillion", "Duodecillion", "Tredecillion",
    "Quattuordecillion", "Quindecillion", "Sexdecillion", "Septendecillion", "Octodecillion",
    "Novemdecillion", "Vigintillion"
]


def threeTwoWord(x):
    if len(x) <= 2:
        return diggity[int(x)]
    # x is 3 digits
    ret = ""
    if not x[0] == "0":
        ret += diggity[int(x[0])] + "Hundred"
    if not int(x[0:]) == 0:
        ret += diggity[int(x[1:])]
    return ret


def toWord(x):
    if x == "0":
        return "Zero"
    if len(x) == 2 or len(x) == 1:
        ret = diggity[int(x)]

        jojo = ""

        for i in ret:
            if i.isupper():
                jojo += " "
            jojo += i

        return jojo

    x = str(x)
    ret = ""
    sz = len(x) - 3
    threeDigList = []
    ptr = 0

    while sz >= 0:
        tl = ""
        tl += x[sz] + x[sz + 1] + x[sz + 2]
        sz -= 3
        if tl != "000":
            ret = threeTwoWord(tl) + groupings[ptr] + ret
        ptr += 1

    if sz == -1:
        ret = diggity[int(x[0:2])] + groupings[ptr] + ret
    elif sz == -2:
        ret = diggity[int(x[0])] + groupings[ptr] + ret

    jojo = ""

    for i in ret:
        if i.isupper():
            jojo += " "
        jojo += i

    return jojo
