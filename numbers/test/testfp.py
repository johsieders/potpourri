# checkInvariants Z over p
# js 12/08/2004
# reworked 20/07/2023

import unittest
from functools import reduce

from numbers.src.fp import Fp


class TestFp(unittest.TestCase):
    def testAri(self):
        primes = [2, 3, 5, 7]
        N = reduce(lambda x, y: x * y, primes)
        # ma = ModularArithmetic(primes)
        a = Fp(5, N)
        b = Fp(6, N)
        c = Fp(7, N)
        print(a, b, c)
        d = a + 2
        e = a + b
        print(d, e)

        # self.assertEqual(11, a + 6)
        # self.assertEqual(11, 6 + a)
        # self.assertEqual(11, a + b)
        #
        # self.assertEqual(6, a - 6)
        # self.assertEqual(1, 6 - a)
        # self.assertEqual(6, a - b)
        #
        # self.assertEqual(2, a * 6)
        # self.assertEqual(2, 6 * a)
        # self.assertEqual(2, a * b)
        #
        # self.assertEqual(2, a / 6)
        # self.assertEqual(4, 6 / a)
        # self.assertEqual(2, a / b)
        #
        # self.assertEqual(1, a ** 0)
        # self.assertEqual(5, a ** 1)
        # self.assertEqual(4, a ** 2)
