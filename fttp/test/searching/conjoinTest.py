# testing iterators
# 20/11/2020

import unittest

from warmingup.warmingup2 import faculty

from searching.conjoin import *
from searching.searching2 import *


class conjoinTest(unittest.TestCase):
    def testConjoin(self):
        g = lambda: range(2)
        cs = conjoin(g, g, g, g)
        # self.assertEqual(len(list(cs)), 8)
        cs = conjoin1(g, g, g, g)
        print(cs)
        # self.assertEqual(len(list(cs)), 8)

    def testConjoin1(self):
        g = lambda: range(1, 5)
        f = lambda: range(5, 7)
        cs = conjoin(g, f)
        self.assertEqual(len(list(cs)), 8)
        cs = conjoin1(g, f)
        self.assertEqual(len(list(cs)), 8)

    def testRomans(self):
        toRomanList = list(romans())
        fromRomanMap = dict((toRomanList[n], n) for n in range(5000))
        self.assertEqual(fromRomanMap['XX'], 20)

    def testConjoinPermutations(self):
        xs = (1, 2, 3)
        p = permutations(xs)
        self.assertEqual(faculty(len(xs)), len(list(p)))

    def testPermutations1(self):
        xs = (2, 3, 4)
        p = PermutationProblem(xs)
        permutations = searchByFunction(p)
        self.assertEqual(faculty(len(xs)), len(permutations))

    def testQueens(self):
        q = queens(8)
        self.assertEqual(92, len(list(q)))
