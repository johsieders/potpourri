# trying to understand primes
# js, reworked 19/07/2023

from typing import Tuple, List


def get_primes(n: int) -> List[int]:
    """
    :param n: an integer > 2
    :return: a list of all primes < n
    """
    ps = []
    for i in range(2, n):
        for p in ps:
            if i % p == 0:
                break
        else:
            ps.append(i)
    return ps


def primefactors(n: int, ps: List[int]) -> Tuple[List[int], int]:
    """
    :param n: a positive integer
    :param ps: a list of primes in ascending order
    :return: a list of exponents of first N prime factors of n
    and the remaining part of n
    """

    def aux(n, p):
        """
        :param n: an integer
        :param p: a prime number
        :return: exponent of p in n and remaining part of n
        """
        cnt = 0
        while n % p == 0:
            cnt += 1
            n //= p
        return n, cnt

    if n < 1:
        raise ValueError('n must be positive')
    result = []
    for p in ps:
        n, e = aux(n, p)
        result.append(e)
        if n == 1:
            break
    return result, n


def gcd(a: int, b: int) -> int:
    """
    :param a: an integer
    :param b: an integer
    :return: gcd of a and b
    """
    while b:
        a, b = b, a % b
    return a


def ext_gcd(a: int, b: int) -> Tuple[int, int, int]:
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
