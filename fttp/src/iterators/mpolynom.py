# Polynome mit mehr als einem Parameter
# js, 25.05.01
# ueberarbeitung 29.12.03, 1.1.2004, 15.7.2004, 9.8.2004

from de.fhro.inf.fputil import flip
from poly import Polynom


class MPolynom(object):
    """
    p(x) = c[0] + c[1]x + c[2]x**2 + .. + c[n-2]x**(n-2) + c[n-1]x**(n-1)
    no trailing zeros
    any polynom has at least one coefficient.
    a polynom is zero iff its only coefficient is zero

    This class is intended for polynoms over any field
    self.__zero = cs[0] - cs[0]
    coefficients must support +, -, *, /, bool
    """

    def __init__(self, cs):
        """ c: multi-array of coefficients
        """
        if cs.rank < 1:
            raise ValueError
        self.cs = cs

    def degree(self):
        return [n - 1 for n in cs.shape]

    def __nonzero__(self):
        return len(self) > 1 or bool(self[0])

    def curry(x):
        pass

    def __call__(self, *xs):
        if len(x) != self.cs.rank:
            raise ValueError
        if self.cs.rank == 1:
            return Polynom(self.cs)(xs[0])
        else:
            return self.curry(xs[0])(*x[1:])

    #########################
    # arithmetic operations	#
    #########################

    def __neg__(self):
        return MPolynom(-self.cs)

    def __pos__(self):
        return Polynom(self.cs)

    def __add__(self, p):
        return MPolynom(self.cs + p.cs)

    def __sub__(self, p):
        return self + -p

    def __mul__(self, p):
        s, q = coerce(self, p)
        result = [self.__zero] * (len(self) + len(q) - 1)
        for i in range(len(self)):
            for j in range(len(q)):
                result[i + j] += self[i] * q[j]
        return Polynom(result)

    def __divmod__(self, p):
        """ q = quotient
            r = remainder
            invariant: self = p * q + r """
        s, p = coerce(self, p)
        q = []
        r = list(self)
        while len(r) >= len(p):
            c = r[-1] / p[-1]  ## quotient of highest coefficients
            q.append(c)
            for i in range(-len(p), 0):
                r[i] -= c * p[i]
            del r[-1]  ## discard highest coefficient

        q.reverse()
        if len(q) == 0:
            q.append(self.__zero)
        if len(r) == 0:
            r.append(self.__zero)
        return Polynom(q), Polynom(r)

    def __mod__(self, p):
        return divmod(self, p)[1]

    def __div__(self, p):
        return divmod(self, p)[0]

    def __pow__(self, n):
        ## kein coerce!!
        from operator import mul
        if not isinstance(n, (int, long)):
            raise TypeError
        if not n:
            return Polynom([self.__zero])
        else:
            return reduce(mul, [self] * n)

    # make operators with reversed operands
    __radd__, __rmul__ = __add__, __mul__
    __rsub__, __rdiv__, __rmod__ = [flip(m) for m in [__sub__, __div__, __mod__]]


## end of class Polynom

p = Polynom([-2, 2] * 30)
if __name__ == '__main__':
    from timeit import *

    t = Timer('p(7543.0)', 'from poly import p')
    print
    t.repeat(3, 10000)
