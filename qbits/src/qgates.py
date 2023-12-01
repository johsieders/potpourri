# 4.4.2022
# 18.11.2023


# Quantum Computing with Pytorch

# Conventions
# state (of n qbits): tensor; size = (2**n,); psi, phi, chi
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
# quantum matrix: tensor of size (N, N); A, B, C, to be applied to states: A.mv(psi) -> phi
# quantum gate: special quantum matrices, such as I, X, CX, CZ, SWAP
# quantum program (P, Q, R): a quantum matrix that serves a special purpose such as
# BELL, TELE, DEUTSCH, DENSE

# representation of |psi> as a tensor
# |psi> =  tensor([a0, a1, a2, a3, a4, a5, a6, a7]).T
# |psi> =  a0 * |0, 0, 0> + a1 * |0, 0, 1> + a2 * |0, 1, 0> + a3 * |0, 1, 1> +
#           a4 * |1, 0, 0> + a5 * |1, 0, 1> + a6 * |1, 1, 0> + a7 * |1, 1, 1>
# sqrt(psi**2) = 1
# Setting qsi = psi.view(2, 2, 2) we get
# sqrt(qsi[a, b, c]**2) = P[X=a, Y=b, Z=c]

import random
from cmath import exp, pi, sqrt

import torch
from torch import tensor, empty, zeros

from basics import log2, int2bin, dev, qtype, matrix2perm, perm2matrix


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


def U(f, n):
    """
    :param f: a binary function of n binary variables
    :param n: the number n >= 2, N = 2 ** n
    :return: the unitary (2*N x 2*N) matrix U(f)
    U(f) includes N times X^0 = I and N times X^1 = X along the diagonal with the exponent being f(x).
    """
    N = 2 ** n
    U = torch.eye(2 * N, dtype=qtype, device=dev)
    for i in range(N):
        if f(int2bin(i, n)):
            U[2 * i: 2 * i + 2, 2 * i: 2 * i + 2] = X
    return U


def I(n: int) -> tensor:
    """
    :param n: number of qbits, N = 2 ** n
    :return: identity matrix of shape (N, N)
    """
    return torch.eye(2 ** n, dtype=qtype, device=dev)


perm_X = [1, 0]  # NOT, Pauli-X
perm_CX = [0, 1, 3, 2]  # Controlled NOT; swap second bit if first bit is set
perm_CX2 = [0, 3, 2, 1]
perm_INC = [3, 0, 1, 2]  # increment
perm_REV = [3, 2, 1, 0]  # reverse
perm_SWAP = [0, 2, 1, 3]  # swap
perm_TOFF = [0, 1, 2, 3, 4, 5, 7, 6]  # Toffoli, swap third bit if first and second bits are set
perm_FRED = [0, 1, 2, 3, 4, 6, 5, 7]  # Fredkin

X = perm2matrix(perm_X)
CX = perm2matrix(perm_CX)
CX2 = perm2matrix(perm_CX2)  # H2 * CX * H2
REV = perm2matrix(perm_REV)  # CX * (X x I) * CX
INC = perm2matrix(perm_INC)  # CX2 * REV
SWAP = perm2matrix(perm_SWAP)  # CX * CX2 * CX
TOFF = perm2matrix(perm_TOFF)
FRED = perm2matrix(perm_FRED)

# Pauli-Y
Y = tensor([[0, -1j],
            [1j, 0]], dtype=qtype, device=dev)

# Pauli-Z
Z = tensor([[1, 0],
            [0, -1]], dtype=qtype, device=dev)

# Phase
S = tensor([[1, 0],
            [0, 1j]], dtype=qtype, device=dev)

# Hadamard
H = 1 / sqrt(2) * tensor([[1, 1],
                          [1, -1]], dtype=qtype, device=dev)
# pi/8; T ** 8 = 1
T = tensor([[1, 0],
            [0, exp(2j * pi / 8)]], device=dev)


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


def qgate(Q, n, args) -> tensor:
    """
    :param Q: a tensor, shape = (2**k, 2**k)
    :param n: number of qbits, N = 2**n
    :param args: a list; len(args) = k
    :return: an NxN matrix which applies Q to the qbits given by args
    If n == k, the result is just a clone of Q
    """
    B = I(n)
    R = B.clone()
    for j in range(2 ** n):
        R[j] = apply(Q, B[j], args)
    return R.T
