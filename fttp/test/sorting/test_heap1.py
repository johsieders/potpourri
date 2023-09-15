import unittest
from random import seed, randrange

from sorting.sorting1 import heap_sort
from sorting.sorting2 import isSorted

seed(33)


class Test_Myheap(unittest.TestCase):
    def test_Myheap(self):
        n = 10
        rand = [randrange(1000) for _ in range(n)]
        test_lists = [rand, range(n), [], [1], [2, 3, 1, 1], [4, 3, 2, 1]]

        for test_list in test_lists:
            xs = heap_sort(test_list)
            self.assertTrue(isSorted(xs))


if __name__ == '__main__':
    unittest.main()
