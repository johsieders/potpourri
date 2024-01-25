# Integers over a prime p
# trying to understand the fields Fp
# reworked 19/07/2023
# reworked 08/01/2024

from mp import Fp


class Mp(int):
    """
    Each instance of Fp represents an integer modulo N = p0 * p1 * ... pn-1.
    Arithmetic operations are performed modulo primes = [p0, p1, ..., pn-1]
    using the ModularArithmetic class. It is immutable as int is.
    It's all about the Chinese Remainder Theorem:
    Each integer n can be uniquely represented as [n%p0, n%p1, ..., n%pn-1], and
    each vector [k0, k1, ..., kn-1] can be transformed into an integer n mod N by
    the extended Euclid algorithm.
    Arithmetic operations on vectors [k0, k1, ..., kn-1] are elementwise performed.
    An integer n has an inverse iff it is coprime to N, or, equivalently, coprime to all pj.

    GPT about __new__:
    __new__ is where the object is actually created (especially crucial for immutable types).
    super(...). __new__ is a way to delegate part of the creation process to
    the parent class's __new__ method. This setup allows Fp to behave like an int,
    but with the added modular arithmetic functionality.
    Note that the __new__ method is static.
    __new__ and __init__ always have the same signature
    """

    @staticmethod  # just to be explicit
    def __new__(cls, v: int, ma: Fp):
        return super(Mp, cls).__new__(cls, v % ma.get_N())

    def __init__(self, v: int, ma: Fp):
        """
        :param v: the initial value
        :param ma: the associated modular arithmetic
        """
        super().__init__()
        self.ma = ma

    def __add__(self, n: int) -> int:
        return Mp(self.ma.add(self, n), self.ma)

    def __sub__(self, n: int) -> int:
        return Mp(self.ma.sub(self, n), self.ma)

    def __mul__(self, n: int) -> int:
        return Mp(self.ma.mul(self, n), self.ma)

    def __floordiv__(self, n: int) -> int | None:  # a / b
        d = self.ma.div(self, n)
        return Mp(d, self.ma) if d else None

    def __eq__(self, n: int) -> bool:  # check equality
        return int(self) == n

    def __ne__(self, n: int) -> bool:  # check inequality
        return not int(self) == n  # n is an M object

    # the inverse exists iff self is coprime to N, or (that's the same)
    # coprime to all p of ma.primes.
    # This is true for multiples of primes not in ma.primes
    def __invert__(self) -> int | None:  # inverse of self modulo N
        d = self.ma.inv(self)
        return Mp(d, self.ma) if d else None

    def __pow__(self, n: int) -> int:
        if n == 0:
            return Mp(1, self.ma)
        elif n == 1:
            return self
        elif n > 1:
            n0 = n // 2
            n1 = n - n0
            return (self ** n0) * (self ** n1)
        elif n < 0:  # assuming self coprime to N
            return ~ (self ** -n)

    def __radd__(self, n: int) -> int:
        return self + n

    def __rsub__(self, n: int) -> int:
        return (-1) * self + n

    def __rmul__(self, n: int) -> int:
        return self * n

    def __lt__(self, n: int) -> bool:
        return int(self) < n

    def __le__(self, n: int) -> bool:
        return int(self) <= n

    def __gt__(self, n: int) -> bool:
        return int(self) > n

    def __ge__(self, n: int) -> bool:
        return int(self) >= 0

    def __str__(self):
        return f"{int(self)} (mod {self.ma.get_N()})"

    def __repr__(self) -> str:
        return f"{int(self)} (mod {self.ma.get_N()})"

    def __hash__(self) -> int:
        return self

    def __neg__(self) -> int:
        return 0 - self
