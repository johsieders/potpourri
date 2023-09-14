# Integers over a prime p
# trying to understand the fields Fp
# reworked 19/07/2023

from ma import ModularArithmetic


class Fp(int):
    """
    Each instance of Fp represents an integer modulo p.
    Arithmetic operations are performed modulo p using the ModularArithmetic class.
    """

    def __new__(cls, value, N):
        obj = int.__new__(cls, value % N)  # create an instance of int
        obj.N = N
        obj.ma = None
        return obj

    def __add__(self, n: int) -> int:
        return Fp(super().__add__(n), self.N)

    def __sub__(self, n: int) -> int:
        return self.ma.sub(self, n)

    def __mul__(self, n: int) -> int:
        return self.ma.mul(self, n)

    def __truediv__(self, n: int) -> int | None:  # a / b
        return self.ma.div(self, n)

    def __eq__(self, n: int) -> bool:  # check equality
        return self - n == 0

    def __ne__(self, n: int) -> bool:  # check inequality
        return not self == n  # n is an M object

    def __invert__(self) -> int | None:  # inverse of self modulo N
        return self.ma.inv(self)  # None if it does not exist

    def __pow__(self, n: int, mode=None) -> int:
        return self.ma.mul(self, n)

    def __radd__(self, n: int) -> int:
        return self + n  # n is an F object

    def __rsub__(self, n: int) -> int:
        return self.ma.sub(n, self)

    def __rmul__(self, n: int) -> int:
        return self * n

    def __rtruediv__(self, n: int) -> int | None:  # a / b
        return self.ma.div(n, self)  # n is an M object

    def __lt__(self, n: int) -> bool:
        return self - n < 0

    def __le__(self, n: int) -> bool:
        return self - n <= 0

    def __gt__(self, n: int) -> bool:
        return self - n > 0

    def __ge__(self, n: int) -> bool:
        return self - n >= 0

    def __str__(self) -> str:
        return str(self) + " mod " + str(self.ma.primes)

    def __repr__(self) -> str:
        return str(self) + " mod " + str(self.ma.primes)

    def __hash__(self) -> int:
        return self

    def __neg__(self) -> int:
        return self.ma.sub(0, self)

    def __abs__(self) -> int:
        return self if self >= 0 else -self


class ModularFactory(object):
    """
    ModularFactory creates instances of M and sets the ModularArithmetic object ma.
    """

    def __init__(self, primes):
        self.ma = ModularArithmetic(primes)  # ModularArithmetic object

    def __call__(self, n: int) -> Fp:
        m = Fp(n)
        m.set_ma(self.ma, self)
        return m
