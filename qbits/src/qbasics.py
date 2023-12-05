# 4.4.2022
# 18.11.2023


import random
from collections.abc import Callable

import torch
from torch import tensor, empty, zeros

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


def basis2bin(psi: tensor) -> list:
    """
    :param psi: a basis state as tensor of size = (2**n, 1)
    :return: a binary index, e.g. [0,1, 1]
    Example:
    [1, 0, 0, 0, 0, 0, 0, 0].T -> [0, 0, 0]
    [0, 0, 0, 1, 0, 0, 0, 0].T -> [0, 1, 1]
    [0, 0, 0, 0, 0, 0, 0, 1].T -> [1, 1, 1]
    """
    n = log2(len(psi))
    i = psi.argmax()
    return int2bin(i, n)


############################################################
#            On Permutations                               #
############################################################
# let p = [p_0, p_1, ... p_n-1] be a permutation of [0, 1, ..., n-1]
# Permutation means: all p_i are distinct. A permutation p maps
# any list x of length n to another list y = p(x) of the same length.
# Let q = [q_0, q_1, ... q_n-1] be another permutation of [0, 1, ..., n-1]
# Then, the composition (p o q) can be explained as follows:
#
# p(x) = x[p] = [x[p[0]], x[p[1]], ..., x[p[n-1]]
#             = [x[p[i]] for i in range(n)]
#             = [x[i] for i in p]
# p o q = p(q) = [q[p[0]], q[p[1]], ..., q[p[n-1]]
#             = [q[p[i]] for i in range(n)]
#             = [q[i] for i in p]
# (p o q)(x)  = [x[(p o q)[0]], x[(p o q)[1]], ..., x[(p o q)[n-1]]]
#             = [q[p[i]] for i in range(n)]
#             = [x[q[i]] for i in p]
#             = [x[i] for i in (p o q)]
#
# the inverse permutation r of p is given by the relation
#     p[i] == j   <=>  r[j] = i
#
# This explains the functions compose(p, q) and inv_perm(p) below


def compose(p: list, q: list) -> list:
    """
    :param p: a permutation
    :param q: another permutation of the same length
    :return: the composition (p o q)
    """
    return [q[i] for i in p]


def inv_perm(p: list) -> list:
    """
    :param p: a permutation such as [1, 0, 2]
    :return: the inverse permutation r which is given by the relation
    p[i] == j   <=>  r[j] = i
    """
    result = [0] * len(p)
    for i, j in enumerate(p):
        result[j] = i
    return result


# Permuting the Dimension of Tensor
# Let x be a tensor with x.dim() = n
# Let i = [i[0], i[1], ..., i[n-1] be an index.
# Each index defines an entry of x via:
# [x[i[0]], x[i[1]], ...,x[i[n-1]]]
# Now, let p be a permutation of length n and q be its inverse.
# The function torch.permute(p) acts on x as follows:
# If
# y = x.permute(p),
# then
# [y[p[i[0]]], y[p[i[1]]], ...,y[p[i[n-1]]]] = [x[i[0]], x[i[1]], ...,x[i[n-1]]]
# see test.test_basics.test_permute for more details


def perm(p: list) -> list:
    """
    :param p: permutation of n integers 0, ..., n-1
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

    Let x be a basis state.
    Then x[tuple(perm(p))] is the permuted state.
    """
    n = len(p)
    x = torch.arange(2 ** n).view(n * [2])
    y = x.permute(inv_perm(p))
    return [a.item() for a in y.ravel()]


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
    result = zeros(n ** 2, dtype=qtype, device=dev).view(n, n)
    for i in range(n):
        result[i, perm[i]] = 1
    return result


def matrix2perm(M: tensor) -> list:
    """
    :param M: a matrix of size (n, n) permuting the columns of a state
    :return: permutation of n integers 0, ..., n-1 if M represents a permutation,
    None otherwise. Example:
    M = [[0, 1, 0],
    [1, 0, 0],
    [0, 0, 1]]
    yields
    perm = [1, 0, 2]
    """
    n = M.shape[0]
    if M.shape[1] != n:
        raise ValueError

    result = []
    for i in range(n):
        for j in range(n):
            if torch.isclose(M[i, j], torch.tensor(1, dtype=qtype, device=dev)):
                result.append(j)
    return result if len(result) == n else None


def measure(psi: tensor) -> tensor:
    """
    :param psi: any state
    :return: a random measurement of the state
    """
    n = psi.size()[0]
    return random.choices(range(2 ** n), weights=psi ** 2)


def tmm(*A: tensor) -> tensor:
    """
    :param A: a list of tensors
    :return: tensor product of all tensors
    """
    if len(A) == 1:
        return A[0].clone()
    else:
        result = _tmm(A[0], A[1])
        for i in range(2, len(A)):
            result = tmm(result, A[i])

        return result


def mm(*A: tensor) -> tensor:
    """
    :param A: a list of tensors
    :return: matrix product of all tensors
    """
    if len(A) == 1:
        return A[0].clone()
    else:
        result = A[0].mm(A[1])
        for i in range(2, len(A)):
            result = result.mm(A[i])

        return result


def _tmm(A: tensor, B: tensor) -> tensor:
    """
    :param A: a tensor
    :param B: another tensor
    :return: R = tensor product of A and B; size(R) = (m_A * m_B, n_A * n_B)
    result[x, y] = A[x] * B[y]
    where x and y are multi-dim indices of A and B
    """
    m_A, n_A = A.size()
    m_B, n_B = B.size()
    result = empty(m_A * m_B, n_A * n_B, dtype=A.dtype, device=dev)
    for i in range(m_A):
        for j in range(n_A):
            result[i * m_B:(i + 1) * m_B, j * n_B:(j + 1) * n_B] = A[i, j] * B
    return result


def tmv(A: tensor, psi: tensor) -> tensor:
    return tmm(A, psi.view(-1, 1))


def tpow(A, n):
    if n == 0:
        return torch.eye(A.size()[0], dtype=qtype, device=dev)
    elif n == 1:
        return A.clone()
    else:
        n, r = divmod(n, 2)
        B = tpow(A, n)
        C = tmm(B, B)
        return C if r == 0 else tmm(A, C)
