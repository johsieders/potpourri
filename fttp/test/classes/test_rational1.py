import unittest

from classes_.romans import *

class test_classes1(unittest.TestCase):
    def test_rat_num_basics(self):
        d = Rational(2, 4)
        e = Rational(0, 1)
        f = Rational(2, 4)

        self.assertEqual(e, Rational(0, 2))
        #  self.assertRaises(ValueError, Rational(2, 0))
        self.assertEqual(d, f)

    def test_rat_operations(self):
        d = Rational(2, 4)
        e = Rational(0, 1)
        f = Rational(1, 4)

        # self.assertEqual(d + e, d)
        # self.assertEqual(d + f, Rational(3, 4))
        self.assertTrue(d + e == d)
