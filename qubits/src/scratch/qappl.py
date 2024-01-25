# 4.4.2022
# 18.11.2023


import torch
from torch import tensor, zeros

from qbasics import bin2int, int2bin, log2, matrix2perm, qtype
from qcat import I


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
