# sudoku_simon
# js 20.11.2006
# js 10.4.2007  bubenorbis


from string import digits
from typing import Iterator

from numpy import array, ndarray

from searching.searching2 import SearchProblem, searchByFunction, searchByGenerator


def solveByFunction(p: str) -> list:
    """
    :param p: a Sudoku problem given as string
    :return: a list of all solutions
    """
    return searchByFunction(SudokuProblem(p))


def solveByGenerator(p) -> Iterator:
    """
    :param p: a Sudoku problem given as string
    :return: an iterator yielding all solutions
    """
    return searchByGenerator(SudokuProblem(p))


def _int(c: chr) -> int:
    return int(c) if c in digits else 0


class SudokuProblem(SearchProblem):
    rows = range(9)
    columns = range(9)
    numbers = range(1, 10)
    boxes = [(i, j) for i in range(3) for j in range(3)]
    positions = [(i, j) for i in range(9) for j in range(9)]

    def __init__(self, input):
        super().__init__()

        # candidates[i][j] contains all legal digits at (i, j)
        self.candidates = [[set() for i in self.rows] for j in self.columns]
        self.history = '\n'

        # this constructor accepts
        # a list of 81 characters: '-' or an integer between 1 and 9       OR
        # a string representing 81 integers (separators being blank and newline)
        if type(input) is ndarray:
            self.grid = array(input)
        elif type(input) is str:
            tmp = [_int(c) for c in input.split()]
            self.grid = array(tmp)
        else:
            raise TypeError

        self.grid.shape = 9, 9
        self.reset()
        self.checkInvariants()

    def row(self, i):  # 0 <= i <= 8
        return list(self.grid[i, :])

    def col(self, j):  # 0 <= j <= 8
        return list(self.grid[:, j])

    def box(self, i, j):  # 0 <= i, j <= 2
        bx = self.grid[3 * i: 3 * i + 3, 3 * j: 3 * j + 3]
        return list(bx.ravel())

    def checkInvariants(self):
        for n in self.numbers:
            for i in self.rows:  # check rows
                if self.row(i).count(n) > 1:
                    raise Exception
            for j in self.columns:  # check columns
                if self.col(j).count(n) > 1:
                    raise Exception
            for i, j in self.boxes:  # check boxes
                if self.box(i, j).count(n) > 1:
                    raise Exception

    def done(self):  # done iff no zeros left
        t = array(self.grid)
        return list(t.ravel()).count(0) == 0

    def reset(self):  # reset candidates
        for i, j in self.positions:
            if self.grid[i][j] != 0:
                self.candidates[i][j] = set()
            else:
                self.candidates[i][j] = \
                    set(self.numbers) \
                    - set(self.row(i)) \
                    - set(self.col(j)) \
                    - set(self.box(i // 3, j // 3))

    def nextsteps(self):
        # a step is a tuple (i, j, n): set n at (i, j)
        # nextsteps returns a list of next steps, to be used by __iter__
        # There are three possible outcomes:
        # the returned list may contain zero, one or more steps:
        # zero: dead end detected
        # one:  there is one mandatory step
        # more: there is no single mandatory step;
        #       at least two options must be considered
        #
        # nextsteps does two things:
        # a) For all positions it computes the set of admissible nums
        #    at that position. nextsteps stops at the zero- or one-outcome
        # b) For each number in range(1, 10) and for all rows/columns/boxes
        #    it computes the set of admissible positions of that number
        #    within that row/column/box.
        #    Again, nextsteps stops at the zero- or one-outcome.
        #
        # In the case of a more-outcome, nextstep returns the smallest of
        # all sets of steps detected along the way.

        m = 1000  # m = number of options
        steps = []

        # check fields: returns
        # dead end or
        # lone field, i.e. a field where exactly one number fits or
        # the field having the shortest candidate list

        for i, j in self.positions:
            if self.grid[i][j] != 0:  # consider empty fields only
                continue

            tmp = [(i, j, n) for n in self.candidates[i][j]]

            if len(tmp) == 0:  # dead end
                self.history += '\ndead end at field'
                return tmp
            elif len(tmp) == 1:
                self.history += '\nlone position on ' + str(tmp[0])
                return tmp
            elif len(tmp) < m:  # keep steps
                m, steps = len(tmp), list(tmp)
            else:
                pass

        # check columns, rows and boxes: returns
        # dead end or
        # the only field in a row/col/box where n fits or
        # the number having the shortest candidate list

        for n in self.numbers:  # for each number
            for i in self.rows:  # check rows
                if n in self.row(i):
                    continue

                tmp = [(i, t, n) for t in self.columns if n in self.candidates[i][t]]

                if len(tmp) == 0:  # dead end
                    self.history += '\ndead end at rows'
                    return tmp
                elif len(tmp) == 1:  # safe guess
                    self.history += '\nlone number on row ' + str(tmp[0])
                    return tmp
                elif len(tmp) < m:  # keep steps
                    m, steps = len(tmp), list(tmp)
                else:
                    pass

        for n in self.numbers:  # for each number
            for j in self.columns:  # check columns
                if n in self.col(j):
                    continue

                tmp = [(s, j, n) for s in self.rows if n in self.candidates[s][j]]

                if len(tmp) == 0:  # dead end
                    self.history += '\ndead end at columns'
                    return tmp
                elif len(tmp) == 1:  # safe guess
                    self.history += '\nlone number on col ' + str(tmp[0])
                    return tmp
                elif len(tmp) < m:  # keep steps
                    m, steps = len(tmp), list(tmp)
                else:
                    pass

        for n in self.numbers:  # for each number
            for i, j in self.boxes:  # check boxes
                if n in self.box(i, j):
                    continue

                tmp = [(s, t, n) for s in range(3 * i, 3 * i + 3) \
                       for t in range(3 * j, 3 * j + 3) \
                       if n in self.candidates[s][t]]

                if len(tmp) == 0:  # dead end
                    self.history += '\ndead end at boxes'
                    return tmp
                elif len(tmp) == 1:  # safe guess
                    self.history += '\nlone number on box ' + str(tmp[0])
                    return tmp
                elif len(tmp) < m:  # keep steps
                    m, steps = len(tmp), list(tmp)
                else:
                    pass

        if len(steps) > 1:  # at least two options
            self.history += '\ntrying ' + str(steps)

        return steps

    def __iter__(self):
        return iter(self.nextsteps())

    def getState(self):
        state = SudokuProblem(self.grid)
        state.history = str(self.history)
        return state

    def do(self, step):
        i, j, n = step
        self.grid[i][j] = n  # set n at (i, j)
        self.reset()  # recompute candidates
        # self.checkInvariants()

    def undo(self, step):
        i, j, n = step
        self.grid[i][j] = 0  # unset n at (i, j)

    def __repr__(self):
        s = ""
        for i in self.rows:
            if i % 3 == 0 and i > 0:
                s += "\n"
            for j in self.columns:
                if j % 3 == 0 and j > 0:
                    s += "  "
                c = str(self.grid[i, j])
                if c == '0':
                    c = '-'
                s = s + c + ' '

            s += "\n"
        return s

    def __len__(self):
        return self.history.count('\n')
