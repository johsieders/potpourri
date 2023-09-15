# s.siedersleben
# fasttrack to professional programming
# random question found in the internet
# 15.12.2020

def rec_character(s):
    if len(s) <= 1:
        return None
    else:
        characters = []
        for c in s:
            if c in characters:
                return c
            else:
                characters.append(c)


def numWays(data):
    if len(data) <= 1:
        return 0

    if int(data[0]) == 1 or int(data[0]) == 2 and int(data[1]) <= 6:
        return 2 + numWays(data[1::])
    else:
        return 1 + numWays(data[1::])


if __name__ == '__main__':
    print(rec_character(""))
    print(rec_character("ABCB"))
    print(numWays("12"))
    print(numWays("29"))
