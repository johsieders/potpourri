# testing searching
# 20/11/2020

import unittest

from searching.rbtree import insert


class searchingTest(unittest.TestCase):
    def testInsert(self):
        tree = []
        for c in 'searching':
            t = insert(tree, c)
            if t:
                tree = t

        t = insert(tree, 'n')
        print(tree)
