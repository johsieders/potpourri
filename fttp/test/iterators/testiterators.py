# Python Test iterators
# js, 8.6.04

from itertools import count, repeat
from unittest import makeSuite, TestCase, TestSuite, TextTestRunner

from iterators.iterators2 import *

sf = ((None, None), (0, 31), (10, 41), (20, None))
tf = ((None, None), (0, 63), (5, 23), (15, 53), (20, None))
sum_sftf = ((None, None), (0, 94), (5, 54), (10, 64), (15, 94), (20, None))

uf = ((None, None), (0, 100), (10, 200), (20, 100), (30, None))
vf = ((None, None), (0, 200), (10, 100), (20, 200), (30, None))
sum_ufvf = ((None, None), (0, 300), (30, None))

wf = ((None, 500),)
xf = ((None, None), (0, 700))
sum_wfxf = ((None, 500), (0, 1200))

sum_all = ((None, 500), (0, 1594), (5, 1554), (10, 1564), (15, 1594), (20, 1500), (30, 1200))
max_all = ((None, 500), (0, 700))
min_all = ((None, 500), (0, 31), (5, 23), (15, 41), (20, 100), (30, 500))


class TestIterator(TestCase):

    def testFmerge(self):
        self.failUnlessEqual(sum_sftf, take(10, fmerge(add, sf, tf)))
        self.failUnlessEqual(sum_ufvf, take(10, fmerge(add, uf, vf)))
        self.failUnlessEqual(sum_wfxf, take(10, fmerge(add, wf, xf)))
        self.failUnlessEqual(sum_all, take(10, fmerge(add, sf, tf, uf, vf, wf, xf)))
        self.failUnlessEqual(max_all, take(10, fmerge(max, sf, tf, uf, vf, wf, xf)))
        self.failUnlessEqual(min_all, take(10, fmerge(min, sf, tf, uf, vf, wf, xf)))

    def testHamming(self):
        h = hamming(3, 5, 7)
        self.failUnlessEqual((1, 3, 5, 7, 9, 15), take(6, h))

    def testProduct1(self):
        p = multiply(repeat(1), repeat(1))
        q = count()
        next(q)
        self.failUnlessEqual(take(1000, p), take(1000, q))

    def testProduct2(self):
        p = multiply(count(), repeat(1))
        self.failUnlessEqual((0, 1, 3, 6, 10, 15), take(6, p))
        p = multiply(repeat(1), count())
        self.failUnlessEqual((0, 1, 3, 6, 10, 15), take(6, p))

    def testProduct3(self):
        """ cos**2 + sin**2 = 1 """
        c2 = square(cos())
        s2 = square(sin())
        p = (x1 + x2 for x1, x2 in izip(c2, s2))
        self.assertAlmostEqual(1.0, next(p))
        for i in range(1, 100):
            self.assertAlmostEqual(0.0, next(p))

    def testInvert(self):
        """ exp_taylor(x) * exp_taylor(-x) = 1 """
        x = inverse(exp())
        p = multiply(exp(), x)
        self.assertAlmostEqual(1.0, next(p))
        for i in range(1, 100):
            self.assertAlmostEqual(0.0, next(p))

    def testMerge(self):
        m = merge((), ())
        self.assertEqual(len(tuple(m)), 0)
        m = merge(range(10), range(20))
        self.assertEqual(sum(m), 235)


def suite():
    suite = TestSuite()
    suite.addTest(makeSuite(TestIterator))
    return suite


if __name__ == '__main__':
    runner = TextTestRunner()
    runner.run(suite())
