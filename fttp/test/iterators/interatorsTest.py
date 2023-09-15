# testing iterators
# 20/11/2020

import unittest
from math import exp, sin, cos

from classes.polynomial import Polynomial

from iterators.iterators2 import *


class classesTest(unittest.TestCase):
    def testSending1(self):
        g = sending1(7)
        a = next(g)
        b = next(g)
        self.assertEqual(7, a)
        self.assertEqual(8, b)

        g = sending1(7)
        a = next(g)
        b = g.send(70)
        self.assertEqual(7, a)
        self.assertEqual(70, b)

    def testSending3(self):
        s = sending3(5)
        a0 = next(s)
        a1 = next(s)
        a2 = next(s)
        a3 = next(s)
        next(s)
        print(a0, a1, a2, a3)

        s = sending3(5)
        a0 = next(s)
        a1 = s.send(11)
        a2 = next(s)
        a3 = next(s)
        next(s)
        print(a0, a1, a2, a3)

        s = sending3(5)
        a0 = next(s)
        a1 = s.send(11)
        a2 = next(s)
        a3 = next(s)
        next(s)
        print(a0, a1, a2, a3)

        s = sending3(5)  # i0 = 5
        a0 = next(s)  # yield i0
        a1 = s.send(11)  # i1 = 11; yield i1
        a2 = next(s)  # yield i1
        a3 = s.send(33)  # i3 = 33; yield i3
        next(s)  # yield None
        print(a0, a1, a2, a3)

    def testCounter(self):
        t = counter(10)
        a = next(t)
        b = next(t)
        c = t.send(8)
        d = next(t)

        self.assertEqual(0, a)
        self.assertEqual(1, b)
        self.assertEqual(8, c)
        self.assertEqual(9, d)

    def testConst(self):
        cst = const(7)
        self.assertListEqual([7] * 10, take(cst, 10))

        nat = naturals()
        self.assertListEqual(list(range(10)), take(nat, 10))

    def testAri(self):
        self.assertEqual(list(range(5)), take(ari(1), 5))

    def testGeo(self):
        self.assertEqual([7 ** k for k in range(5)], take(geo(7), 5))

    def testFibo(self):
        self.assertEqual([1, 1, 2, 3, 5, 8], take(fibo(), 6))
        self.assertEqual([1, 1, 2, 3, 5, 8], take(Fibo(), 6))

    def testTaylor(self):
        exp_p = Polynomial(take(exp_taylor(), 20))
        sin_p = Polynomial(take(sin_taylor(), 20))
        cos_p = Polynomial(take(cos_taylor(), 20))

        for x in range(-3, 3):
            self.assertAlmostEqual(exp_p(x), exp(x), 8)
            self.assertAlmostEqual(sin_p(x), sin(x), 8)
            self.assertAlmostEqual(cos_p(x), cos(x), 8)

    def testMerge(self):
        m = merge()
        self.assertEqual(0, len(tuple(m)))
        m = merge(())
        self.assertEqual(0, len(tuple(m)))
        m = merge((), ())
        self.assertEqual(0, len(tuple(m)))
        m = merge((), (1,))
        self.assertEqual(1, len(tuple(m)))
        m = merge((1,), ())
        self.assertEqual(1, len(tuple(m)))
        m = merge((1,), (1,))
        self.assertEqual(2, len(tuple(m)))
        m = merge(range(10), range(20))
        self.assertEqual(235, sum(m))
        m = merge(range(10), range(20), range(30))
        self.assertEqual(670, sum(m))
        m = merge(range(100000), range(200000), range(300000))
        self.assertEqual(69999700000, sum(m))

    def testMerge1(self):
        merge = merge1
        m = merge((), ())
        self.assertEqual(0, len(tuple(m)))
        m = merge((), (1,))
        self.assertEqual(1, len(tuple(m)))
        m = merge((1,), ())
        self.assertEqual(1, len(tuple(m)))
        m = merge((1,), (1,))
        self.assertEqual(2, len(tuple(m)))
        m = merge(range(10), range(20))
        self.assertEqual(235, sum(m))

    def testTee(self):
        t = fibo()
        forks = tee1(t, 3)
        f0 = take(forks[0], 3)
        f1 = take(forks[1], 4)
        f2 = take(forks[2], 5)
        f0 += take(forks[0], 5)
        f1 += take(forks[1], 4)
        f2 += take(forks[2], 3)
        self.assertListEqual(f0, f1)
        self.assertListEqual(f1, f2)

    def testHamming(self):
        h = hamming(3, 5, 7)

        # self.assertEqual([1, 3, 5, 7, 9, 15], take(h, 6))
