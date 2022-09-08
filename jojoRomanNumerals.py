def toRoman(x):
    if x >= 4000 or x <= 0:
        return -1

    ret = ""

    lows = [1, 4, 5, 9, 10, 40, 50, 90, 100, 400, 500, 900, 1000]
    vals = ["I", "IV", "V", "IX", "X", "XL", "L", "XC", "C", "CD", "D", "CM", "M"]

    while x != 0:
        # binary searching for the value less than or equal to x
        lo = 0
        hi = 12
        while lo <= hi:
            mid = (lo + hi)//2
            if lows[mid] <= x:
                lo = mid + 1
            else:
                hi = mid - 1

        mid = (lo + hi)//2
        ret += vals[mid]
        x -= lows[mid]

    return ret
