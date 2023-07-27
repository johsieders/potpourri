## js 12.12.2020
# Comparing my Polynom with that of numpy.
# Main differences
# - you need trim() to trim leading zeros
# - coefficients are accessed by p.coef
# - it is much slower (factor 10)

import unittest

from numpy.polynomial.polynomial import Polynomial as Polynom


class TestPolynom(unittest.TestCase):

    def testBasics(self):
        z = Polynom((0, 0, 0, 0, 0, 0)).trim()
        self.assertEqual(0, z.degree())
        # self.assertFalse(z)
        self.assertEqual(0, z(27))

        p = Polynom((1, 1, 1, 0, 0)).trim()
        self.assertEqual(2, p.degree())
        self.assertTrue(p)
        self.assertEqual(1, p(-1))
        self.assertEqual(1, p(0))
        self.assertEqual(3, p(1))
        self.assertEqual(7, p(2))

        r = -p
        s = +p
        for i in range(-10, 10):
            self.assertEqual(r(i), -p(i))
            self.assertEqual(s(i), p(i))

        q = Polynom((0, 1, 0, 0)).trim()
        self.assertTrue(p)
        self.assertEqual(1, q.degree())
        for i in range(-10, 10):
            self.assertEqual(i, q(i))

    def testArithmetics(self):
        n = 5
        ps = [Polynom(range(k, 2 * k + 1)) for k in range(n)]
        for p in ps:
            q = p - p
            self.assertEqual(0, (p - p).degree())
            # self.assertFalse(p - p)
            for q in ps:
                for x in range(-10, 10):
                    self.assertEqual(p(x) + q(x), (p + q)(x))
                    self.assertEqual(p(x) - q(x), (p - q)(x))
                    self.assertEqual(p(x) * q(x), (p * q)(x))

    def testMul(self):
        a = Polynom((0,))
        b = Polynom((1,))
        p = Polynom((1, 2))
        q = Polynom((1, 1, 1))
        r = Polynom((1, -1, 1, -1, 1))

        ps = [a, b, p, q, r]
        for s in ps:
            for t in ps:
                self.assertEqual(s(1) * t(1), (s * t)(1))
                self.assertListEqual(list((s * t).coef), list((t * s).coef))

        for n in range(0, 10):
            for s in ps:
                t = s ** n
                self.assertEqual(s(1) ** n, (s ** n)(1))

    def testMixedArithmetic(self):
        a = Polynom(0)
        b = Polynom(1)
        p = Polynom((1, 2))
        q = Polynom((1, 1, 1))
        ps = [a, b, p, q]

        a1 = 0
        b1 = 1
        p1 = (1, 2)
        q1 = (1, 1, 1)
        ps1 = [a1, b1, p1, q1]

        for s in ps:
            for t in ps1:
                self.assertEqual(s(1) * Polynom(t)(1), (s * t)(1))
                self.assertListEqual(list((s * t).coef), list((t * s).coef))

    def testDiv(self):
        n = 10
        ps = [Polynom(k * [1]) for k in range(1, n)]
        for p in ps:
            for q in ps:
                a, r = divmod(p, q)
                t = a * q + r
                for i in range(len(p)):
                    self.assertAlmostEqual(p.coef[i], t.coef[i])
        n = 10
        ps = [Polynom(range(k, 2 * k + 1)) for k in range(n)]
        for p in ps:
            for q in ps[1:]:
                a, r = divmod(p, q)
                t = a * q + r
                for i in range(len(p)):
                    self.assertAlmostEqual(p.coef[i], t.coef[i])
                for x in range(-20, 20):
                    self.assertAlmostEqual(p(x), (p // q * q + p % q)(x))

    def testPolynomOfPolynom(self):
        a = Polynom((0,))
        b = Polynom((3,))
        p = Polynom((1, 2))
        q = Polynom((1, 1, 1))

        ps = [a, b, p, q]
        for s in ps:
            for t in ps:
                self.assertEqual(sum(s(t)), s(t(1)))
                self.assertEqual(s(t)(7), s(t(7)))

    # def testGcd(self):
    #     b = Polynom((3,))
    #     p = Polynom((1, 2))
    #     q = Polynom((1, 1, 1))
    #
    #     ps = [b, p, q]
    #     for s in ps:
    #         for t in ps:
    #             g = gcd(s, t)
    #             self.assertEqual(Polynom(0), s % g)
    #             self.assertEqual(Polynom(0), t % g)
