## Integers over a prime p
## trying to understand the fields Fp

from functools import reduce
from operator import mul


def powm(a, d, m):  # returns a power d modulo m
    result = 1
    a = a % m
    while d > 0:
        if d % 2:
            result = (result * a) % m
        a = (a * a) % m
        d = d >> 1
    return result


def makeFp(p):
    """ p must be prime.
        makeFp returns a subclass Fp of F
    """

    class Fp(F):
        pass

    return Fp(p)


class F(int):
    """ F represents the fields Fp (integers over p where p is prime)
        F ist abstract. Subclasses supply the prime self.p
    """

    def __init__(self, p):
        super().__init__()
        self.p = p

    def __add__(self, n):
        return type(self)(int.__add__(self, n) % self.p)

    def __sub__(self, n):
        return type(self)(int.__sub__(self, n) % self.p)

    def __rsub__(self, n):
        return type(self)(int.__sub__(n, self) % self.p)

    def __mul__(self, n):
        return type(self)(int.__mul__(self, n) % self.p)

    def __invert__(self):
        return type(self)(int.__pow__(self, self.p - 2) % self.p)

    def __div__(self, n):
        return self * ~n

    def __rdiv__(self, n):
        return n * ~self

    def __pow__(self, **kwargs):
        # if not isinstance(n, (int, long)):
        #     raise TypeError, 'int or long required'
        return reduce(mul, [self] * n, 1)

    __radd__, __rmul__ = __add__, __mul__
