# check prime utilities
# reworked 20/07/2023
# js

import unittest
from functools import reduce

from nums.src.primes import *


class TestPrimes(unittest.TestCase):
    def testPrimefactors(self):
        ps = get_primes(10000)
        for n in range(2, 1000):
            f = primefactors(n, ps)
            result = reduce(lambda x, y: x * y, [ps[i] ** f[0][i] for i in range(len(f[0]))], 1) * f[1]
            self.assertEqual(n, result)

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
