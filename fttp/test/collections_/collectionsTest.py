# testing collections
# 20/11/2020

import unittest

from collections_.collections2 import *
from collections_.hash import makeDict, Hashdict


class collectionsTest(unittest.TestCase):

    def testMerge(self):
        n = 10
        for i in range(n):
            xs = i * [1]
            ys = 2 * i * [1]
            m = merge1(xs, ys)
            self.assertListEqual(3 * i * [1], m)

        xs = [9, 11]
        ys = [2, 4, 5]
        expected_result = [2, 4, 5, 9, 11]
        self.assertListEqual(merge(xs, ys), expected_result)

    def testHistogram(self):
        histograms = (histogram0, histogram1, histogram2, histogram3)
        xss = [[], [1], [0, 1, 2, 2, 3, 3, 3]]
        for hg in histograms:
            for xs in xss:
                h = hg(xs)
                for x in xs:
                    self.assertEqual(h[x], xs.count(x))

    def testIndexA(self):
        book = [['xx', 'yy', 'zz'],
                ['xx', 'uu', 'zz'],
                ['xx', 'yy', 'vv', 'tt']]

        index = indexA(book)
        for w, ps in index.items():
            for p in ps:
                self.assertTrue(w in book[p])

    def testIndexB(self):
        book = [['xx', 'yy', 'zz'],
                ['xx', 'uu', 'zz'],
                ['xx', 'yy', 'vv', 'tt']]
        keywords = ['xx', 'tt']
        fs = (indexB1, indexB2)
        for f in fs:
            index = f(book, keywords)
            self.assertListEqual(keywords, list(index.keys()))
            for w, ps in index.items():
                for p in ps:
                    self.assertTrue(w in book[p])

    def testRomans(self):
        toRoman, fromRoman = romanTrafos()

        self.assertEqual('I', toRoman(1))
        self.assertEqual('CI', toRoman(101))

        self.assertEqual(1, fromRoman('I'))
        self.assertEqual(100, fromRoman('C'))

    def testMakeDict(self):
        g, s = makeDict()

        caught = False
        try:
            g(1)
        except ValueError:
            caught = True
        self.assertTrue(caught)

        n = 1000

        for i in range(n):
            s(i, str(5 * i))

        for i in range(n):
            s(i, str(10 * i))

        for i in range(n):
            self.assertEqual(str(10 * i), g(i))

    def testHash(self):
        dict = Hashdict()

        caught = False
        try:
            a = dict[1]
        except ValueError:
            caught = True
        self.assertTrue(caught)

        n = 1000

        for i in range(n):
            dict[i] = str(5 * i)

        for i in range(n):
            dict[i] = str(10 * i)

        for i in range(n):
            self.assertEqual(str(10 * i), dict[i])

    def testHanoi(self):
        # all checks in implementation
        n = 10
        # hanoi_naked(n)
        ps = hanoi(n)
        self.assertEqual(2 ** n, len(ps))
