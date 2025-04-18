# testing classes_
# 20/11/2020
# This exercise shows three ways how to make
# static data and methods available


import unittest

from classes_.romans import *

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

class classesTest(unittest.TestCase):

    def testRomans(self):
        tofrom = (Roman.toRoman, Roman.fromRoman), \
            (RomanFunc.toRoman, RomanFunc.fromRoman), \
            (toRoman1, fromRoman1)

        for toRoman, fromRoman in tofrom:
            self.assertEqual('I', toRoman(1))
            self.assertEqual('CI', toRoman(101))

            self.assertEqual(1, fromRoman('I'))
            self.assertEqual(100, fromRoman('C'))



class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

