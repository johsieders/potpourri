# Integers over a prime p
# trying to understand the fields Fp
# reworked 19/07/2023


class M(int):
    """
    Each instance of M represents an integer modulo N.
    Arithmetic operations are performed modulo N using the ModularArithmetic class.
    """

    def __new__(cls, value, N):
        obj = int.__new__(cls, value % N)  # create an instance of int
        obj.N = N
        return obj

    def __add__(self, n: int) -> int:
        return M(super().__add__(n), self.N)
