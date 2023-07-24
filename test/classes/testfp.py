# checkInvariants Z over p
# js 12/08/2004
# reworked 20/07/2023

import unittest
from functools import reduce

from classes.fp import *


class TestExtGcd(unittest.TestCase):
    def testExtGcd(self):
        data = [(1, 0), (81, 99), (99, 81), (123, 456), (456, 123),
                (123456789, 987654321), (987654321, 123456789)]
        for a, b in data:
            d, s, t = ext_gcd(a, b)
            self.assertEqual(d, a * s + b * t)

    def testInv(self):
        data = [(1, 2), (2, 3), (3, 5), (4, 7), (5, 11), (6, 13), (7, 17)]
        for a, m in data:
            b = inv(a, m)
            self.assertEqual(1, a * b % m)

    def testChineseRemainder(self):
        data = [([0, 2], [2, 3]), ([2, 3], [3, 5]), ([2, 3, 2], [3, 5, 7])]
        for a, m in data:
            b = chinese_remainder(a, m)
            for i in range(len(a)):
                self.assertEqual(a[i] % m[i], b % m[i])


class TestModularArithmetic(unittest.TestCase):
    def testBasics(self):
        primes = [2, 3, 7, 11, 13, 17, 19, 23, 29]
        N = reduce(lambda a, b: a * b, primes)
        ma = ModularArithmetic(primes)
        xs = [0, 1, 20, 300, 4000, 50000, 6, 7, 8]
        for x in xs:
            mx = ma.toModular(x)
            y = ma.fromModular(mx)
            self.assertEqual(x % N, y % N)

    def testOperations(self):
        primes = [2, 3, 5, 7]
        N = reduce(lambda x, y: x * y, primes)
        ma = ModularArithmetic(primes)
        data = [(1, 2), (2, 3), (3, 5), (4, 7), (5, 11), (6, 13), (7, 17)]
        for (a, b) in data:
            c = ma.add(a, b)
            self.assertEqual(c % N, (a + b) % N)
            d = ma.sub(a, b)
            self.assertEqual(d % N, (a - b) % N)
            e = ma.mul(a, b)
            self.assertEqual(e % N, (a * b) % N)
            f = ma.inv(a)
            if f:
                self.assertEqual(1, (a * f) % N)
            g = ma.div(a, b)
            if g:
                self.assertEqual(g % N, a * ma.inv(b) % N)


class TestMA(unittest.TestCase):
    def testAri(self):
        primes = [2, 3, 5, 7]
        mf = ModularFactory(primes)
        a = mf(5)
        b = mf(6)
        c = mf(a)
        d = a + 2
        e = a + b

        self.assertEqual(11, a + 6)
        self.assertEqual(11, 6 + a)
        self.assertEqual(11, a + b)

        self.assertEqual(6, a - 6)
        self.assertEqual(1, 6 - a)
        self.assertEqual(6, a - b)

        self.assertEqual(2, a * 6)
        self.assertEqual(2, 6 * a)
        self.assertEqual(2, a * b)

        self.assertEqual(2, a / 6)
        self.assertEqual(4, 6 / a)
        self.assertEqual(2, a / b)

        self.assertEqual(1, a ** 0)
        self.assertEqual(5, a ** 1)
        self.assertEqual(4, a ** 2)

