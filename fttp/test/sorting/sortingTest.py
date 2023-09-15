# testing sorting
# 25.12.2020


import sys
import unittest
from random import seed, randrange
from time import perf_counter

from sorting.sorting1 import heap_sort
from sorting.sorting2 import *


def wrap(sort_on_place):
    """
    :param sort_on_place: a sort function sorting on place
    :return: a sort function returning a new sorted list
    with the original list untouched
    """

    def srt(xs):
        aux = list(xs)
        sort_on_place(aux)
        return aux

    return srt


sort = {'bubble1': bubble1, 'bubble2': wrap(bubble2), 'bubble3': wrap(bubble3),
        'bubble4': wrap(bubble4),
        'msort': msort, 'qsort': qsort, 'hsort1': hsort1, 'hsort2': hsort2,
        'pysort': wrap(list.sort),
        'heap_sort_simon': heap_sort}

sortH = {  # 'bubble3': wrap(bubble3), 'bubble4': wrap(bubble4),
    'hsort1': hsort1, 'hsort2': hsort2, 'msort': msort,
    'pysort': wrap(list.sort)}

seed(64)

sys.setrecursionlimit(2450)  # 2450 is about the minimum to run the checkInvariants with n = 2400


class sortingTest(unittest.TestCase):
    def testSort(self):
        n = 2400  # 2400 is about the maximum on my computer
        rand = [randrange(10000) for _ in range(n)]
        xss = [[], [1], [2, 3, 1, 1], list(range(n)), list(range(n, -1, -1)), rand]

        for name, srt in sort.items():
            tstart = perf_counter()
            for xs in xss:
                ys = srt(xs)
                self.assertTrue(isSorted(ys))
            tstop = perf_counter()
            print('elapsed time for ' + name + ': ', tstop - tstart)

    def testSortHard(self):
        n = 100000
        rand = [randrange(10000) for _ in range(n)]
        xss = [[], [1], [2, 3, 1, 1], list(range(n)), list(range(n, -1, -1)), rand]

        for name, srt in sortH.items():
            tstart = perf_counter()
            for xs in xss:
                srt(xs)
            tstop = perf_counter()
            print('elapsed time for ' + name + ': ', tstop - tstart)

    def testHeap(self):
        h = Heap()
        xs = [2, 3, 1, 1]
        ys = []
        for x in xs:
            h.heappush(x)
        for _ in range(len(h)):
            ys.append(h.heappop())
        xs.sort()
        self.assertListEqual(xs, ys)
