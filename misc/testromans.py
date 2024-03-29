# testing nums
# 20/11/2020
# j.siedersleben
# checked 08.01.2024


import unittest

from misc.romans import *


class TestRomans(unittest.TestCase):
    def testRomans(self):
        tofrom = (Roman.toRoman, Roman.fromRoman), \
            (RomanFunc.toRoman, RomanFunc.fromRoman), \
            (toRoman1, fromRoman1)

        for toRoman, fromRoman in tofrom:
            self.assertEqual('I', toRoman(1))
            self.assertEqual('CI', toRoman(101))

            self.assertEqual(1, fromRoman('I'))
            self.assertEqual(100, fromRoman('C'))
