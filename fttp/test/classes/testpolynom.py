## js 27.12.2003


import unittest

from classes.polynomial import Polynomial
from classes.rational import gcd


class TestPolynom(unittest.TestCase):

    def testBasics(self):
        z = Polynomial((0, 0, 0, 0, 0, 0))
        self.assertEqual(0, z.degree())
        self.assertFalse(z)
        self.assertEqual(0, z(27))

        p = Polynomial((1, 1, 1, 0, 0))
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

        q = Polynomial((0, 1, 0, 0))
        self.assertTrue(p)
        self.assertEqual(1, q.degree())
        for i in range(-10, 10):
            self.assertEqual(i, q(i))

    def testArithmetics(self):
        n = 5
        ps = [Polynomial(range(k, 2 * k + 1)) for k in range(n)]
        for p in ps:
            q = p - p
            self.assertEqual(0, (p - p).degree())
            self.assertFalse(p - p)
            for q in ps:
                for x in range(-10, 10):
                    self.assertEqual(p(x) + q(x), (p + q)(x))
                    self.assertEqual(p(x) - q(x), (p - q)(x))
                    self.assertEqual(p(x) * q(x), (p * q)(x))

    def testMul(self):
        a = Polynomial((0,))
        b = Polynomial((1,))
        p = Polynomial((1, 2))
        q = Polynomial((1, 1, 1))
        r = Polynomial((1, -1, 1, -1, 1))

        ps = [a, b, p, q, r]
        for s in ps:
            for t in ps:
                self.assertEqual(s(1) * t(1), (s * t)(1))
                self.assertListEqual(s * t, t * s)

        for n in range(0, 10):
            for s in ps:
                t = s ** n
                self.assertEqual(s(1) ** n, (s ** n)(1))

    def testMixedArithmetic(self):
        a = Polynomial(0)
        b = Polynomial(1)
        p = Polynomial((1, 2))
        q = Polynomial((1, 1, 1))
        ps = [a, b, p, q]

        a1 = 0
        b1 = 1
        p1 = (1, 2)
        q1 = (1, 1, 1)
        ps1 = [a1, b1, p1, q1]

        for s in ps:
            for t in ps1:
                self.assertEqual(s(1) * Polynomial(t)(1), (s * t)(1))
                self.assertListEqual(s * t, t * s)

    def testDiv(self):
        n = 10
        ps = [Polynomial(k * [1]) for k in range(1, n)]
        for p in ps:
            for q in ps:
                a, r = divmod(p, q)
                t = a * q + r
                for i in range(len(p)):
                    self.assertAlmostEqual(p[i], t[i])
        n = 10
        ps = [Polynomial(range(k, 2 * k + 1)) for k in range(n)]
        for p in ps:
            for q in ps[1:]:
                a, r = divmod(p, q)
                t = a * q + r
                for i in range(len(p)):
                    self.assertAlmostEqual(p[i], t[i])
                for x in range(-20, 20):
                    self.assertAlmostEqual(p(x), (p // q * q + p % q)(x))

    def testPolynomOfPolynom(self):
        a = Polynomial((0,))
        b = Polynomial((3,))
        p = Polynomial((1, 2))
        q = Polynomial((1, 1, 1))

        ps = [a, b, p, q]
        for s in ps:
            for t in ps:
                self.assertEqual(sum(s(t)), s(t(1)))
                self.assertEqual(s(t)(7), s(t(7)))

    def testGcd(self):
        b = Polynomial((3,))
        p = Polynomial((1, 2))
        q = Polynomial((1, 1, 1))

        ps = [b, p, q]
        for s in ps:
            for t in ps:
                g = gcd(s, t)
                self.assertEqual(0, s % g)
                self.assertEqual(0, t % g)

    def testInt(self):
        p = Polynomial((1, 0, 1))
        q = Polynomial((1, 1))

        self.assertEqual(26, p(5))
        self.assertEqual(101, p(10))
        self.assertEqual(26., p(5.))
        self.assertEqual(101., p(10.))
        self.assertEqual([2, 1, 1], p + q)
        self.assertEqual([2, 0, 1], p + 1)
        self.assertEqual([2, 0, 1], 1 + p)
        self.assertEqual([2, 0, 2], p * 2)
        self.assertEqual([2, 0, 2], 2 * p)
        self.assertEqual([2, 2, 1], p(q))
        self.assertEqual([2, 0, 1], q(p))
        self.assertEqual([1, 1, 1, 1], p * q)
        self.assertEqual([1, 1, 1, 1], q * p)

    def testFloat(self):
        p = Polynomial((1., 0., 1.))
        q = Polynomial((1., 1.))
        self.assertEqual(26., p(5))
        self.assertEqual(101., p(10))
        self.assertEqual(26., p(5.))
        self.assertEqual(101., p(10.))
        self.assertEqual([2., 1., 1.], p + q)
        self.assertEqual([2., 0., 1.], p + 1)
        self.assertEqual([2., 0., 1.], 1 + p)
        self.assertEqual([2., 0., 2.], p * 2)
        self.assertEqual([2., 0., 2.], 2 * p)
        self.assertEqual([2., 2., 1.], p(q))
        self.assertEqual([2., 0., 1.], q(p))
        self.assertEqual([1., 1., 1., 1.], p * q)
        self.assertEqual([1., 1., 1., 1.], q * p)

    def testComparison(self):
        z = Polynomial(0)
        e = Polynomial(1)
        p = Polynomial((1, 0, 1))
        q = Polynomial((2, 1))
        u = Polynomial((2, 1))
        v = Polynomial((2, 1))

        self.assertFalse(p < q)
        self.assertTrue(z == 0)
        self.assertTrue(0 == z)
        self.assertFalse(z < 0)
        self.assertFalse(0 < z)
        self.assertTrue(0 <= z)

        self.assertFalse(p < 1)
        self.assertFalse(1 == p)
        self.assertFalse(p == 1)
        self.assertTrue(1 < p)
