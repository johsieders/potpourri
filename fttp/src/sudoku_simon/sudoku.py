# s.siedersleben
# fasttrack to professional programming
# lesson ??: programming the sudoku_simon game
# 12.1.2021


import numpy as np


class Sudoku(object):
    def __init__(self):
        # self.grid = np.zeros([9, 9])
        self.grid = np.array([[8, 0, 0, 0, 3, 0, 0, 2, 6],
                              [1, 5, 0, 4, 0, 0, 8, 0, 0],
                              [0, 0, 0, 0, 0, 8, 9, 0, 4],
                              [9, 0, 0, 0, 4, 0, 2, 0, 5],
                              [5, 0, 8, 0, 0, 6, 0, 0, 1],
                              [6, 0, 0, 0, 0, 0, 7, 9, 0],
                              [0, 0, 0, 9, 1, 5, 0, 0, 0],
                              [2, 0, 6, 3, 0, 0, 0, 8, 9],
                              [7, 0, 0, 0, 0, 0, 0, 1, 0]])

        # self.grid = np.array([[8, 0, 0, 0, 0, 0, 0, 2, 6],
        #                       [1, 5, 0, 4, 0, 0, 8, 0, 0],
        #                       [0, 0, 0, 0, 0, 8, 9, 0, 4],
        #                       [9, 0, 0, 0, 4, 0, 2, 0, 5],
        #                       [5, 0, 8, 0, 0, 6, 0, 0, 1],
        #                       [6, 0, 0, 0, 0, 0, 7, 9, 0],
        #                       [0, 0, 0, 9, 1, 5, 0, 0, 0],
        #                       [2, 0, 6, 3, 0, 0, 0, 8, 9],
        #                       [7, 0, 0, 0, 0, 0, 0, 1, 0]])

    def __repr__(self):
        pass

    def __str__(self):
        return str(self.grid)

    def done(self):
        t = np.array(self.grid)
        return list(t.ravel()).count(0) == 0

    def getState(self):
        return str(self.grid)

    def undo_step(self, i, j):
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

    def do_step(self, i, j, value):
        """
        :param i: index of row
        :param j: index of column
        :param value: input-value
        """
        self.grid[i, j] = value

    def solve(self):
        """
        :return: hopefully a solved sudoku_simon game
        """
        for i in range(9):
            for j in range(9):
                if self.grid[i, j] == 0:
                    for value in range(1, 10):
                        if self.check_step(i, j, value):
                            self.do_step(i, j, value)
                            self.solve()
                            # restore state
                            self.undo_step(i, j)
                    return
        print(self)


if __name__ == '__main__':
    game = Sudoku()
    print(game)
    game.solve()
    # print(game)
