# Rationale Zahlen

# checked 08/01/2024

from euclidian_rings import Comparable
from fields import Field
from primes import gcd


class Rational(Field, Comparable):
    """
    This class implements the field of rational nums over an Euclidian ring.
    The field can be integers, polynomials, or some Fp.

    Invariants:
    - denominator is never zero
    - denominator = 1 if numerator = 0
    - denominator always positive
    - numerator and denominator always shortened.

    Two mild optimizations:
    - no unnecessary reductions thanks to flag "shortened"
    - early division by gcd in basic operations to keep nums small
    """

    def __init__(self, num=0, denom=1, shortened=False):
        if not denom:
            raise ValueError('denominator must not be zero, is ' + str(denom))
        self.numerator = num
        self.denominator = denom
        if not shortened:
            self.shorten()

    def transform(self, num=0, denom=1):
        return num if isinstance(num, Rational) else Rational(num, denom)

    def add(self, b):
        return Rational(self.numerator * b.denominator + self.denominator * b.numerator,
                        self.denominator * b.denominator)

    def sub(self, b):
        return Rational(self.numerator * b.denominator - self.denominator * b.numerator,
                        self.denominator * b.denominator)

    def mul(self, b):
        return Rational(self.numerator * b.numerator, self.denominator * b.denominator)

    def div(self, b):
        return Rational(self.numerator * b.denominator, self.denominator * b.numerator)

    def eq(self, b):
        return self.numerator * b.denominator == self.denominator * b.numerator

    def __lt__(self, b):
        b = self.transform(b)
        return self.numerator * b.denominator < self.denominator * b.numerator

    def shorten(self):
        self.normalize()
        g = gcd(self.numerator, self.denominator)
        self.numerator //= g
        self.denominator //= g

    def normalize(self):
        if self.numerator == 0:
            self.denominator = 1
        elif self.numerator < 0:
            self.numerator = -self.numerator
            self.denominator = -self.denominator

    def __float__(self):
        return self.numerator / self.denominator

    def __int__(self) -> int:
        """
        Converts self into an integer rounded towards 0
        :return: self as int
        Note that a // b rounds towards minus infinity
        """
        return self.numerator // self.denominator if self.numerator >= 0 \
            else -(-self.numerator // self.denominator)

    def __abs__(self) -> float:
        return abs(self.__float__())

    def __call__(self, x) -> Field:
        """
        :param x: whatever numerator and denominator accept
        :return: quotient of the results
        This call succeeds if the numerator and denominator accept ()
        and self.denominator(x) != 0.
        What does NOT work:
        (1) (self.numerator / self.denominator)(x),
        because numerator and denominator do not support /
        (2) Rational(self.numerator(x) / self.denominator(x))
        because (numerator(x) / denominator(x)) does not support //
        """
        return self.numerator(x) / self.denominator(x)

    def __str__(self) -> str:
        return str(self.numerator) + '/' + str(self.denominator)
