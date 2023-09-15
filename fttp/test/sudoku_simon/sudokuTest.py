import unittest

from sudoku_simon.searchProblem import search_by_function
from sudoku_simon.sudokuSearchProblem import SudokuSearchProblem

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


class SudokuTestCase(unittest.TestCase):

    def test_sudokuSearchProblem(self):
        problem = SudokuSearchProblem(stern23bonsai)
        print(problem)
        result = search_by_function(problem)
        for r in result:
            print(r)


if __name__ == '__main__':
    unittest.main()
