## conjoin as alternative to search
## js 10.8.02
## bubenorbis

from warmingup.types import Callable, List, Sequence


############################################
##   three implementations of conjoin     ##
############################################

def conjoin(*gs: Callable) -> Iterator:
    """
    :param gs: list of Callables() -> Iterable
    :return: their cartesian product as iterator
    """
    values = [None] * len(gs)

    def loop(i):
        if i >= len(gs):
            yield list(values)
        else:
            for values[i] in gs[i]():
                yield from loop(i + 1)

    yield from loop(0)


def conjoin1(*gs: Callable) -> Sequence:
    """
    :param gs: list of Callables() -> Iterable
    :return: their cartesian product as list
    """
    values = [None] * len(gs)
    result = []

    def loop(i):
        if i >= len(gs):
            result.append(list(values))
        else:
            for values[i] in gs[i]():
                loop(i + 1)

    loop(0)
    return result


def conjoin2(*gs: Iterator) -> Sequence:
    """
    :param gs: list of Iterators
    :return: their cartesian product as list
    """
    values = [None] * len(gs)
    result = []

    def loop(i):
        if i >= len(gs):
            result.append(list(values))
        else:
            for values[i] in gs[i]:
                loop(i + 1)

    loop(0)
    return result


############################################
##    applying conjoin to roman nums   ##
############################################


digits0 = ('', 'M', 'MM', 'MMM', 'MMMM')
digits1 = ('', 'C', 'CC', 'CCC', 'CD', 'D', 'DC', 'DCC', 'DCCC', 'CM')
digits2 = ('', 'X', 'XX', 'XXX', 'XL', 'L', 'LX', 'LXX', 'LXXX', 'XC')
digits3 = ('', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX')

d0 = lambda: digits0
d1 = lambda: digits1
d2 = lambda: digits2
d3 = lambda: digits3


def romans1() -> Iterator[str]:
    """
    :return: romans nums from 1 to 4999
    """
    result = [''] * 4
    for result[0] in digits0:
        for result[1] in digits1:
            for result[2] in digits2:
                for result[3] in digits3:
                    yield ''.join(result)


def romans() -> Iterator[str]:
    """
    :return: romans nums from 1 to 4999
    """
    result = conjoin(d0, d1, d2, d3)
    return (''.join(t) for t in result)


############################################
##    applying conjoin to permutations    ##
############################################

def permutations(xs: Collection) -> Iterator[Collection]:
    """
    :param xs: a collection
    :return: iterator of all permutations of xs
    """
    steps = []
    visited = len(xs) * [None]

    for i in range(len(xs)):
        def step(i: int = i) -> Iterator:
            """
            :param i: level of step
            :return: all objects not previously visited
            """
            for x in xs:
                if x not in visited[:i]:
                    visited[i] = x
                    yield x

        steps.append(step)

    yield from conjoin(*steps)


############################################
## applying conjoin to the queens problem ##
############################################

def free_fields(occupied_fields: Sequence[int], n: int = 8) -> Set[int]:
    """
    :param occupied_fields: occupied_places[i] = field of queen on row i
    :param n: size of board
    :return: set of save fields in line k = len(state)
    Example: occupied_fields = [3, 1] means:
    In row 0 there is a queen on column 3
    In row 1 there is a queen on column 1
    This would return (4, 6, 7) on an 8x8 board
    """
    result = set(range(n))
    k = len(occupied_fields)
    for i in range(k):
        result.discard(occupied_fields[i] - k + i)
        result.discard(occupied_fields[i])
        result.discard(occupied_fields[i] + k - i)
    return result


def queens(n: int) -> Iterator[List[int]]:
    """
    :param n: size of board, n >= 0
    :return: Iterator over all solutions of the queens problem
    The for-loop produces an array of generators, rows
    occupied_fields is global for all of them.
    rows[i]() yields all free fields in row i depending on
    occupied fields in rows 0 to i-1

    """
    rows = []
    occupied_fields = n * [-1]

    for i in range(n):
        def row(i: int = i) -> Iterator:
            """
            :param i: row to be iterated on
            :return: list of free fields on row i
            """
            for x in free_fields(occupied_fields[:i], n):
                occupied_fields[i] = x
                yield x

        rows.append(row)

    yield from conjoin(*rows)
