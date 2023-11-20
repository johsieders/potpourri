# 4.4.2022
# 18.11.2023


from collections.abc import Callable

import torch
from torch import tensor, zeros

qtype = torch.complex64
dev = torch.device('cpu')
# dev = torch.device('cuda')


def log2(n):
    """
    :param n: an integer >= 0
    :return: (number of binary digits of n) - 1
    So: log2(1) = 0, log2(2) = 1, log2(3) = 1, log2(4) = 2
    """
    if n < 1:
        raise ValueError
    result = -1
    while n > 0:
        n >>= 1
        result += 1
    return result


def int2bin(i: int, n: int = 0) -> list:
    """
    :param i: an integer index >= 0
    :param n: length of list
    :return: binary index of i as a list of length max(n, log2(i))
    6, 2 -> [1, 1, 0]
    6, 3 -> [1, 1, 0]
    6, 4 -> [0, 1, 1, 0]
    """
    return [int(c) for c in bin(i)[2:].rjust(n, '0')]


def bin2int(b: list) -> int:
    """
    :param b: a binary index, e.g. [0,1,0,0,1]
    :return: corresponding integer index, e.g.
    [0,1,0,0,1] -> 9
    """
    result = 0
    for digit in b:
        result = (result << 1) | digit
    return result


def bin2basis(b: list) -> tensor:
    """
    :param b: a binary index, e.g. [0,1, 1]
    :return: corresponding basis state as tensor of size = (2**n, 1).
    Example:
    [0, 0, 0] -> [1, 0, 0, 0, 0, 0, 0, 0].T
    [0, 1, 1] -> [0, 0, 0, 1, 0, 0, 0, 0].T
    [1, 1, 1] -> [0, 0, 0, 0, 0, 0, 0, 1].T
    """
    result = zeros(2 ** len(b), dtype=torch.int, device=dev)
    result[bin2int(b)] = 1
    return result


def basis2bin(s: tensor, n: int) -> list:
    """
    todo: n = log2(len(s))
    :param s: a basis state as tensor of size = (2**n, 1)
    :param n:
    :return: a binary index, e.g. [0,1, 1]
    Example:
    [1, 0, 0, 0, 0, 0, 0, 0].T -> [0, 0, 0]
    [0, 0, 0, 1, 0, 0, 0, 0].T -> [0, 1, 1]
    [0, 0, 0, 0, 0, 0, 0, 1].T -> [1, 1, 1]
    """
    i = s.argmax()
    return int2bin(i, n)


def inverse_perm(perm: list) -> list:
    """
    :param perm: a permutation such as [1, 0, 2]
    :return: the inverse permutation
    """
    result = [0] * len(perm)
    for i, j in enumerate(perm):
        result[j] = i
    return result


def compose(p: list, q: list) -> list:
    """
    :param p: a permutation
    :param q: another permutation of same length
    :return: the compostion of p and q
    """
    return [q[i] for i in p]

def permute(perm: list) -> list:
    """
    :param perm: permutation of n integers 0, ..., n-1
    :return: permutation of integers 0, ..., 2**n - 1
    example: seq = [1, 0, 2] swaps columns 0 and 1.
    This yields [0, 1, 4, 5, 2, 3, 6, 7]
    0: [0, 0, 0]
    1: [0, 0, 1]
    4: [1, 0, 0]
    5: [1, 0, 1]
    2: [0, 1, 0]
    3: [0, 1, 1]
    6: [1, 1, 0]
    7: [1, 1, 1]

    Let x be a basis state, then permute(seq) permutes the columns of x.
    Then x[permute(seq)] is the permuted state.
    """
    n = len(perm)
    bs = [int2bin(j, n) for j in range(2 ** n)]
    return [bin2int([b[i] for i in perm]) for b in bs]


def extend_perm(perm: list, args: list, n: int) -> list:
    """
    :param perm: a permutation, len(perm) = 2**k
    :param args: a list of args, len(args) = k, args[i] < n
    :param n: total number variables
    :return: a perm extended to a permutation of length 2**n
    This is what happens: The permutation perm of length 2**k
    is extended by permuting args according to perm
    and leaving all other indices in place. So,
    perm = perm_CX = [0, 1, 3, 2], args = [1, 2], and n = 3 yields
    [0, 1, 3, 2, 4, 5, 7, 6]
    """

    k = len(args)
    if 2 ** k != len(perm):
        raise ValueError

    result = []
    for j in range(2 ** n):
        b = int2bin(j, n)
        b_args = [b[i] for i in args]
        j_args = bin2int(b_args)
        j_perm = perm[j_args]
        b_perm = int2bin(j_perm, k)
        for i in range(k):
            b[args[i]] = b_perm[i]
        result.append(bin2int(b))

    return result


def perm2matrix(perm: list) -> tensor:
    """
    :param perm: permutation of n integers 0, ..., n-1
    :return: matrix permuting the columns of a state according to perm
    example: perm = [1, 0, 2] swaps columns 0 and 1.
    This yields the matrix
    [[0, 1, 0],
    [1, 0, 0],
    [0, 0, 1]]
    """
    n = len(perm)
    result = zeros(n ** 2, dtype=qtype, device=dev).view(n, -1)
    for i in range(n):
        result[i, perm[i]] = 1
    return result


def matrix2perm(M: tensor) -> list:
    """
    :param M: a matrix of size (n, n) permuting the columns of a state
    :return: permutation of n integers 0, ..., n-1
    example: M = [[0, 1, 0],
    [1, 0, 0],
    [0, 0, 1]]
    yields perm = [1, 0, 2]
    """
    n = M.size()[0]
    result = []
    for i in range(n):
        for j in range(n):
            if M[i, j] == 1:
                result.append(j)
    return result


def one_at(i: int) -> Callable:
    """
    :param i: an integer
    :return: a function f: list -> int
    f accepts a number j given as list of binaries.
    f returns 1 if i == j, 0 otherwise.
    """

    def aux(x: list) -> int:
        j = bin2int(x)
        return 1 if i == j else 0

    return aux
