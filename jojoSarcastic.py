import random

lower = [
    'a',
    'b',
    'c',
    'd',
    'e',
    'f',
    'g',
    'h',
    'i',
    'j',
    'k',
    'l',
    'm',
    'n',
    'o',
    'p',
    'q',
    'r',
    's',
    't',
    'u',
    'v',
    'w',
    'x',
    'y',
    'z'
]


def jojoSarcastic(inputtedString):
    change = inputtedString.lower()
    output = ""
    count = 0
    for letter in change:
        if lower.__contains__(letter):
            if count % 2 == 0:
                output += letter
            else:
                output += letter.upper()
            count += 1
        else:
            output += letter
    return output
