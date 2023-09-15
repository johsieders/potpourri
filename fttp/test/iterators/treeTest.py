# j.siedersleben
# fasttrack to professional programming
# testing iterators applied to trees
# 1.1.2021


import unittest
from heapq import heappush

from iterators.trees import *


class TreesTest(unittest.TestCase):

    def testBfo2tree(self):
        h = []
        t = bfo2tree(h)
        bfs = breadthfirst(t)
        self.assertIsNone(t)
        self.assertListEqual(h, list(bfs))

        for x in [10, 20, 15, 25, 10, 30, 5]:
            heappush(h, x)
            t = bfo2tree(h)
            bfs = breadthfirst(t)
            self.assertListEqual(h, list(bfs))

    def testPreorder2tree(self):
        h = []
        t = pre2tree(h)
        pre = list(preorder(t))
        pass
        self.assertIsNone(t)
        self.assertListEqual(h, list(pre))

        heappush(h, 10)
        heappush(h, 20)
        heappush(h, 15)
        heappush(h, 25)
        t = bfo2tree(h)
        pre = list(preorder(t))
        s = pre2tree(pre)
        print(s)
        # for x in [10, 20, 15, 25, 10, 30, 5]:
        # for x in [10, 20, 15]:
        #     heappush(h, x)          # h is bfo list
        #     t = bfo2tree(h)         # t is a binary tree
        #     pre = list(preorder(t)) # pre is preorder list
        #     s = pre2tree(pre)       # s is a binary tree
        #
        #     bfs = breadthfirst(s)   # bfs is a bfo list equal to h
        #     self.assertListEqual(h, list(bfs))

    def testPreorder(self):
        h = []
        t = bfo2tree(h)
        pre = preorder2(t)
        self.assertIsNone(t)
        self.assertListEqual(h, list(pre))

        for x in [10, 20, 15, 25, 10, 30, 5]:
            heappush(h, x)
            t = bfo2tree(h)
            p = list(preorder(t))
            q = list(preorder2(t))
            self.assertListEqual(p, q)

        heappush(h, 10)
        heappush(h, 20)
        t = bfo2tree(h)
        p = list(preorder(t))
        q = list(preorder2(t))
        self.assertListEqual(p, q)

    def testInorder(self):
        h = []
        t = bfo2tree(h)
        inord = inorder1(t)
        self.assertIsNone(t)
        self.assertListEqual(h, list(inord))

        for x in [10, 20, 15, 25, 10, 30, 5]:
            heappush(h, x)
            t = bfo2tree(h)
            p = list(inorder(t))
            q = list(inorder1(t))
            self.assertListEqual(p, q)
