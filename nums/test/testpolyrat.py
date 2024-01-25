# checkInvariants polynoms of rationals
# js 16.12.2020
# revisited 08.01.2024

import unittest

from polynomials__ import Polynomial

from rationals import Rational


class TestPolynomial(unittest.TestCase):
    def testWithRational(self):
        z = Rational(0)
        r = Rational(1)
        s = Rational(1, 2)
        t = Rational(3, 4)

        p = Polynomial(z)
        q = Polynomial((r, s))
        w = Polynomial((s, t, r))

        self.assertEqual(z + w, w)
        self.assertEqual(w + z, w)
        self.assertEqual(w * z, z)
        self.assertEqual(z * w, z)
        self.assertEqual(w * r, w)
        self.assertEqual(r * w, w)
        # self.assertEqual(w / r, w)
        # self.assertEqual(t * w, w)

        #      Be careful!
        #       t  + w --> t + Rational(w)
        #       t * w --> t * Rational(w)
        self.assertEqual((w + t)(7), t + w(7))
        self.assertEqual((w * t)(7), t * w(7))
