# trying to understand primes
# js, reworked 19/07/2023
# checked 07/01/2024

from typing import Tuple, List, Sequence


def is_prime(n: int) -> bool:
    # Basic prime checking algorithm
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def get_primes(n: int) -> list:
    """
    :param n: an integer > 2
    :return: a list of all primes < n
    """
    if n <= 2:
        raise ValueError(f"n must be greater than 2")
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
    :param ps: an Iterator of primes in ascending order
    :return: a list of exponents of first N prime factors of n
    and the remaining part of n
    """

    def aux(n: int, p: int) -> Tuple[int, int]:
        """
        :param n: an integer
        :param p: a prime number
        :return: exponent e of p in n and remaining factor r, so:
        n = r * p ** e
        examples:
        aux(28, 2) -> 2, 7
        aux(28, 5) -> 0, 28
        aux(28, 7) -> 1, 4
        """
        e = 0  # exponent
        r = n  # remaining factor
        while r % p == 0:
            e += 1
            r //= p
        return e, r

    if n < 1:
        raise ValueError('n must be positive')
    result = []
    for p in (q for q in ps if q <= n):
        e, n = aux(n, p)
        result.append(e)
        if n == 1:
            break
    return result, n


def gcd(a, b):
    """
    :param a: an element of an Euclidian ring
    :param b: another element of an Euclidian ring
    :return: gcd of a and b
    """
    while b:
        a, b = b, a % b
    return a


def ext_gcd(a, b) -> tuple:
    """
    :param a: an element of an Euclidian ring
    :param b: another element of an Euclidian ring
    :return: three elements g, s, t such that
            g = gcd(a, b) and
            g = a * s + b * t
    """
    s, u = 1, 0
    t, v = 0, 1

    while b:
        q, r = divmod(a, b)
        a, b = b, r
        s, u = u, s - q * u
        t, v = v, t - q * v
    return a, s, t


def ext_gcd_rec(a, b, s=1, u=0, t=0, v=1) -> tuple:
    """
    :param a: an element of an Euclidian ring
    :param b: another element of an Euclidian ring
    :return: three elements g, s, t such that
            g = gcd(a, b) and
            g = a * s + b * t
    """
    if b == 0:
        return a, s, t
    else:
        q, r = divmod(a, b)
        return ext_gcd_rec(b, r, u, s - q * u, v, t - q * v)


def inv(a, m):
    """
    :param a: an element of an Euclidian ring
    :param m: another element of an Euclidian ring
    :return: inverse of a modulo m
    The inverse exists iff gcd(a, m) = 1
    Here is how it works:
    a * s + b * t = 1
    => a * s = 1 - b * t
    => a * s = 1 mod b
    """
    g, s, t = ext_gcd(a, m)
    if g != 1:  # g must be 1
        raise ValueError("No inverse for %d modulo %d" % (a, m))
    return s % m


def chinese_remainder_2(a: list, m: list):
    """
    :param a: list of two elements of an Euclidian ring
    :param m: list of two coprime two elements of an Euclidian ring
    :return: x such that x = a[i] mod m[i] for i = 0, 1
    Here is why it works:

    ext_gcd(m0, m1) -> (1, s, t), so:
    m0 * s + m1 * t = 1
    => m1 * t = 1 - m0 * s
    x := a0 * m1 * t + a1 * m0 * s  (this is the trick)
    = a0 * (1 - m0 * s) + a1 * m0 * s
    = a0 + m0 * (a1 * s - a0 * s)
    = a0 mod m0
    """
    g, s, t = ext_gcd(m[0], m[1])
    if g != 1:
        raise ValueError("No inverse for %d modulo %d" % (m[0], m[1]))
    return a[0] * m[1] * t + a[1] * m[0] * s


def chinese_remainder_(a: list, primes: list):
    """
    :param a: list of elements of an Euclidian ring, len(a) >= 2
    :param primes: list of coprime elements of an Euclidian ring, often primes
    :return: x such that x = a[i] mod m[i] for all i

    Here is why it works:
    The for-loop produces x1, x2 ... such that

    x1 = a0 mod m0
    x1 = a1 mod m1

    x2 = x1 mod m0 * m1
    x2 = a2 mod m2

    This implies by simple calculation:
    x2 = a0 mod m0
    x2 = a1 mod m1
    """

    if len(a) != len(primes):
        raise ValueError("a and primes must have the same length")

    N = 1
    for i in range(len(a)):
        N *= primes[i]

    m = 1
    x = a[0]
    for i in range(1, len(a)):
        m *= primes[i - 1]
        x = chinese_remainder_2([x, a[i]], [m, primes[i]])

    return x % N


def chinese_remainder(a: Sequence, primes: Sequence):
    """
    :param a: list of elements of an Euclidian ring
    :param primes: list of coprime elements of an Euclidian ring, often primes
    :return: x such that x = a[i] mod m[i] for all i

    Here is how it works:

    qi = N // pi (all i), so
    (pi, qj) = 1 if i == j, else 0

    xi = inv(qi, pi), so
    xi * qi = 1 mod pj if i == j, else 0
    ai * xi * qi = ai mod pj if i == j, else 0

    and therefore the solution is:

    x = sum_i(ai * xi * qi)
    """

    if len(a) != len(primes):
        raise ValueError("a and primes must have the same length")

    n = len(a)
    N = 1
    for i in range(n):
        N *= primes[i]

    qs = [N // p for p in primes]
    xs = [inv(qs[i], primes[i]) for i in range(n)]

    x = 0
    for i in range(n):
        x += a[i] * xs[i] * qs[i]
    return x % N
