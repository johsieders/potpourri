# 4.4.2022
# 6.10.2023


import time

import torch
from torch import tensor, zeros

from qbasics import log2, qtype, dev, int2bin, bin2int, perm


def permute(perm: list) -> list:
    """
    :param perm: permutation of n integers 0, ..., n-1
    :return: permutation of integers 0, ..., 2**n - 1
    """
    n = len(perm)
    bs = [int2bin(j, n) for j in range(2 ** n)]
    return [bin2int([b[i] for i in perm]) for b in bs]


def test_perf():
    p = list(range(15))
    q = p[10:] + p[5:10] + p[:5]

    start = time.perf_counter()
    for i in range(100):
        r = perm(q)
    stop = time.perf_counter()
    print(stop - start)

    start = time.perf_counter()
    for i in range(100):
        r = permute(q)
    stop = time.perf_counter()
    print(stop - start)


def apply_(Q: tensor, x: tensor, args: list) -> tensor:
    """
    :param Q: a tensor, shape = (2**k, 2**k)
    :param x: a vector, shape = (2**n); k <= n
    :param args: a list; len(args) = k
    :return: result of Q applied to the qbits of x given by args, so:

    X.shape = (2, 2)
    apply(X, x, [0]) applies X to qubit 0 of x
    apply(X, x, [1]) applies X to qubit 1 of x

    CX.shape = (4, 4)
    apply(CX, x, [0, 1]) applies CX to qbits 0 and 1 of x
    apply(CX, x, [1. 2]) applies CX to qbits 1 and 2 of x
    apply(CX, x, [0, 2]) applies CX to qbits 0 and 2 of x
    """

    K = Q.shape[0]
    N = x.shape[0]
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

    y = x.view(n * [2])  # a cube, shape = (2, 2, .., 2)
    result = zeros(N, dtype=qtype).view(n * [2])  # a cube, shape = (2, 2, .., 2)

    # run through all non-args qbits
    # The complexity of this loop is 2**(n-k) * 2**(2k) = 2**(n+k)
    # as opposed to 2**(2n), the complexity of the naive approach.
    for j in range(2 ** (n - k)):
        # update the non-arg part of idx according to j
        b = iter(int2bin(j, n - k))
        for i in non_args:
            idx[i] = next(b)
        z = y[idx].ravel()  # z is a vector, shape = (2**k)
        r = Q.mv(z)  # Q applied to z yields r, shape = (2**k)
        # each pass updates its own part of result.
        result[idx] = r.view(k * [2])

    return result.view(N)


def extend_(Q: tensor, args: list, n: int) -> tensor:
    """
    :param Q: a tensor, shape = (2**k, 2**k)
    :param args: a list of indices; len(args) = k
    :param n: number of qbits Q is to be extended to
    :return: an extended tensor T, shape = (2**n, 2**n) such that,
    if T = apply_P(Q, args, n), then
    T.mv(x) = apply_Q(Q, x, args)

    In other words:
    T acts on a vector psi exactly as Q would on the
    sub-vector of psi given by args.
    """

    K = Q.shape[0]
    N = 2 ** n
    k = log2(K)
    if (len(args) != k) or (k > n):
        raise ValueError

    result = torch.zeros(N, dtype=qtype, device=dev)
    B = torch.eye(N, dtype=qtype, device=dev)
    for j in range(N):
        a = apply_(Q, B[j], args)
        result[:, j] = a


# has been replaced with new versio of apply
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
    if 2 ** k != len(perm) or k > n:
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
