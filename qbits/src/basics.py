# 4.4.2022
# 18.11.2023


import random
from collections.abc import Callable

import torch
from torch import tensor, empty, zeros

qtype = torch.complex64
dev = torch.device('cpu')
# dev = torch.device('cuda')


def I(n: int) -> tensor:
    """
    :param n: number of qbits, N = 2 ** n
    :return: identity matrix of shape (N, N)
    """
    return torch.eye(2 ** n, dtype=qtype, device=dev)


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


def apply(Q: tensor, psi: tensor, args: list) -> tensor:
    """
    :param Q: a tensor, shape = (2**k, 2**k)
    :param psi: a vector, shape = (2**n); k <= n
    :param args: a list; len(args) = k
    :return: result of Q applied to the qbits of x given by args, so:

    X.shape = (2, 2), psi.shape = [4]
    apply(X, psi, [0]) applies X to qubit 0 of x
    apply(X, psi, [1]) applies X to qubit 1 of x

    CX.shape = (4, 4), psi.shape = [8]
    apply(CX, psi, [0, 1]) applies CX to qbits 0 and 1 of x
    apply(CX, psi, [1. 2]) applies CX to qbits 1 and 2 of x
    apply(CX, psi, [0, 2]) applies CX to qbits 0 and 2 of x
    """

    K = Q.shape[0]
    perm = matrix2perm(Q)
    N = psi.shape[0]
    n = log2(N)
    k = log2(K)
    if (len(args) != k) or (k > n):
        raise ValueError

    non_args = [i for i in range(n) if i not in args]

    # idx is the main element of the following code.
    # It is initialized to ":" overall.
    # The args-part of idx remains unchanged.
    # The non-args-part of idx runs through all non-arg qbits.
    idx = [slice(None)] * n

    y = psi.view(n * [2])  # a cube, shape = (2, 2, .., 2)
    result = zeros(N, dtype=qtype).view(n * [2])  # a cube, shape = (2, 2, .., 2)

    # run through all non-args qbits
    # The complexity of this loop is 2**(n-k) * 2**(2k) = 2**(n+k)
    # If Q is a permutation, then the complexity is 2**(n-k) * 2**k = 2**n
    # as opposed to 2**(2n), the complexity of the naive approach.
    for j in range(2 ** (n - k)):
        # update the non-arg part of idx according to j
        bs = iter(int2bin(j, n - k))
        for i in non_args:
            idx[i] = next(bs)
        z = y[idx].ravel()  # z is a vector, shape = (2**k)
        r = z[perm] if perm else Q.mv(z)  # Q applied to z yields r, shape = (2**k)
        # each pass updates its own part of result.
        result[idx] = r.view(k * [2])

    return result.view(N)


def curry(R: tensor, idxvals: list) -> tensor:
    """
    :param R: a tensor, shape = (2**n, 2**n)
    :param idxvals: a list of (idx, val)-pairs; len(idxvals) = l <= n
    0 <= idx < n; idxs ascending: idxvals[i][0] < idxvals[i+1][0]
    :return: an KxK submatrix Q of R.
    All rows and columns of R with non-matching values in one of the indices are dropped.

    Example:
    curry(CX, []) = CX
    curry(CX, [[0, 0], [1, 0]]) = [[1]]
    curry(TOFF, [[0, 0]]) = I(2)   # first bit is not set, so nothing happens
    curry(TOFF, [[0, 1]]) = CX     # first bit is set, second one is variable
    curry(TOFF, [[1, 1]]) = CX     # second bit is set, first one is variable
    """

    N = R.shape[0]
    n = log2(N)
    k = n - len(idxvals)
    K = 2 ** k

    # Construct the boolean mask
    B = tensor([int2bin(j, n) for j in range(N)])
    mask = torch.ones(N, dtype=torch.bool)
    for index, value in idxvals:
        mask &= (B[:, index] == value)

    # Find rows that meet all conditions
    Q = B[mask].tolist()
    sub_idx = [bin2int(Q[i]) for i in range(K)]
    return R[sub_idx][:, sub_idx]


def uncurry(Q: tensor, n: int, args: list) -> tensor:
    """
    :param Q: a tensor, shape = (2**k, 2**k)
    :param n: number of qbits, N = 2**n
    :param args: a list; len(args) = k
    :return: an NxN matrix R which applies Q to the qbits given by args
    So, Q (k qbits) is extended to R (n qbits)
    If n == k, R is just a clone of Q
    """
    B = I(n)
    R = B.clone()
    for j in range(2 ** n):
        R[j] = apply(Q, B[j], args)
    return R.T
