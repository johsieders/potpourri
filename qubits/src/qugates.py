# 4.4.2022
# 6.10.2023


import random
from cmath import exp, pi, sqrt

import torch
from torch import tensor, empty

from scratch.quantum import int2bin, perm2matrix, qtype, dev


def measure(psi: tensor) -> tensor:
    """
    :param psi: any state
    :return: a random measurement of the state
    """
    n = psi.size()[0]
    return random.choices(range(2 ** n), weights=psi ** 2)


def norm(x):
    """
    :param x: a vector x
    :return: the Euclidian norm of x
    """
    return sqrt(sum(x ** 2))


def tmm(A: tensor, B: tensor) -> tensor:
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


perm_I = [0, 1]  # identity
perm_X = [1, 0]  # NOT, Pauli-X
perm_CX = [0, 1, 3, 2]  # Controlled NOT; swap second bit if first bit is set
perm_CX2 = [0, 3, 2, 1]
perm_INC = [3, 0, 1, 2]  # increment
perm_REV = [3, 2, 1, 0]  # reverse
perm_SWAP = [0, 2, 1, 3]  # swap
perm_TOFF = [0, 1, 2, 3, 4, 5, 7, 6]  # Toffoli, swap third bit if first and second bits are set
perm_FRED = [0, 1, 2, 3, 4, 6, 5, 7]  # Fredkin

I = perm2matrix(perm_I)
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
