# testing classes
# 20/11/2020
# This exercise shows three ways how to make
# static data and methods available


import unittest

from classes.romans import *


class classesTest(unittest.TestCase):
    def testRomans(self):
        tofrom = (Roman.toRoman, Roman.fromRoman), \
                 (RomanFunc.toRoman, RomanFunc.fromRoman), \
                 (toRoman1, fromRoman1)

        for toRoman, fromRoman in tofrom:
            self.assertEqual('I', toRoman(1))
            self.assertEqual('CI', toRoman(101))

            self.assertEqual(1, fromRoman('I'))
            self.assertEqual(100, fromRoman('C'))
