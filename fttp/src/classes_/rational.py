## Rationale Zahlen
## js 15.7. 2004
## js 12.12.2020
## nur int; keine Polymorphie
## Idee: so einfach wie möglich, aber vollständig


def gcd(a, b):  # return gcd of a and b
    while b:
        a, b = b, a % b
    return a


def flip(f):
    return lambda x, y: f(y, x)


class Rational(object):
    """
    rational numbers, works for int only
    denominator must never be zero
    Invariants:
    - denominator = 1 if numerator = 0
    - denominator always positive
    - numerator and denominator always reduced.
    All meaningful operators are overloaded (in place included) .
    Mixed arithmetic with int implemented.
    Three mild optimizations:
    - no unnecessary reductions thanks to flag "reduced"
    - early division by gcd in basic operations to keep numbers small
    - in place operators (iadd, isub, ..) are really in place (no unnecessary objects)
    """

    def __init__(self, num=0, denom=1, reduced=False):
        if denom == 0:
            raise ValueError('denominator must not be zero, is ' + str(denom))
        self.numerator = num
        self.denominator = denom
        if not reduced:
            self.reduce()

    def __bool__(self):
        return bool(self.numerator)

    def reduce(self):
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

    def __call__(self, x):
        return self.numerator(x) / self.denominator(x)

    def __int__(self):
        return self.numerator // self.denominator if self.numerator >= 0 \
            else - (-self.numerator // self.denominator)

    def __abs__(self):
        return Rational(abs(self.numerator), self.denominator, True)

    def __neg__(self):
        return Rational(-self.numerator, self.denominator, True)

    def __pos__(self):
        return Rational(self.numerator, self.denominator, True)

    def __invert__(self):
        result = Rational(self.denominator, self.numerator, True)
        result.normalize()
        return result

    def __str__(self):
        return str(self.numerator) + '/' + str(self.denominator)

    def __add__(self, r):
        result = Rational(self.numerator, self.denominator, True)
        result += r
        return result

    def __iadd__(self, r):
        if not isinstance(r, Rational):
            r = Rational(r)
        if not r:
            return self

        g = gcd(self.denominator, r.denominator)
        self.numerator = self.numerator * r.denominator // g \
                         + self.denominator // g * r.numerator
        self.denominator = self.denominator // g * r.denominator
        return self

    def __sub__(self, r):
        result = Rational(self.numerator, self.denominator, True)
        result += -r
        return result

    def __isub__(self, r):
        return self.__iadd__(-r)

    def __mul__(self, r):
        result = Rational(self.numerator, self.denominator, True)
        result *= r
        return result

    def __imul__(self, r):
        if not isinstance(r, Rational):
            r = Rational(r)

        if not r or not self:  # one factor is zero
            self.numerator = 0
            self.denominator = 1
            return self
        else:
            g1 = gcd(self.numerator, r.denominator)
            g2 = gcd(self.denominator, r.numerator)
            self.numerator = self.numerator // g1 * r.numerator // g2
            self.denominator = self.denominator // g2 * r.denominator // g1
            return self

    def __truediv__(self, r):
        result = Rational(self.numerator, self.denominator, True)
        result /= r
        return result

    def __itruediv__(self, r):
        if not isinstance(r, Rational):
            r = Rational(r)
        if not r:
            raise ValueError

        g1 = gcd(self.numerator, r.numerator)
        g2 = gcd(self.denominator, r.denominator)
        self.numerator = self.numerator // g1 * r.denominator // g2
        self.denominator = self.denominator // g2 * r.numerator // g1
        self.normalize()
        return self

    def __pow__(self, n):
        result = Rational(1, 1, True)
        for _ in range(n):
            result *= self
        return result

    def __lt__(self, r):
        if not isinstance(r, Rational):
            r = Rational(r)
        return self.numerator * r.denominator - \
            self.denominator * r.numerator < 0

    def __le__(self, r):
        if not isinstance(r, Rational):
            r = Rational(r)
        return self.numerator * r.denominator - \
            self.denominator * r.numerator <= 0

    def __eq__(self, r):
        if not isinstance(r, Rational):
            r = Rational(r)
        return self.numerator * r.denominator \
            == self.denominator * r.numerator

    # make operators with reversed operands
    __radd__ = __add__
    __rmul__ = __mul__
    __rsub__ = flip(__sub__)
    __rtruediv__ = flip(__truediv__)
    __ge__ = flip(__le__)
    __gt__ = flip(__lt__)
