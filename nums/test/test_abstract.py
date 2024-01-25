# checkInvariants Z over p
# js 12/08/2004
# reworked 20/07/2023
# reworked 16/01/2024

import unittest
from functools import reduce

from euclidian_rings import EuclidianRing
from fields import Field
from primes import gcd, inv
from rings import Ring


class TestAbstract(unittest.TestCase):
    def challenge_ring(self, *x: Ring):
        if len(x) < 1:
            raise ValueError("at least 1 argument is required")

        self.assertEqual(x[0], x[0])
        self.assertNotEqual(x[0], x[0] + 1)

        self.assertEqual(0, 0 + x[0] - x[0])
        self.assertEqual(0, 0 + x[0] + -x[0])
        self.assertEqual(0, 0 - +x[0] + x[0])
        self.assertEqual(1, x[0] - x[0] + 1)

        self.assertEqual(1, +x[0] - x[0] + 1)
        self.assertEqual(1, +x[0] - x[0] + 1)

        self.assertEqual(x[0] + x[0], 2 * x[0])
        self.assertEqual(x[0] - 2, x[0] - 1 - 1)
        self.assertNotEqual(x[0], x[0] - 1)

        y = list(x)
        y.reverse()

        self.assertEqual(sum(x), sum(y))
        self.assertEqual(sum(x) * sum(y), sum(y) * sum(x))
        px = reduce(lambda a, b: a * b, x)
        py = reduce(lambda a, b: a * b, y)
        self.assertEqual(px, py)
        self.assertEqual(x[0] * sum(x[1:]), sum([x[0] * a for a in x[1:]]))

        y = [-a for a in x]
        self.assertEqual(sum(x), -sum(y))

        self.assertEqual(1, x[0] ** 0)
        self.assertEqual(x[0], x[0] ** 1)
        self.assertEqual(x[0] * x[0], x[0] ** 2)

    def challenge_field(self, *x: Field):
        self.challenge_ring(*x)

        self.assertEqual(x[0], x[0] / 1)
        self.assertEqual(x[0] * x[1], x[0] * x[1] / 1)

        y = [a for a in x if a]
        py = reduce(lambda a, b: a * b, y)

        for a in y:
            self.assertEqual(py, (py / a) * a)
            self.assertEqual(1, (1 / a) * a)
            self.assertEqual(1, a * a ** -1)
            # self.assertEqual(1, a ** 2 * a ** -2)

    def challenge_div(self, p: EuclidianRing, q: EuclidianRing):
        if gcd(p, q) != 1 or not q:  # nothing to test, q could be a zero divider
            return

        s, r = divmod(p, q)
        self.assertEqual(p, q * s + r)
        self.assertLess(r, q)
        self.assertEqual(r, p % q)
        self.assertEqual(s, p // q)
        u = p * q + 1
        if u:
            r = inv(p, u)
            if r:
                self.assertEqual(1, p * r % u)

    def challenge_euclidian_ring(self, *x: EuclidianRing):
        if len(x) < 3:
            raise ValueError("at least 3 arguments are required")

        self.challenge_ring(*x)

        self.challenge_div(0, x[0])
        self.challenge_div(1, x[0])
        self.challenge_div(x[0], 1)
        self.challenge_div(x[0], x[0])
        self.challenge_div(x[0], x[1])
        self.challenge_div(x[0], x[2])
        self.challenge_div(x[2], x[0])
        self.challenge_div(x[0] + 1, x[0] - 1)
        self.challenge_div(1 + x[0], 1 - x[0])
        self.challenge_div((1 + x[0]) * (1 - x[0]), 1 + x[0])
