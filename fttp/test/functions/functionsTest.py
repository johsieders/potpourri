# testing functions
# 13/11/2020

import unittest
from math import sin, cos, pi
from operator import add

from functions.functions2 import *

anagrams = ['Old Testament',
            'most talented',
            'carthose',
            'orchestra',
            'contaminated',
            'no admittance',
            'emigrants',
            'streaming',
            'Amery',
            'Mayer',
            'Cinerama',
            'American',
            'World Cup team',
            'talcum powder',
            'William Ewart Gladstone',
            'Wild agitator, means well']

xs = ['otto', 'anna', 'ttoo', 'oott', 'nnaa']


class functionsTest(unittest.TestCase):
    def testAnagram2(self):
        anagram_sort2(anagrams)
        for a in anagrams:
            print(a)

    def testAdd(self):
        f = addFun(sin, cos)
        x = f(pi)
        self.assertAlmostEqual(sin(pi) + cos(pi), x)

    def testCompose(self):
        f = compose(sin, cos)
        x = f(pi)
        self.assertAlmostEqual(sin(cos(pi)), x)

    def testCurry(self):
        add7 = curry(add, 7)
        x = add7(5)
        self.assertEqual(12, x)

    def testComposeAll(self):
        fs = [curry(add, i) for i in range(1, 11)]
        # 1 + 2 + ... + 10 = (10 * 11) / 2 = 55

        f = composeAll(fs)
        x = 100
        self.assertEqual(x + 55, f(x))

        f = composeAll1(fs)
        x = 100
        self.assertEqual(x + 55, f(x))

        f = composeAll2()(*fs)
        x = 100
        self.assertEqual(x + 55, f(x))

    def testBinary2nary(self):
        xadd = binary2nary(add)
        x = xadd(2, 3, 4)
        self.assertEqual(9, x)

        xmul = binary2nary(mul)
        x = xmul(2, 3, 4)
        self.assertEqual(24, x)

        fs = [curry(add, i) for i in range(1, 11)]
        F = composeAll2()
        f = F(*fs)
        x = 100
        self.assertEqual(x + 55, f(x))

    def testHorner(self):
        a = [1, 1, 1]
        y = horner(a, 2)
        self.assertEqual(7, y)

        # p = polynom(a)
        # y = p(2)
        # self.assertEqual(3, y)
