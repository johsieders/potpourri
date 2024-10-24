# js 27.12.2003
# checked 08/01/2024

import unittest

from polynomials import Polynomial, distance, epsilon
from primes import gcd


class TestPolynomial(unittest.TestCase):

    def testDistance(self):
        p = Polynomial(1, 2, 3)
        q = Polynomial(1, 2, 3, 4)
        # print(distance(p, q))

    def testDivision(self):

        p = Polynomial(7)
        q = Polynomial(3)
        s, r = divmod(p, q)
        self.assertEqual(p, s * q + r)
        self.assertLess(r, q)

        p = Polynomial(1, 2, 3)
        q = Polynomial(1, 2, 3)
        s, r = divmod(p, q)
        self.assertEqual(p, s * q + r)
        self.assertLess(r, q)

        p = Polynomial(1, 2)
        q = Polynomial(1, 2, 3)
        s, r = divmod(p, q)
        self.assertEqual(p, s * q + r)
        self.assertLess(r, q)

        p = Polynomial(range(7))
        q = Polynomial(range(3))
        s, r = divmod(p, q)
        t = s * q + r
        self.assertEqual(p, s * q + r)
        self.assertLess(r, q)

        p = Polynomial(1, 2, 3)
        q = Polynomial(0, 0, 0, 0, 0, 6)
        s, r = divmod(p, q)
        self.assertEqual(p, s * q + r)
        self.assertLess(r, q)
        s, r = divmod(q, p)
        self.assertEqual(q, s * p + r)
        self.assertLess(r, p)

        p = Polynomial(1)
        q = Polynomial(1, 2, 3, 4, 5)
        s, r = divmod(p, q)
        self.assertEqual(p, s * q + r)
        self.assertLess(r, q)
        s, r = divmod(q, p)
        self.assertEqual(q, s * p + r)
        self.assertLess(r, p)

        p = Polynomial(5, 6, 7, 8, 9, 10)
        q = Polynomial(3, 4, 5, 6)
        s, r = divmod(p, q)
        self.assertEqual(p, s * q + r)
        self.assertLess(r, q)

    def testBasics(self):
        z = Polynomial(0, 0, 0, 0, 0, 0)
        self.assertEqual(0, z.degree())

        self.assertFalse(z)
        self.assertEqual(0, z(27))

        p = Polynomial(2, 3)
        self.assertEqual(7, p(2))

        p = Polynomial(1, 1, 1, 0, 0)
        self.assertEqual(4, p.degree())
        self.assertTrue(p)

        self.assertEqual(1, p(-1))
        self.assertEqual(0, p(0))
        self.assertEqual(3, p(1))
        self.assertEqual(28, p(2))

        r = -p
        s = +p
        for i in range(-10, 10):
            self.assertEqual(r(i), (-p)(i))
            self.assertEqual(s(i), p(i))

        q = Polynomial(0, 1, 0)
        self.assertTrue(p)
        self.assertEqual(1, q.degree())
        for i in range(-10, 10):
            self.assertEqual(i, q(i))

    def testArithmetics(self):

        testcases = [[Polynomial(1, 1) ** 5, Polynomial(1, 1)],
                     [Polynomial(3, 2, -1, 2), Polynomial(-1, 2)],
                     [Polynomial(3, 2, -1, 2), Polynomial(1)],
                     [Polynomial(1), Polynomial(3, 2)]]

        for p, q in testcases:
            s, r = divmod(p, q)
            self.assertEqual(p, q * s + r)
            self.assertLess(r, q)

        n = 10
        ps = [Polynomial(*range(k, 2 * k + 1)) for k in range(1, n)]
        for p in ps:
            self.assertEqual(0, (p - p).degree())
            self.assertFalse(p - p)
            for q in ps:
                for x in range(-10, 10):
                    self.assertEqual(p(x) + q(x), (p + q)(x))
                    self.assertEqual(p(x) - q(x), (p - q)(x))
                    self.assertEqual(p(x) * q(x), (p * q)(x))

    def testDiv(self):
        ps = [Polynomial(k * [1]) for k in range(1, 10)]
        for p in ps:
            for q in ps:
                s, r = divmod(p, q)
                self.assertLess(distance(p, q * s + r), epsilon)
                self.assertLess(r, q)

        n = 10
        ps = [Polynomial(range(k, 2 * k + 1)) for k in range(0, n)]
        for p in ps:
            for q in ps[1:]:
                s, r = divmod(p, q)
                self.assertLess(distance(p, q * s + r), epsilon)
                self.assertLess(r, q)

    def testMul(self):
        a = Polynomial(0)
        b = Polynomial(1)
        p = Polynomial(1, 2)
        q = Polynomial(1, 1, 1)
        r = Polynomial(1, -1, 1, -1, 1)

        ps = [a, b, p, q, r]
        for s in ps:
            for t in ps:
                self.assertEqual(s(1) * t(1), (s * t)(1))
                self.assertLess(distance(s * t, t * s), epsilon)

        for n in range(1, 10):
            for s in ps:
                self.assertEqual(s(5) ** n, (s ** n)(5))

    def testMixedArithmetic(self):
        a = Polynomial(0)
        b = Polynomial(1)
        p = Polynomial(1, 2)
        q = Polynomial(1, 1, 1)
        ps = [a, b, p, q]

        a1 = 0
        b1 = 1
        p1 = (1, 2)
        q1 = (1, 1, 1)
        ps1 = [a1, b1, p1, q1]

        for s in ps:
            for t in ps1:
                self.assertEqual(s(1) * Polynomial(t)(1), (s * t)(1))
                self.assertLess(distance(s * t, t * s), epsilon)

    #
    # def testPolynomOfPolynom(self):
    #     a = Polynomial((0,))
    #     b = Polynomial((3,))
    #     p = Polynomial((1, 2))
    #     q = Polynomial((1, 1, 1))
    #
    #     ps = [a, b, p, q]
    #     for s in ps:
    #         for t in ps:
    #             self.assertEqual(sum(s(t)), s(t(1)))
    #             self.assertEqual(s(t)(7), s(t(7)))
    #
    def testGcd(self):
        p = Polynomial(7)
        q = Polynomial(3)

        g = gcd(p, q)
        self.assertFalse(p % g)
        self.assertFalse(q % g)

        p = Polynomial(1, 0, -1)
        q = Polynomial(1, 1)
        g = gcd(p, q)
        self.assertFalse(p % g)
        self.assertFalse(q % g)

        g = gcd(p * q, p)
        self.assertFalse(p * q % g)
        self.assertFalse(p % g)
        g = gcd(p * q, q)
        self.assertFalse(p * q % g)
        self.assertFalse(q % g)

        p = Polynomial(1, 1)
        q = Polynomial(1, -1)
        g = gcd(p, q)
        self.assertFalse(p % g)
        self.assertFalse(q % g)

        # self.assertEqual(q, g)
    #
    # def testInt(self):
    #     p = Polynomial((1, 0, 1))
    #     q = Polynomial((1, 1))
    #
    #     self.assertEqual(26, p(5))
    #     self.assertEqual(101, p(10))
    #     self.assertEqual(26., p(5.))
    #     self.assertEqual(101., p(10.))
    #     self.assertEqual([2, 1, 1], p + q)
    #     self.assertEqual([2, 0, 1], p + 1)
    #     self.assertEqual([2, 0, 1], 1 + p)
    #     self.assertEqual([2, 0, 2], p * 2)
    #     self.assertEqual([2, 0, 2], 2 * p)
    #     self.assertEqual([2, 2, 1], p(q))
    #     self.assertEqual([2, 0, 1], q(p))
    #     self.assertEqual([1, 1, 1, 1], p * q)
    #     self.assertEqual([1, 1, 1, 1], q * p)
    #
    # def testFloat(self):
    #     p = Polynomial((1., 0., 1.))
    #     q = Polynomial((1., 1.))
    #     self.assertEqual(26., p(5))
    #     self.assertEqual(101., p(10))
    #     self.assertEqual(26., p(5.))
    #     self.assertEqual(101., p(10.))
    #     self.assertEqual([2., 1., 1.], p + q)
    #     self.assertEqual([2., 0., 1.], p + 1)
    #     self.assertEqual([2., 0., 1.], 1 + p)
    #     self.assertEqual([2., 0., 2.], p * 2)
    #     self.assertEqual([2., 0., 2.], 2 * p)
    #     self.assertEqual([2., 2., 1.], p(q))
    #     self.assertEqual([2., 0., 1.], q(p))
    #     self.assertEqual([1., 1., 1., 1.], p * q)
    #     self.assertEqual([1., 1., 1., 1.], q * p)
    #
    # def testComparison(self):
    #     z = Polynomial(0)
    #     e = Polynomial(1)
    #     p = Polynomial((1, 0, 1))
    #     q = Polynomial((2, 1))
    #     u = Polynomial((2, 1))
    #     v = Polynomial((2, 1))
    #
    #     self.assertFalse(p < q)
    #     self.assertTrue(z == 0)
    #     self.assertTrue(0 == z)
    #     self.assertFalse(z < 0)
    #     self.assertFalse(0 < z)
    #     self.assertTrue(0 <= z)
    #
    #     self.assertFalse(p < 1)
    #     self.assertFalse(1 == p)
    #     self.assertFalse(p == 1)
    #     self.assertTrue(1 < p)
