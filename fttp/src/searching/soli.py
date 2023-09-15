# Tiefe-Zuerst-Suche fuer Solitaer
# js 2.1.2003

from functools import reduce
from operator import add

grid = ((0, 2), (0, 3), (0, 4),
        (1, 2), (1, 3), (1, 4),
        (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
        (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6),
        (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6),
        (5, 2), (5, 3), (5, 4),
        (6, 2), (6, 3), (6, 4))


def initBoard():
    on = {}
    for s in grid:
        on[s] = 1
    on[(3, 3)] = 0
    return on


def printBoard(on):
    for x in range(7):
        print([on.get((x, y), 9) for y in range(7)])


def count(on):
    """ liefert die Anzahl der besetzten Felder """
    return reduce(add, [on[s] for s in grid])


def up(s):
    return s, (s[0] - 1, s[1]), (s[0] - 2, s[1])


def down(s):
    return s, (s[0] + 1, s[1]), (s[0] + 2, s[1])


def left(s):
    return s, (s[0], s[1] - 1), (s[0], s[1] - 2)


def right(s):
    return s, (s[0], s[1] + 1), (s[0], s[1] + 2)


def __mayMove(s, dir, on):
    s0, s1, s2 = dir(s)
    return s2 in grid and \
        on[s0] and on[s1] and not on[s2]


def mayMove(s, on):
    return __mayMove(s, up, on) or \
        __mayMove(s, down, on) or \
        __mayMove(s, left, on) or \
        __mayMove(s, right, on)


def getTargets(s, on):
    return [dir(s)[2] \
            for dir in (up, down, right, left) \
            if __mayMove(s, dir, on)]


def move(s, dir, on):
    s0, s1, s2 = dir(s)
    if s2 in grid and \
            on[s0] and on[s1] and not on[s2]:
        on[s0], on[s1], on[s2] = 0, 0, 1
        return 1
    else:
        return 0


def moveTo(s, t, on):
    if t == (s[0] - 2, s[1]):
        move(s, up, on)
    elif t == (s[0] + 2, s[1]):
        move(s, down, on)
    elif t == (s[0], s[1] - 2):
        move(s, left, on)
    elif t == (s[0], s[1] + 2):
        move(s, right, on)
    elif s == t:
        return
    else:
        assert 0


def undo(s, dir, on):
    s0, s1, s2 = dir(s)
    on[s0], on[s1], on[s2] = 1, 1, 0


cnt = 0
maxmoves = 0


def search(on, moves=(), result=()):
    global cnt, maxmoves
    if cnt % 100000 == 0:
        print("still alive ", cnt, maxmoves, len(result))
    cnt += 1

    if len(moves) > 29:
        result.append(moves)
        print(len(moves), moves)

    if len(result) > 1:
        return result

    for s in grid:
        for dir in (up, left, down, right):
            if move(s, dir, on):
                moves.append((s, dir))
                maxmoves = max(maxmoves, len(moves))
                search(on, moves, result)
                moves.pop()
                undo(s, dir, on)
    return result


if __name__ == "__main__":
    on = initBoard()
    search(on)
