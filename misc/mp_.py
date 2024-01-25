# Integers over a prime p
# trying to understand modular arithmetic
# reworked 19/07/2023
# checked 08/01/2024

from functools import reduce
from typing import List

from primes import chinese_remainder, inv


class MA(object):
    """
    This class implements the arithmetic mod N; N = p0 * p1 * ... * pn-1
    p is a list of coprime nums, generally a list of primes.
    """

    def __init__(self, primes: list):
        """
        :param primes: list of different primes
        N = product of primes
        """
        super().__init__()
        self.primes = list(primes)
        self.N = reduce(lambda x, y: x * y, primes)

    def get_N(self) -> int:
        return self.N

    def to_modular(self, a: int) -> List[int]:
        """
        :param a: an integer
        :return: m such that m[i] = a modulo p[i]
        """
        return [a % p for p in self.primes]

    def from_modular(self, m: List[int]) -> int:
        """
        :param m: an integer represented modulo primes
        :return: a such that n = xs[i] mod p[i] for all i
        """
        return chinese_remainder(m, self.primes)

    # def perform(self, op, a: int, b: int) -> int:
    #     """
    #     :param op: a binary operation
    #     :param a: an integer
    #     :param b: another integer
    #     :return: op(a, b) mod N
    #     """
    #     ma = self.to_modular(a)
    #     mb = self.to_modular(b)
    #     mc = [op(ma[i], mb[i]) for i in range(len(self.primes))]
    #     return self.from_modular(mc)

    def add(self, a: int, b: int) -> int:
        ma = self.to_modular(a)
        mb = self.to_modular(b)
        mc = [ma[i] + mb[i] for i in range(len(self.primes))]
        return self.from_modular(mc)

    def sub(self, a: int, b: int) -> int:
        return self.add(a, -b)

    def mul(self, a: int, b: int) -> int:
        ma = self.to_modular(a)
        mb = self.to_modular(b)
        mc = [ma[i] * mb[i] for i in range(len(self.primes))]
        return self.from_modular(mc)

    def inv(self, a: int) -> int | None:
        """
        :param a: an integer
        :return: inverse of a modulo N if it exists, None otherwise
        The inverse exists iff gcd(a, p) == 1 for all p in primes
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
        :param b: another integer
        :return: (a / b) mod N if b has an inverse, None otherwise
        """
        pb = self.inv(b)
        return self.mul(a, pb) if pb else None
