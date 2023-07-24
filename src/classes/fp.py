# Integers over a prime p
# trying to understand the fields Fp
# reworked 19/07/2023

from typing import Tuple, List


def ext_gcd(a, b):  # return gcd of a and b
    """
    return gcd of a and b and s, t such that
        a * s + b * t = gcd(a, b)
    """
    s, u = 1, 0
    t, v = 0, 1

    while b:
        q, r = divmod(a, b)
        a, b = b, r
        s, u = u, s - q * u
        t, v = v, t - q * v
    return a, s, t


def ext_gcd_rec(a: int, b: int, s=1, u=0, t=0, v=1) -> Tuple[int, int, int]:
    """
    return gcd(a, b) and s, t such that
        a * s + b * t = gcd(a, b)
    """
    if b == 0:
        return a, s, t
    else:
        q, r = divmod(a, b)
        return ext_gcd_rec(b, r, u, s - q * u, v, t - q * v)


def inv(a: int, m: int) -> int:
    """
    :param a: an integer
    :param m: an integer coprime to a
    :return: inverse of a modulo m
    """
    g, s, t = ext_gcd(a, m)
    if g != 1:
        raise ValueError("No inverse for %d modulo %d" % (a, m))
    return s % m


def chinese_remainder_2(a: List[int], m: List[int]) -> int:
    """
    :param a: list of two integers
    :param m: list of two coprime integers
    :return: x such that x = a[i] mod m[i] for i = 0, 1
    """
    g, s, t = ext_gcd(m[0], m[1])
    if g != 1:
        raise ValueError("No inverse for %d modulo %d" % (m[0], m[1]))
    return a[0] * t * m[1] + a[1] * s * m[0]


def chinese_remainder(a: List[int], m: List[int]) -> int:
    """
    :param a: list of integers
    :param m: list of coprime integers
    :return: x such that x = a[i] mod m[i] for all i
    """

    a0 = a[0] % m[0]
    m0 = m[0]

    for i in range(1, len(a)):
        a1 = a[i] % m[i]
        m1 = m[i]
        a0 = chinese_remainder_2([a0, a1], [m0, m1])
        m0 *= m1

    return a0


def chinese_remainder_copilot(a: List[int], m: List[int]) -> int:
    """
    :param a: list of integers
    :param m: list of coprime integers
    :return: x such that x = a[i] mod m[i] for all i
    """
    n = len(a)
    M = 1
    for i in range(n):
        M *= m[i]
    M_i = [M // m_i for m_i in m]
    y_i = [inv(M_i[i], m[i]) for i in range(n)]
    x = 0
    for i in range(n):
        x += a[i] * M_i[i] * y_i[i]
    return x % M


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

    def toModular(self, x: int) -> List[int]:
        """
        :param x: an integer
        :return: n modulo p
        """
        return [x % p for p in self.primes]

    def fromModular(self, x: List[int]) -> int:
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
        pa = self.toModular(a)
        pb = self.toModular(b)
        pc = [op(pa[i], pb[i]) for i in range(len(self.primes))]
        result = self.fromModular(pc)
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
        pa = self.toModular(a)
        try:
            pb = [inv(pa[i], self.primes[i]) for i in range(len(self.primes))]
        except ValueError:
            return None
        return self.fromModular(pb)

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

    def __new__(cls, value):
        obj = int.__new__(cls, value)  # create an instance of int
        obj.ma = None
        return obj

    def set_ma(self, ma: ModularArithmetic, mf: ModularFactory):
        self.ma = ma
        self.mf = mf

    def __add__(self, n: int) -> int:
        return self.ma.add(self, n)

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
