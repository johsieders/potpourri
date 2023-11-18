# 4.4.2022
# 18.11.2023

# Quantum Computing with Pytorch

# Conventions
# state: tensor; size = (2**n, 1); psi, phi, xi
# basis state: a state with exactly one element = 1, all others = 0
# binary index: list of n binaries; len = n; x, y, z
# integer index: int < N = 2**n; i, j, k
# binary: int < 2; a, b, c
# For each n, there are 2**n basis states, binary indices and integer indices.
# The table for n = 3, N = 8
#
# integer indices   Dirac notation          basis states
# 0                 [0, 0, 0 >              [1, 0, 0, 0, 0, 0, 0, 0]
# 1                 [0, 0, 1 >              [0, 1, 0, 0, 0, 0, 0, 0]
# 2                 [0, 1, 0 >              [0, 0, 1, 0, 0, 0, 0, 0]
# 3                 [0, 1, 1 >              [0, 0, 0, 1, 0, 0, 0, 0]
# 4                 [1, 0, 0 >              [0, 0, 0, 0, 1, 0, 0, 0]
# 5                 [1, 0, 1 >              [0, 0, 0, 0, 0, 1, 0, 0]
# 6                 [1, 1, 0 >              [0, 0, 0, 0, 0, 0, 1, 0]
# 7                 [1, 1, 1 >              [0, 0, 0, 0, 0, 0, 0, 1]


# [0, 0 >  =  [0 > X [0 >  =  [1, 0, 0, 0]
# quantum matrix: tensor of size (N, N); A, B, C, to be applied to states: A.mm(psi) -> phi
# quantum gate: special quantum matrices, such as I, X, CX, CZ, SWAP
# quantum program: list of quantum matrices, P, Q, R, or BELL, TELE, DEUTSCH, DENSE

# representation of |psi> as a tensor
# |psi> =  tensor([a0, a1, a2, a3, a4, a5, a6, a7]).T
# |psi> =  a0 * |0, 0, 0> + a1 * |0, 0, 1> + a2 * |0, 1, 0> + a3 * |0, 1, 1> +
#           a4 * |1, 0, 0> + a5 * |1, 0, 1> + a6 * |1, 1, 0> + a7 * |1, 1, 1>
# sqrt(psi**2) = 1
# Setting qsi = psi.view(2, 2, 2) we get
# sqrt(qsi[a, b, c]**2) = P[X=a, Y=b, Z=c]

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


def permute_x(perm: list, args: list, n: int) -> list:
    """
    :param perm: a permutation, len(perm) = k < n
    :param args: a list of args, len(args) = k, args[i] < n
    :param n: total number variables
    :return: a permutation of length 2**n
    This is what happens: The permutation perm of length k
    is extended to a permutation perm_x of length n by permuting args
    according to perm, by and leaving all other indices in place. So,
    perm = [2, 1, 0], args = [0, 2, 3], and n = 4 yields
    perm_x = [3, 1, 2, 0].
    The function permute is then applied to perm_x
    """
    k = len(perm)
    if len(args) != k or k > n:
        raise ValueError

    perm_x = list(range(n))
    perm_y = perm_x.copy()
    for i in range(k):
        perm_x[args[i]] = perm_y[args[perm[i]]]

    return permute(perm_x)


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
