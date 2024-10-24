# Polynome
# js, 25.05.01
# ueberarbeitung 29.12.03, 1.1.2004, 15.7.2004, 9.8.2004
# ueberarbeitung 4.12.2020
# Idee, alles einfacher, nur int, aber vollständig
# checked 08/01/2024

from functools import reduce
from typing import Sequence

from euclidian_rings import EuclidianRing
from fields import Field

epsilon = 1e-8


def truncate(xs, eps=epsilon):
    """
    removes leading zeros
    :param xs: a list
    :return: xs with leading zeros removed or [0] if xs contains only zeros
    """
    if len(xs) == 0:
        return xs

    i = 0
    for i, x in enumerate(xs):
        if abs(x) > eps:
            break

    return xs[i:] if i < len(xs) else [xs[0]]


class Polynomial(EuclidianRing, list):
    """
    p(x) = a[0]x**(n-1) + a[1]x**(n-2) + ... + a[n-2]x + a[n-1]
    Invariants:
    - no leading zeros
    - each polynomial has at least one coefficient.
    - Highest coefficient is not zero unless the polynom is zero.
    - a polynomial is zero iff its only coefficient is zero.

    All meaningful operators are overloaded.
    Mixed arithmetic with collections implemented.
    Polynomials ARE list, any kind of subscripting works ([:] and the like)

    The class Polynomials implements polynomials over a field:
    - unary operators are defined (-, +)
    - binary operators are defined (+, -, /)
    """

    def __init__(self, *coefficients: Field):
        """
        :param coefficients: sequence of coefficients, trailing zeros are trimmed
        """
        if len(coefficients) == 0:
            raise ValueError

        if isinstance(coefficients[0], Sequence):
            coefficients = coefficients[0]

        # trim trailing zeros
        super().__init__(truncate(coefficients))

    def transform(self, x):
        return x if isinstance(x, Polynomial) else Polynomial(x)

    def lt(self, p):
        """
        :param p: another Polynom
        :return: True if len(self) < len(p) or self == [0] and p != [0]
        """
        return len(self) < len(p) or not self and p

    def __bool__(self, eps=epsilon):
        """
        :return: True if self(0) != 0
        A polynomial p is not zero iff p(0) != 0
        """
        return abs(self[0]) >= eps

    def eq(self, p):
        """
        :param p: another Polynom
        :return: True if self and p are close after normalizing
        Polynomials p, q are considered equal iff they differ by a constant factor,
        that is p = x * q or q = x * p
        """
        if self < p or p < self:
            return False
        elif not (self or p):
            return True
        else:
            q, r = self.my_divmod(p) if p else p.my_divmod(self)
            return len(q) == 1 and not r

    def add(self, q):
        """
        :param q: a polynomial or a list of coefficients
        :return: self + q
        """
        a, b = (self, q) if len(self) < len(q) else (q, self)
        # now len(a) <= len(b)
        result = list(b)
        for i in range(1, len(a) + 1):
            result[-i] += a[-i]

        return Polynomial(*result)

    def sub(self, q):
        """
        :param q: a polynomial or a list of coefficients
        :return: self - q
        """
        q = [-x for x in q]
        return self.add(q)

    def mul(self, q):
        """
        :param q: a polynomial or a list of coefficients
        :return: self * q
        """
        result = [0] * (len(self) + len(q) - 1)
        for i in range(len(self)):
            for j in range(len(q)):
                result[i + j] += self[i] * q[j]

        return Polynomial(*result)

    def my_divmod(self, q):
        """
        :param q: divisor
        :return: quotient and remainder of self and q
        """

        if not q:  # denominator must not be zero
            raise ValueError

        remainder = list(self)
        diff = len(remainder) - len(q)
        quotient = [0] * (max(0, diff) + 1)  # length of quotient

        while remainder[0] and diff >= 0:
            c = remainder[0] / q[0]
            for i in range(min(len(remainder), len(q))):
                remainder[i] -= c * q[i]
            quotient[-diff - 1] = c
            remainder = truncate(remainder)
            diff = len(remainder) - len(q)

        return Polynomial(*quotient), Polynomial(*remainder)

    def __abs__(self):
        return abs(self(0))

    def __str__(self):
        return 'Poly[' + ', '.join([str(c) for c in self]) + ']'

    def __call__(self, x):
        return reduce(lambda a, b: x * a + b, self)
