# j.siedersleben
# fasttrack to professional programming
# lesson 1: warm up
# 15.11.2020

from typing import List


def powerOf2(n: int) -> bool:
    """
    :param n: an integer > = 1
    :return: true if n is a power of two
    """
    return not n & (n - 1)


def log2(n):
    """
    :param n: an integer >= 0
    :return: (number of binary digits of n) - 1
    So: log2(1) = 0, log2(2) = 1, log2(3) = 1
    """
    if n < 1:
        raise ValueError
    result = -1
    while n > 0:
        n >>= 1
        result += 1
    return result


def intersection(u: (int, int), v: (int, int)) -> (int, int):
    """
    :param u: half open interval (u0, u1)
    :param v: half open interval (v0, v1)
    :return: intersection of u and v
    Convention: an interval u is empty iff u[0] >= u[1]
    """
    return max(u[0], v[0]), min(u[1], v[1])


def faculty(n: int) -> int:
    """
    :param n: integer
    :return:  nth-faculty
    standard solution
    """
    if n < 0:
        raise ValueError
    else:
        result = 1
        for i in range(1, n + 1):
            result *= i
        return result


def faculty1(n: int) -> int:
    """
    :param n: integer
    :return:  nth-faculty
    recursive solution
    """
    if n < 0:
        raise ValueError
    elif n <= 1:
        return 1
    else:
        return n * faculty1(n - 1)


def fibo1(n: int) -> int:
    """
    :param n: integer >= 0
    :return: n-th Fibonacci number
    naive solution
    """
    if n < 0:
        raise ValueError
    elif n == 0:
        return 0
    else:
        result = [0, 1]
        for _ in range(2, n + 1):
            result.append(result[-2] + result[-1])
        return result[-1]


def fibo(n: int) -> int:
    """
    :param n: integer >= 0
    :return: n-th Fibonacci number
    standard solution
    """
    if n < 0:
        raise ValueError
    elif n == 0:
        return 0
    else:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b


def fibo2(n: int) -> int:
    """
    :param n: integer >= 0
    :return: n-th Fibonacci number
    """
    # recursive programming, cool but slow
    if n < 0:
        raise ValueError
    elif n <= 1:
        return n
    else:
        return fibo2(n - 2) + fibo2(n - 1)


def gcd(a: int, b: int) -> int:
    """
    :param a: integer
    :param b: integer
    :return: greatest common divisor of a and b
    standard solution
    """
    while b != 0:
        a, b = b, a % b
    return a


def gcd1(a, b):
    """
    :param a: integer
    :param b: integer
    :return: greatest common divisor of a and b
    recursive solution
    """
    return a if b == 0 \
        else gcd1(b, a % b)


def exp_coeff(n: int, x: float) -> float:
    """
    :param n: integer >= 0
    :param x: real
    :return: x**n / n!  (nth coefficient of taylor series of exp_taylor)
    standard solution
    """
    if n < 0:
        raise ValueError

    result = 1
    for k in range(1, n + 1):
        result = result * x / k

    return result


def exp_coeff1(n: int, x: float) -> float:
    """
    :param n: integer >= 0
    :param x: float
    :return: x**n / n!  (nth coefficient of taylor series of exp_taylor)
    recursive solution
    """
    if n < 0:
        raise ValueError

    return 1 if n == 1 \
        else exp_coeff1(n - 1, x) * x / n


def reverse0(xs: list) -> list:
    """
    :param xs: a list
    :return: a new list containing xs in reversed order
    """
    return xs[::-1]


def reverse1(xs: list) -> list:
    """
    :param xs: a list
    :return: a new list containing xs in reversed order
    same as reverse0, recursive solution
    This produces O(n) new lists!
    """
    return list(xs) if len(xs) <= 1 \
        else [xs[-1]] + reverse1(xs[1: -1]) + [xs[0]]


def reverse(xs: list) -> None:
    """
    :param xs: a list
    :return: None
    this function reverses the order of xs
    standard solution
    """
    m = len(xs) // 2
    for i in range(m):
        xs[i], xs[-1 - i] = xs[-1 - i], xs[i]


def reverse2(xs: list) -> None:
    """
    :param xs: a list
    :return: None
    same as reverse, recursive solution
    Functional programming should have no side effects.
    This is why this solution is awkward
    """

    def rev(i, j):
        if i < j:
            xs[i], xs[j] = xs[j], xs[i]
            rev(i + 1, j - 1)

    rev(0, len(xs) - 1)


def normstring(s: str) -> str:
    """
    :param s: a string
    :return: keeps ascii letters only and converts s to lower case
    """
    import string
    result = ''
    for c in s:
        if c in string.ascii_letters:
            result += str.lower(c)
    return result


def palindrome1(xs: str) -> bool:
    """
    :param xs: string
    :return: true if xs is a palindrome
    using Python's reverse which only works on lists
    """
    ys = list(normstring(xs))
    zs = list(ys)
    zs.reverse()
    return ys == zs


def palindrome(xs: str) -> bool:
    """
    :param xs: string
    :return: true if xs is a palindrome
    standard solution
    """
    ys = normstring(xs)
    m = len(ys) // 2
    for i in range(m):
        if ys[i] != ys[-1 - i]:
            return False
    return True


def palindrome2(xs: str) -> bool:
    """
    :param xs: string
    :return: true if xs is a palindrome
    recursive solution, normstring only called once
    """

    def pal(ys):
        return True if len(ys) <= 1 \
            else ys[0] == ys[-1] and pal(ys[1:-1])

    return pal(normstring(xs))


def romans() -> List[str]:
    """
    :return: romans nums from 1 to 4999
    """
    digits1 = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX']
    digits2 = ['', 'X', 'XX', 'XXX', 'XL', 'L', 'LX', 'LXX', 'LXXX', 'XC']
    digits3 = ['', 'C', 'CC', 'CCC', 'CD', 'D', 'DC', 'DCC', 'DCCC', 'CM']
    digits4 = ['', 'M', 'MM', 'MMM', 'MMMM']

    result = []
    for d4 in digits4:
        for d3 in digits3:
            for d2 in digits2:
                for d1 in digits1:
                    result.append(d4 + d3 + d2 + d1)
    return result


def teile(betrag: int) -> (int, List[int]):
    EUROS = (20000, 10000, 5000, 2000, 1000, 500, 200, 100, 50, 20, 10, 5, 2, 1)
    result = [0] * len(EUROS)
    summe = 0
    for i, euro in enumerate(EUROS):
        result[i], betrag = divmod(betrag, euro)
        summe = result[i] * euro + summe
        if betrag <= 0:
            return result, summe


def zeugnisnote(proben: List[float],
                kurzproben: List[float],
                stegreifaufgaben: List[float]) -> float:
    """
    :param proben: Noten der Proben
    :param kurzproben: Noten der Kurzproben
    :param stegreifaufgaben: Noten der Stegreifaufgaben
    :return: resultierende Gesamtnote
    """

    note = (3 * sum(proben) + 2 * sum(kurzproben) + sum(stegreifaufgaben)) / \
           (3 * len(proben) + 2 * len(kurzproben) + len(stegreifaufgaben))

    return note


def pascal(n):
    """
    :param n: an integer >= 0
    :return: coefficients of (a + b) ** n
    """
    triangle = [[1]]  # that's all for n = 0
    for k in range(1, n + 1):
        triangle.append([1])  # append a new line starting with 1
        for i in range(k - 1):  # apply the rule for computing the pascal triangle
            triangle[k].append(triangle[k - 1][i] + triangle[k - 1][i + 1])
        triangle[k].append(1)  # append final 1

    return triangle[n]  # return last line


def pascal1(n):
    """
    :param n: an integer >= 0
    :return: coefficients of (a + b) ** n
    recursive implementation
    """
    if n == 0:
        return [1]

    else:
        previous_line = pascal1(n - 1)
        this_line = [1]  # set first coefficient = 1
        for i in range(n - 1):  # apply the rule for computing the pascal triangle
            this_line.append(previous_line[i] + previous_line[i + 1])
        this_line.append(1)  # append last coefficient = 1

    return this_line
