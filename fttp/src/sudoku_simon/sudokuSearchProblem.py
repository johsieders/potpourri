# s.siedersleben
# fasttrack to professional programming
# lesson ??: programming the sudoku_simon game
# 27.1.2021, 28.1.2021
#

from abc import ABC
from string import digits

import numpy as np

from sudoku_simon.searchProblem import SearchProblem


def _int(c: chr) -> int:
    return int(c) if c in digits else 0


class SudokuSearchProblem(SearchProblem, ABC):
    def __init__(self, sudoku_input):
        super().__init__()

        if type(sudoku_input) is np.ndarray:
            self.grid = np.array(sudoku_input)
        elif type(sudoku_input) is str:
            sudoku_input = sudoku_input.split()
            tmp = []
            for c in sudoku_input:
                tmp.append(_int(c))
            self.grid = np.array(tmp).reshape(9, 9)
        else:
            raise TypeError

    @property
    def __repr__(self):
        s = ""
        for i in range(9):
            if i % 3 == 0 and i > 0:
                s += "\n"
                for j in range(9):
                    if j % 3 == 0 and j > 0:
                        s += "  "
                    c = str(self.grid[i, j])
                    if c == '0':
                        c = '-'
                    s = s + c + ' '

                s += "\n"
        return s

    def __str__(self):
        s = ""
        for i in range(9):
            if i % 3 == 0 and i > 0:
                s += "\n"
            for j in range(9):
                if j % 3 == 0 and j > 0:
                    s += "  "
                c = str(self.grid[i, j])
                if c == '0':
                    c = '-'
                s = s + c + ' '

            s += "\n"
        return s

    def done(self):
        t = np.array(self.grid)
        return list(t.ravel()).count(0) == 0

    def get_state(self):
        sudoku_state = SudokuSearchProblem(self.grid)
        return [sudoku_state]

    def undo_step(self, step):
        i, j, value = step
        self.grid[i, j] = 0

    def check_row(self, i, j):
        row = self.grid[i, :]
        row_without_zeros = row[np.nonzero(row)]
        if len(np.unique(row_without_zeros)) != len(row_without_zeros):
            self.grid[i, j] = 0
            return False
        return True

    def check_column(self, i, j):
        column = self.grid[:, j]
        column_without_zeros = column[np.nonzero(column)]
        if len(np.unique(column_without_zeros)) != len(column_without_zeros):
            self.grid[i, j] = 0
            return False
        return True

    def check_box(self, i, j):
        i_start, i_end = (i // 3) * 3, (i // 3) * 3 + 3
        j_start, j_end = (j // 3) * 3, (j // 3) * 3 + 3
        block = self.grid[i_start: i_end, j_start: j_end]
        block_without_zeros = block[np.nonzero(block)]

        # check block
        if len(block_without_zeros) != len(np.unique(block_without_zeros)):
            self.grid[i, j] = 0
            return False
        return True

    def check_step(self, i, j, value):
        """
        :param i:
        :param j:
        :param value:
        :return: False in case the input at grid i, j does not satisfy the common Sudoku conditions
        """
        if int(value) not in range(0, 10):
            raise ValueError

        self.grid[i, j] = value

        if not self.check_row(i, j):
            return False

        if not self.check_column(i, j):
            return False

        if not self.check_box(i, j):
            return False
        self.grid[i, j] = 0
        return True

    def do_step(self, step):
        """
        :param step: a tuple (i, j, value)
        """
        i, j, value = step
        self.grid[i, j] = value

    def options(self):
        """
        :return: a generator pointing to the next step i.e. the tuple (i, j, value)
        """
        for i in range(9):
            for j in range(9):
                if self.grid[i, j] == 0:
                    for value in range(1, 10):
                        if self.check_step(i, j, value):
                            yield i, j, value
                    return  # this prevents an endless loop

    def __iter__(self):
        return self.options()


if __name__ == '__main__':
    stern23bonsai = """
    - - 9   5 - -   8 1 7
    - 3 -   - 8 -   6 - 9
    8 - -   - - -   2 3 4

    6 - -   3 1 5   - - -
    - 9 -   8 - 2   - 6 -
    - - -   7 6 9   - - 2

    3 8 1   - - -   - - 5
    9 - 5   - 2 -   - 8 -
    4 6 2   - - 8   9 - -
    """
    problem = SudokuSearchProblem(stern23bonsai)
    print(problem)
    state = problem.get_state()
