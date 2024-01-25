# Integers over a prime p
# trying to understand modular arithmetic
# checked 08/01/2024

from fields import Field
from primes import inv


class Fp(Field):
    """
    This class implements modular arithmetic.
    It works on any class that implements a Euclidean Ring.
    """

    def __init__(self, v, p):
        """
        :param v: an element of an Euclidian Ring (e.g. int or polynomial)
        :param a prime (irreducible) element of an Euclidian Ring
        """
        self.prime = p  # checking for primality too hard (polynomials)
        self.value = v % p

    def transform(self, v):
        return v if isinstance(v, Fp) else Fp(v, self.prime)

    def eq(self, b):
        return self.value == b.value and self.prime == b.prime

    def __bool__(self):
        return bool(self.value)

    def add(self, b):
        return Fp(self.value + b.value, self.prime)

    def sub(self, b):
        return Fp(self.value - b.value, self.prime)

    def mul(self, b):
        return Fp(self.value * b.value, self.prime)

    def div(self, b):
        return Fp(self.value * inv(b.value, b.prime), self.prime)

    def __abs__(self):
        return abs(self.value)

    def __str__(self):
        return f"{str(self.value)}(mod {self.prime})"
