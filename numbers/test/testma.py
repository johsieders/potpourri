# checkInvariants Z over p
# js 12/08/2004
# reworked 20/07/2023

import unittest
from functools import reduce

from numbers.src.ma import ModularArithmetic
from numbers.src.primes import get_primes


class TestModularArithmetic(unittest.TestCase):
    def testBasics(self):
        primes = get_primes(1000)
        ma = ModularArithmetic(primes)
        N = ma.get_N()
        for x in range(100):
            mx = ma.to_modular(x)
            y = ma.from_modular(mx)
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
