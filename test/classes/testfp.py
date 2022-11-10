# checkInvariants Z over p
# js 12.08.2004

import unittest
from classes.fp import *


class TestFp(unittest.TestCase):
    def testAri(self):
        F7 = makeFp(7)
        a = F7(5)
        b = F7(6)

        self.assertEqual(4, a + 6)
        self.assertEqual(4, 6 + a)
        self.assertEqual(4, a + b)

        self.assertEqual(6, a - 6)
        self.assertEqual(1, 6 - a)
        self.assertEqual(6, a - b)

        self.assertEqual(2, a * 6)
        self.assertEqual(2, 6 * a)
        self.assertEqual(2, a * b)

        self.assertEqual(2, a / 6)
        self.assertEqual(4, 6 / a)
        self.assertEqual(2, a / b)

        self.assertEqual(1, a ** 0)
        self.assertEqual(5, a ** 1)
        self.assertEqual(4, a ** 2)

