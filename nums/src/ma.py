# Integers over a prime p
# trying to understand modular arithmetic
# reworked 19/07/2023

from functools import reduce
from typing import List

from primes import chinese_remainder, inv


class ModularArithmetic(object):
    """
    Modular arithmetic
    """

    def __init__(self, primes: List[int]):
        """
        :param primes: list of different primes
        N = product of primes
        """
        self.primes = list(primes)
        self.N = reduce(lambda x, y: x * y, primes)

    def get_N(self) -> int:
        return self.N

    def to_modular(self, x: int) -> List[int]:
        """
        :param x: an integer
        :return: n modulo p
        """
        # todo: optimize this for large N
        return [x % p for p in self.primes]

    def from_modular(self, x: List[int]) -> int:
        """
        :param x: a list of integers
        :return: n such that n = x[i] mod p[i] for all i
        """
        return chinese_remainder(x, self.primes)

    def perform(self, op, a: int, b: int) -> int:
        """
        :param op: a binary operation
        :param a: an integer
        :param b: an integer
        :return: op(a, b) modulo N
        """
        pa = self.to_modular(a)
        pb = self.to_modular(b)
        pc = [op(pa[i], pb[i]) for i in range(len(self.primes))]
        result = self.from_modular(pc)
        return result

    def add(self, a: int, b: int) -> int:
        return self.perform(lambda x, y: x + y, a, b)

    def sub(self, a, b):
        return self.perform(lambda x, y: x - y, a, b)

    def mul(self, a, b):
        return self.perform(lambda x, y: x * y, a, b)

    def inv(self, a: int) -> int | None:
        """
        :param a: an integer
        :return: inverse of a modulo N if it exists, None otherwise
        """
        pa = self.to_modular(a)
        try:
            pb = [inv(pa[i], self.primes[i]) for i in range(len(self.primes))]
        except ValueError:
            return None
        return self.from_modular(pb)

    def div(self, a: int, b: int) -> int | None:  # a / b
        """
        :param a: an integer
        :param b: an integer
        :return: a / b modulo N if it exists, None otherwise
        """
        pb = self.inv(b)
        if pb is None:
            return None
        return self.mul(a, pb)


class M(int):
    """
    Each instance of M represents an integer modulo N.
    Arithmetic operations are performed modulo N using the ModularArithmetic class.
    """

    def __new__(cls, value, N):
        obj = int.__new__(cls, value % N)  # create an instance of int
        obj.N = N
        obj.ma = None
        return obj

    def __add__(self, n: int) -> int:
        return M(super().__add__(n), self.N)

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

    def __call__(self, n: int) -> M:
        m = M(n)
        m.set_ma(self.ma, self)
        return m
