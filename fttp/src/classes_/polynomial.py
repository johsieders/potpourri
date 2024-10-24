# Polynome
# js, 25.05.01
# ueberarbeitung 29.12.03, 1.1.2004, 15.7.2004, 9.8.2004
# ueberarbeitung 4.12.2020
# Idee, alles einfacher, nur int, aber vollständig

# from collections.abc import Collection, Callable, Sequence
from functools import reduce

from warmingup.types_ import NewType, Collection, Callable, Sequence


def flip(f: Callable) -> Callable:
    return lambda x, y: f(y, x)  # flips args


def lastIdx(a: Sequence[int]) -> int:
    """
    :param a: a list of int
    :return: largest index idx such that a[i] = 0 for i >= idx
    -1 if a is empty
    """
    i = len(a) - 1
    while i > 0 and not a[i]:
        i -= 1
    return i + 1


Coefficient = NewType('coefficient', any)


class Polynomial(list):
    """
    p(x) = a[0] + a[1]x + a[2]x**2 + .. + a[n-2]x**(n-2) + a[n-1]x**(n-1)
    Invariants:
    - no trailing zeros
    - each polynom has at least one coefficient.
    - Highest coefficient is not zero unless the polynom is zero.
    - a polynom is zero iff its only coefficient is zero.

    All meaningful operators are overloaded (in place included) .
    Mixed arithmetic with collections implemented.
    In place operators (iadd, isub, ..) are really in place (no unnecessary objects)
    Polynoms ARE list, any kind of subscripting works ([:] and the like)

    Assumptions about Coefficient, the datatype of coefficients (hold for Rational):
    - X(0), X(1) work
    - bool is defined
    - comparison operators are defined (<, <=, ==)
    - unary operators are defined (-, +)
    - binary operators are defined (+, -, /)
    - on place operators are +=, -=, *= are defined

    Comparisons:
    lt: p < q iff (p - q)[-1] < 0, that is: p - q --> limit < 0 for x --> + oo
    le: p <= q iff (p - q)[-1] <= 0 that is: p - q --> limit >= 0 for x --> + oo (or == 0)
    le: p == q iff (p - q)[-1] == 0
    """

    def __init__(self, a: Coefficient):
        """
        :param a: sequence of coefficients, trailing zeros are trimmed
        If a is a single object (a number) it is replaced with [a]
        """
        if not isinstance(a, Collection):
            a = [a]
        if len(a) == 0:
            raise ValueError

        # trim trailing zeros
        super().__init__(a[:lastIdx(a)])
        self.coef = self  # for compatiblity with numpy

    def degree(self) -> int:
        return len(self) - 1

    def trim(self):  # for compatiblity with numpy
        return Polynomial(self)

    def __bool__(self):
        return len(self) > 1 or bool(self[0])

    def __call__(self, x: any) -> any:
        tmp = list(self)
        tmp.append(0)
        tmp.reverse()
        return reduce(lambda a, b: x * a + b, tmp)

    def __str__(self):
        string = ''
        for a in self:
            string += str(a) + ', '
        return '[' + string[:-2] + ']'

    #########################
    # comparison operators	#
    #########################

    def __lt__(self, p):
        if not isinstance(p, Polynomial):
            p = Polynomial(p)
        return (self - p)[-1] < 0

    def __le__(self, p):
        if not isinstance(p, Polynomial):
            p = Polynomial(p)
        return (self - p)[-1] <= 0

    def __eq__(self, p):
        if not isinstance(p, Polynomial):
            p = Polynomial(p)
        return (self - p)[-1] == 0

    #########################
    # arithmetic operators	#
    #########################

    def __neg__(self):
        return Polynomial([-a for a in self])

    def __pos__(self):
        return Polynomial(self)

    def __add__(self, p):
        result = Polynomial(self)
        result += p
        return result

    def __iadd__(self, p):
        """
        :param p: a polynom or whatever can be made one
        :return: self + Polynom(p)
        """
        if not isinstance(p, Polynomial):
            p = Polynomial(p)
        if not p:
            return self

        m = min(len(self), len(p))
        self.extend(p[len(self):])
        for i, a in enumerate(p[:m]):
            self[i] += a

        del self[lastIdx(self):]  # trim trailing zeros
        return self

    def __sub__(self, p):
        """
        :param p: a polynom or whatever can be made one
        :return: self - Polynom(p)
        """
        result = Polynomial(self)
        result += -p
        return result

    def __isub__(self, p):
        return self.__iadd__(-p)

    def __mul__(self, p):
        result = Polynomial(self)
        result *= p
        return result

    def __imul__(self, p):
        """
        :param p: a polynom or whatever can be made one
        :return: self * Polynom(p)
        """
        if not isinstance(p, Polynomial):
            p = Polynomial(p)

        if not p or not self:  # one factor is zero
            self[:] = [0]
            return self
        else:
            aux = [0] * (len(self) + len(p) - 1)
            for i in range(len(self)):
                for j in range(len(p)):
                    aux[i + j] += self[i] * p[j]
            self[:] = aux[:]
            return self

    def __floordiv__(self, p):
        return self.__divmod__(p)[0]

    def __ifloordiv__(self, p):
        q = self.__divmod__(p)[0]
        self[:] = q[:]
        return self

    def __mod__(self, p):
        return self.__divmod__(p)[1]

    def __divmod__(self, p):
        """
        :param p: divisor
        :return: quotient q and remainder r of self and p
        """
        if not isinstance(p, Polynomial):
            p = Polynomial(p)
        if not p:  # denominator must not be zero
            raise ValueError

        q = []  # the to-be-quotient
        r = list(self)  # the to-be-remainder
        while len(r) >= len(p):
            c = r[-1] / p[-1]
            q.append(c)
            for i in range(-len(p), 0):
                r[i] -= c * p[i]
            del r[-1]

        if len(r) == 0:  # r empty if no remainder
            r = [0]
        if len(q) == 0:  # q empty if len(self) < len(p)
            q[:] = [0]
        else:
            q.reverse()

        return Polynomial(q), Polynomial(r)

    def __pow__(self, n):
        result = Polynomial(1)
        for _ in range(n):
            result *= self
        return result

    # make operators with reversed operands
    __radd__ = __add__
    __rmul__ = __mul__
    __rsub__ = flip(__sub__)
    __rfloordiv__ = flip(__floordiv__)
    __rmod__ = flip(__mod__)
    __ge__ = flip(__le__)
    __gt__ = flip(__lt__)
