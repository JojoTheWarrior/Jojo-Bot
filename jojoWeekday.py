# used to calculate what day of the week it will be

daysOfTheWeek = [
    'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'
]

monthsOfTheYear = [
    'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'
]


def getName(DD, MM, YYYY):
    # calculating the trunk of the name of the day
    lastDigitOfDay = int(str(DD)[-1:])
    if lastDigitOfDay == 1:
        trunk = 'st'
    elif lastDigitOfDay == 2:
        trunk = 'nd'
    elif lastDigitOfDay == 3:
        trunk = 'rd'
    else:
        trunk = 'th'
    return f"The {DD}{trunk} of {monthsOfTheYear[MM - 1]}, {YYYY}"


def getDay(DD, MM, YYYY):
    if YYYY % 4 == 0:
        isLeap = True
    else:
        isLeap = False
    """
    :param DD: Day
    :param MM: Month
    :param YYYY: Year
    :return: Day of the week that this day was on, as a string. Returns false if the date is invalid
    1800 to 1899 = 200 (mod 400) to 299 (mod 400) = Friday
    1900 to 1999 = 300 (mod 400) to 399 (mod 400) = Wednesday
    2000 to 2099 = 0 (mod 400) to 99 (mod 400) = Tuesday
    2100 to 2199 = 100 (mod 400) to 199 (mod 400) = Sunday
    """
    # checking for invalid dates generally
    if DD < 1 or MM < 1 or YYYY < 1 or MM > 12:
        return False
    # checking for invalid dates by the month
    if MM == 1 or 3 or 5 or 7 or 8 or 10 or 12:
        if DD > 31:
            return False
    elif MM != 2:
        if DD > 30:
            return False
    elif MM == 2:
        if isLeap and DD > 29:
            return False
        elif not isLeap and DD > 28:
            return False

    anchor = 0
    # collecting the anchor code
    if 200 <= YYYY % 400 <= 299:
        anchor = 5
    elif 300 <= YYYY % 400 <= 399:
        anchor = 3
    elif 0 <= YYYY % 400 <= 99:
        anchor = 2
    elif 100 <= YYYY % 400 <= 199:
        anchor = 7

    # collecting the doomsday code
    ddc = ((int(str(YYYY)[-2:]) // 12) + (int(str(YYYY)[-2:]) % 12) + ((int(str(YYYY)[-2:]) % 12) // 4) + anchor) % 7

    # dictionary of the closest doomsdays
    closeDay = {}
    if YYYY % 4 == 0:
        # leap year
        closeDay[1] = 4
        closeDay[2] = 29
    else:
        # not leap year
        closeDay[1] = 3
        closeDay[2] = 28

    # even ones
    for i in range(4, 13, 2):
        closeDay[i] = i

    # last ones
    closeDay[5] = 9
    closeDay[7] = 11
    closeDay[9] = 5
    closeDay[11] = 7

    # taking the modulos, subtract the actual date FROM the closeDay value
    if closeDay[MM] == DD:
        # same day
        dayIndex = daysOfTheWeek[ddc]
    elif closeDay[MM] < DD:
        # day is bigger
        dayIndex = (DD - closeDay[MM] + ddc) % 7
    else:
        # closeDay is bigger
        dayIndex = (ddc + (7 - ((closeDay[MM] - DD) % 7))) % 7

    # returns the date as a string
    return daysOfTheWeek[dayIndex]
