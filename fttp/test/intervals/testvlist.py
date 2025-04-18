# Python Test Intervalle
# js, 8.6.04
# js 25.12.04

import unittest

from src.intervals.vlist import *

N = 10


class TestInterval(unittest.TestCase):
    def testIntersection(self):
        v = Vlist((0, 10), (20, 30))
        w = v.intersect((-10, -5))
        self.failUnlessEqual(w, iv())

        w = v.intersect((-10, 0))
        self.failUnlessEqual(w, iv())

        w = v.intersect((-10, 5))
        self.failUnlessEqual(w, Vlist((0, 5)))

        w = v.intersect((-10, 10))
        self.failUnlessEqual(w, Vlist((0, 10)))

        w = v.intersect((-10, 15))
        self.failUnlessEqual(w, Vlist((0, 10)))

        w = v.intersect((-10, 20))
        self.failUnlessEqual(w, Vlist((0, 10)))

        w = v.intersect((-10, 25))
        self.failUnlessEqual(w, Vlist((0, 10), (20, 25)))

        w = v.intersect((-10, 30))
        self.failUnlessEqual(w, Vlist((0, 10), (20, 30)))

        w = v.intersect((-10, 35))
        self.failUnlessEqual(w, Vlist((0, 10), (20, 30)))

        ## untere Grenze wandert, obere Grenze fest
        w = v.intersect((35, 40))
        self.failUnlessEqual(w, Vlist())

        w = v.intersect((30, 40))
        self.failUnlessEqual(w, Vlist())

        w = v.intersect((25, 40))
        self.failUnlessEqual(w, Vlist((25, 30)))

        w = v.intersect((20, 40))
        self.failUnlessEqual(w, Vlist((20, 30)))

        w = v.intersect((15, 40))
        self.failUnlessEqual(w, Vlist((20, 30)))

        w = v.intersect((10, 40))
        self.failUnlessEqual(w, Vlist((20, 30)))

        w = v.intersect((5, 40))
        self.failUnlessEqual(w, Vlist((5, 10), (20, 30)))

        w = v.intersect((0, 40))
        self.failUnlessEqual(w, Vlist((0, 10), (20, 30)))

        w = v.intersect((-10, 40))
        self.failUnlessEqual(w, Vlist((0, 10), (20, 30)))

    def testAppend(self):
        v = Vlist((0, 10), (20, 30))
        v.append((-10, -5))
        self.failUnlessEqual(v, Vlist((-10, -5), (0, 10), (20, 30)))

        v = Vlist((0, 10), (20, 30))
        v.append((-10, 0))
        self.failUnlessEqual(v, Vlist((-10, 10), (20, 30)))

        v = Vlist((0, 10), (20, 30))
        v.append((-10, 5))
        self.failUnlessEqual(v, Vlist((-10, 10), (20, 30)))

        v = Vlist((0, 10), (20, 30))
        v.append((-10, 10))
        self.failUnlessEqual(v, Vlist((-10, 10), (20, 30)))

        v = Vlist((0, 10), (20, 30))
        v.append((-10, 15))
        self.failUnlessEqual(v, Vlist((-10, 15), (20, 30)))

        v = Vlist((0, 10), (20, 30))
        v.append((-10, 20))
        self.failUnlessEqual(v, Vlist((-10, 30)))

        v = Vlist((0, 10), (20, 30))
        v.append((-10, 25))
        self.failUnlessEqual(v, Vlist((-10, 30)))

        v = Vlist((0, 10), (20, 30))
        v.append((-10, 30))
        self.failUnlessEqual(v, Vlist((-10, 30)))

        v = Vlist((0, 10), (20, 30))
        v.append((-10, 35))
        self.failUnlessEqual(v, Vlist((-10, 35)))

        ## untere Grenze wandert, obere Grenze fest
        v = Vlist((0, 10), (20, 30))
        v.append((35, 40))
        self.failUnlessEqual(v, Vlist((0, 10), (20, 30), (35, 40)))

        v = Vlist((0, 10), (20, 30))
        v.append((30, 40))
        self.failUnlessEqual(v, Vlist((0, 10), (20, 40)))

        v = Vlist((0, 10), (20, 30))
        v.append((25, 40))
        self.failUnlessEqual(v, Vlist((0, 10), (20, 40)))

        v = Vlist((0, 10), (20, 30))
        v.append((20, 40))
        self.failUnlessEqual(v, Vlist((0, 10), (20, 40)))

        v = Vlist((0, 10), (20, 30))
        v.append((15, 40))
        self.failUnlessEqual(v, Vlist((0, 10), (15, 40)))

        v = Vlist((0, 10), (20, 30))
        v.append((10, 40))
        self.failUnlessEqual(v, Vlist((0, 40)))

        v = Vlist((0, 10), (20, 30))
        v.append((5, 40))
        self.failUnlessEqual(v, Vlist((0, 40)))

        v = Vlist((0, 10), (20, 30))
        v.append((0, 40))
        self.failUnlessEqual(v, Vlist((0, 40)))

        v = Vlist((0, 10), (20, 30))
        v.append((-10, 40))
        self.failUnlessEqual(v, Vlist((-10, 40)))

    def testMake(self):
        vs = Vlist()

    def testContains(self):
        v = Vlist((None, None))
        self.failUnless(-1 in v)
        self.failUnless(0 in v)
        self.failUnless(1 in v)

        v = Vlist((0, 10))
        self.failUnless(0 in v)
        self.failUnless(9.9 in v)
        self.failUnless(10 not in v)

    def testAnd(self):
        v = Vlist((None, 0))
        w = Vlist((0, None))
        self.failUnlessEqual(Vlist(), v & w)

        v = Vlist((0, 10))
        self.failUnlessEqual(v, v & v)
        self.failUnlessEqual(+v, v & +v)

        w = Vlist((0, 20))
        self.failUnlessEqual(v, v & w)
        self.failUnlessEqual(+v, v & +w)

        w = Vlist((5, 15))
        self.failUnlessEqual(Vlist((5, 10)), v & w)
        self.failUnlessEqual(+Vlist((5, 10)), v & +w)

    def testUnion(self):
        v = Vlist((0, 1))
        w = Vlist((0, 1))
        self.failUnlessEqual(w, v | w)
        self.failUnlessEqual(w, w | v)

        w = v | Vlist((1, 2))
        self.failUnlessEqual(w, Vlist((0, 2)))

        w = v | Vlist((2, 3))
        self.failUnlessEqual(w, Vlist((0, 1), (2, 3)))

    def testDifference(self):
        pass
        v = Vlist((0, 4))
        w = Vlist((2, 6))
        self.failUnlessEqual(v - w, Vlist((0, 2)))
        self.failUnlessEqual(w - v, Vlist((4, 6)))
        self.failUnlessEqual(v ^ w, (v - w) | (w - v))
        self.failUnlessEqual(v ^ w, (v | w) - (v & w))

    def testEmpty(self):
        e = Vlist()
        self.failUnlessEqual(e, e)
        self.failUnless(not e < e)
        self.failUnlessEqual('', repr(e))
        self.failIf(-1 in e)
        self.failIf(0 in e)
        self.failIf(1 in e)

    def testHard(self):
        vs = Vlist(*[(a, a + 10) for a in range(0, 1000, 20)])
        self.failUnlessEqual(500, vs.sum())
        self.failUnlessEqual(Vlist((None, None)), vs | -vs)
        self.failUnlessEqual(Vlist(), vs & -vs)

    def testHarder(self):
        vs = Vlist(*[(a, a + 1) for a in range(N)])
        self.failUnlessEqual(Vlist((None, None)), vs | -vs)
        self.failUnlessEqual(Vlist(), vs & -vs)
