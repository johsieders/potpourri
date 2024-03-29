## checkInvariants Sudoku
## js 12.11.2006

import unittest
from time import time

from searching.sudoku import *

voidsudoku = """
- - -   - - -   - - -
- - -   - - -   - - -
- - -   - - -   - - -

- - -   - - -   - - -
- - -   - - -   - - -
- - -   - - -   - - -

- - -   - - -   - - -
- - -   - - -   - - -
- - -   - - -   - - -
"""

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

stern23samurai = """
- - 5   3 - 2   9 - -
- 1 3   - 8 -   6 5 -
7 - -   - - -   - - 3

6 - -   1 - 8   - - 9
- 8 -   - 7 -   - 3 -
5 - -   4 - 6   - - 2

4 - -   - - -   - - 1
- 2 7   - 5 -   4 6 -
- - 9   8 - 7   3 - -
"""

stern23sumo = """
9 - -   - 8 -   - - 5
- - -   1 - 5   - - -
- - 4   - - -   3 - -

- 3 -   5 7 1   - 8 -
5 - -   2 - 4   - - 7
- 7 -   8 6 9   - 5 -

- - 8   - - -   1 - -
- - -   3 - 7   - - -
2 - -   - 1 -   - - 9
"""

stern23kamikaze = """
- 9 -   - - -   - 7 -
5 - -   - - -   - - 3
- - 8   1 - 2   4 - -

7 - -   - 4 -   - - 2
- 1 -   7 - 5   - 4 -
8 - -   - 6 -   - - 1

- - 2   6 - 8   5 - -
4 - -   - - -   - - 9
- 6 -   - - -   - 3 -
"""

sz0704121 = """
- - -   3 9 -   - - -
- - -   5 7 -   - 4 -
- - -   2 8 1   - 7 5

6 7 1   - - -   4 - 8
- - -   7 1 2   - 3 -
9 - -   - 6 -   - - -

- 9 -   - 2 -   - - -
3 - 4   - 5 -   - 8 1
5 - -   - - 3   - - 6
"""

sz0704122 = """
- - -   5 - -   - - -
9 - 2   1 - -   - 6 -
- 5 -   - 7 2   - 8 -

- 8 -   - - -   9 2 -
- - -   - - -   5 - 3
- - -   7 - 6   - 1 -

7 - -   3 - 1   8 5 -
1 - -   - 2 -   - - -
3 - -   - - -   2 - -
"""

sz070407 = """
2 7 4   1 8 6   5 3 9
5 3 6   2 9 4   1 8 7
1 8 9   3 7 5   2 4 6

9 4 1   8 3 2   6 7 5
8 6 3   5 1 7   4 9 2
7 2 5   6 4 9   8 1 3

6 1 8   9 2 3   7 5 4
3 5 7   4 6 1   9 2 8
4 9 2   7 5 8   3 6 1
"""

t2 = """
2 7 4   1 8 6   5 3 9
5 3 6   2 9 4   1 8 7
1 8 9   3 7 5   2 4 6

9 4 1   8 3 2   6 7 5
8 6 3   5 1 7   4 9 2
7 2 5   6 4 9   8 1 3

6 1 8   9 2 3   - - -
3 5 7   4 6 1   - - -
4 9 2   7 5 8   - - -
"""

sz0704072 = """
5 - -   7 3 -   - - -
- - 3   5 - 2   - - -
- - 4   - - -   1 - -

- - -   - - 8   - - -
- - -   - 1 -   - - 2
- 8 5   3 - -   - - -

- - -   - - -   - - 5
- - 8   4 - 5   - 3 -
- - 7   8 2 6   - - -
"""

sz070217 = """
- - 1   - 7 -   3 5 6
- 5 -   - 6 -   - 1 -
- 6 -   1 - 5   - 9 -

6 1 8   5 - -   2 7 9
5 3 2   - - -   8 6 4
4 - -   6 8 2   1 3 5

- - 5   - - 9   6 - -
- 8 6   - 5 -   9 - -
- 4 -   - - 6   5 - 1
"""

gentle = """
- 1 -   4 2 -   - - 5
- - 2   - 7 1   - 3 9
- - -   - - -   - 4 -

2 - 7   1 - -   - - 6
- - -   - 4 -   - - -
6 - -   - - 7   4 - 3

- 7 -   - - -   - - -
1 2 -   7 3 -   5 - -
3 - -   - 8 2   - 7 -
"""
gentle1 = """
- 1 -   4 2 -   - - 5
- - 2   - 7 1   - 3 9
- - -   - - -   - 4 -

2 - 7   1 - -   - - 6
- - -   - 4 -   - - -
6 - -   - - 7   4 - 3

- 7 -   - - -   - - -
1 2 -   7 3 -   5 - -
3 - -   - 8 2   - - -
"""
moderate = """
- - 6   2 - 1   - - -
8 - -   - - -   - 7 1
- - 1   7 - -   - 3 2

- - 7   - 3 -   - 4 -
- 5 -   - - -   - 8 -
- 8 -   - 4 -   7 - -

4 6 -   - - 5   8 - -
1 7 -   - - -   - - 4
- - -   4 - 6   5 - -
"""

tough = """
- - 1   9 - -   - - 8
6 - -   - 8 5   - 3 -
- - 7   - 6 -   1 - -

- 3 4   - 9 -   - - -
- - -   5 - 4   - - -
- - -   - 1 -   4 2 -

- - 5   - 7 -   9 - -
- 1 -   8 4 -   - - 7
7 - -   - - 9   2 - -
"""

diabolical = """
- 9 -   7 - -   8 6 -
- 3 1   - - 5   - 2 -
8 - 6   - - -   - - -

- - 7   - 5 -   - - 6
- - -   3 - 7   - - -
5 - -   - 1 -   7 - -

- - -   - - -   1 - 9
- 2 -   6 - -   3 5 -
- 5 4   - - 8   - 7 -
"""

testcases1 = [stern23bonsai, stern23samurai, stern23sumo, stern23kamikaze,
              sz0704121, sz0704122, sz070407, sz0704072, sz070217,
              gentle, gentle1, moderate, tough, diabolical]

testcases = [stern23bonsai]


class TestSudoku(unittest.TestCase):
    def test(self):
        timer = []
        print("\nstart sudoku_simon")
        for tc in testcases1:
            timer.append(time())
            searchByFunction(SudokuProblem(tc))
        print("stop sudoku_simon")
        print(timer)
        print(timer)
