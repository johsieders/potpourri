## js 27.12.2003
## js 12.12.2020

import unittest

flag = 1

if flag:
    from classes.rational import Rational
else:
    from fractions import Fraction as Rational


class TestRational(unittest.TestCase):

    def testBasics(self):
        a = Rational(-5, 15)
        b = Rational(1, -3)
        z = Rational(0, 7)
        self.assertEqual(a, b)
        self.assertEqual(Rational(0, 1), z)

        self.assertEqual(-1, int(Rational(-3, 2)))
        self.assertEqual(0, int(a))
        self.assertEqual(0, int(Rational(1, 2)))

        self.assertEqual(Rational(1, 3), abs(a))
        self.assertEqual(Rational(1, 3), -a)
        self.assertEqual(a, +a)
        if flag:
            self.assertEqual(Rational(3, -1), ~a)
        self.assertAlmostEqual(-1 / 3, float(a))

    def testBasicArithmetic(self):
        a = Rational(5, 15)
        b = Rational(1, 2)
        self.assertEqual(Rational(5, 6), a + b)
        self.assertEqual(Rational(-1, 6), a - b)
        self.assertEqual(Rational(1, 6), a * b)
        self.assertEqual(Rational(2, 3), a / b)

        a = Rational(1, 2)
        b = Rational(3, 4)
        self.assertEqual(Rational(5, 4), a + b)
        self.assertEqual(Rational(-1, 4), a - b)
        self.assertEqual(Rational(3, 8), a * b)
        self.assertEqual(Rational(2, 3), a / b)

    def testCompare(self):
        r = Rational(1, 2)
        s = Rational(1, 2)
        t = Rational(3, 4)

        self.assertTrue(r == s)
        self.assertTrue(s < t)
        self.assertTrue(s <= t)
        self.assertTrue(t > s)
        self.assertTrue(t >= s)

    def testMixedArithmetic(self):
        a = Rational(1, 2)

        self.assertEqual(Rational(7, 2), a + 3)
        self.assertEqual(Rational(-5, 2), a - 3)
        self.assertEqual(Rational(3, 2), a * 3)
        self.assertEqual(Rational(1, 6), a / 3)

        self.assertEqual(Rational(7, 2), 3 + a)
        self.assertEqual(Rational(5, 2), 3 - a)
        self.assertEqual(Rational(3, 2), 3 * a)
        self.assertEqual(Rational(6, 1), 3 / a)

    def testInPlaceArithmetic(self):
        a = Rational(1, 2)
        b = Rational(3, 4)
        a += b
        self.assertEqual(Rational(5, 4), a)
        a = Rational(1, 2)
        a -= b
        self.assertEqual(Rational(-1, 4), a)
        a = Rational(1, 2)
        a *= b
        self.assertEqual(Rational(3, 8), a)
        a = Rational(1, 2)
        a /= b
        self.assertEqual(Rational(2, 3), a)
        a = Rational(1, 2)

    def testPower(self):
        num = 2
        denom = 3
        a = Rational(num, denom)
        for n in range(10):
            pw = Rational(num ** n, denom ** n)
            # print(pw)
            self.assertEqual(Rational(num ** n, denom ** n), a ** n)
