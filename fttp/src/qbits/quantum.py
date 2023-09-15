# 4.4.2022

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


# [0, 0 > = [0 > x [0 > = [1, 0, 0, 0]
# quantum matrix: tensor of size (N, N); A, B, C, to be applied to states: A.mm(psi) -> phi
# quantum gate: special quantum matrices, such as I, X, CX, CZ, SWAP
# quantum program: list of quantum matrices, P, Q, R, or BELL, TELE, DEUTSCH, DENSE


import random
from cmath import exp, pi, sqrt
from collections.abc import Callable

import torch
from torch import tensor, empty, zeros

qtype = torch.complex64
dev = torch.device('cpu')


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


def bin2int(x: list) -> int:
    """
    :param x: a binary index, e.g. [0,1,0,0,1]
    :return: corresponding integer index, e.g.
    [0,1,0,0,1] -> 9
    """
    result = 0
    for digit in x:
        result = (result << 1) | digit
    return result


def bin2basis(x: list) -> tensor:
    """
    :param x: a binary index, e.g. [0,1, 1]
    :return: corresponding basis state as tensor of size = (2**n, 1).
    Example:
    [0, 0, 0] -> [1, 0, 0, 0, 0, 0, 0, 0].T
    [0, 1, 1] -> [0, 0, 0, 1, 0, 0, 0, 0].T
    [1, 1, 1] -> [0, 0, 0, 0, 0, 0, 0, 1].T
    """
    result = zeros(2 ** len(x), dtype=qtype, device=dev).view(-1, 1)
    result[bin2int(x)] = 1
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
    i = psi.argmax()
    return int2bin(i)


def measure(psi: tensor) -> tensor:
    """
    :param psi: any state
    :return: a random measurement of the state
    """
    n = psi.size()[0]
    return random.choices(range(2 ** n), weights=psi ** 2)


def permute(perm):
    """
    :param perm: permutation of n integers 0, .., n-1
    :return: permutation of integers 0, .., 2**n - 1
    example: perm = [1, 0, 2] swaps columns 0 and 1.
    This yields [0, 1, 4, 5, 2, 3, 6, 7]
    0: [0, 0, 0]
    1: [0, 0, 1]
    4: [1, 0, 0]
    5: [1, 0, 1]
    2: [0, 1, 0]
    3: [0, 1, 1]
    6: [1, 1, 0]
    7: [1, 1, 1]
    """
    n = len(perm)
    binaries = [int2bin(j, n) for j in range(2 ** n)]
    return [bin2int([x[i] for i in perm]) for x in binaries]


def one_at(i: int) -> Callable:
    def aux(x: list) -> int:
        j = bin2int(x)
        return 1 if i == j else 0

    return aux


def tmm(A: tensor, B: tensor) -> tensor:
    """
    :param A: a tensor
    :param B: a tensor
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


def apply(Q: list, psi: tensor) -> tensor:
    """
    :param Q: a quantum program give as list of tensors, size = (2**n, 2**n)
    :param x: a vector of length 2**n
    :return: the result of program Q, a vector of length 2**n
    """
    result = Q[0].mm(psi.view(-1, 1))
    for q in Q[1:]:
        result = q.mm(result)
    return result


def U(f, n):
    """
    :param f: a binary function of n binary variables
    :param n: the number n >= 2, N = 2 ** n
    :return: the unitary (2*N x 2*N) matrix U(f)
    """
    N = 2 ** n
    U = torch.eye(2 * N, dtype=qtype, device=dev)
    for i in range(N):
        if f(int2bin(i, n)):
            U[2 * i: 2 * i + 2, 2 * i: 2 * i + 2] = X
    return U


# identity
I = tensor([[1, 0],
            [0, 1]], dtype=qtype, device=dev)

# NOT, Pauli-X
X = tensor([[0, 1],
            [1, 0]], dtype=qtype, device=dev)

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

# Controlled NOT
CX = tensor([[1, 0, 0, 0],
             [0, 1, 0, 0],
             [0, 0, 0, 1],
             [0, 0, 1, 0]], dtype=qtype, device=dev)

# Controlled NOT  = H2 * CX * H2
CX2 = tensor([[1, 0, 0, 0],
              [0, 0, 0, 1],
              [0, 0, 1, 0],
              [0, 1, 0, 0]], dtype=qtype, device=dev)

# controlled Z
CZ = tensor([[1, 0, 0, 0],
             [0, 1, 0, 0],
             [0, 0, 1, 0],
             [0, 0, 0, -1]], dtype=qtype, device=dev)

# SWAP = CX * CX2 * CX
SWAP = tensor([[1, 0, 0, 0],
               [0, 0, 1, 0],
               [0, 1, 0, 0],
               [0, 0, 0, 1]], dtype=qtype, device=dev)

# REV = CX * (tmm(X, I) * CX
REV = tensor([[0, 0, 0, 1],
              [0, 0, 1, 0],
              [0, 1, 0, 0],
              [1, 0, 0, 0]], dtype=qtype, device=dev)

# INC = CX2 * REV
INC = tensor([[0, 0, 0, 1],
              [1, 0, 0, 0],
              [0, 1, 0, 0],
              [0, 0, 1, 0]], dtype=qtype, device=dev)

# Toffoli
TOFF = tensor([[1, 0, 0, 0, 0, 0, 0, 0],
               [0, 1, 0, 0, 0, 0, 0, 0],
               [0, 0, 1, 0, 0, 0, 0, 0],
               [0, 0, 0, 1, 0, 0, 0, 0],
               [0, 0, 0, 0, 1, 0, 0, 0],
               [0, 0, 0, 0, 0, 1, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 1],
               [0, 0, 0, 0, 0, 0, 1, 0]], dtype=qtype, device=dev)

A = tmm(X, I)
B = tmm(X, I).mm(CX)
C = CX.mm(tmm(X, I))
D = CX.mm(tmm(X, I)).mm(CX)

H2 = tmm(H, H)
K = H2.mm(CX).mm(H2)  # CNOT2
L = CX.mm(CX2).mm(CX)

M = tmm(I, CX).mm(tmm(CX, I))
N = tmm(CX, CX)

P = tmm(X, I).mm(CX)
Q = tmm(X, I).mm(tmm(I, X))
R = Q.mm(CX)

if __name__ == '__main__':
    print(A.real)
    print(B.real)
    print(C.real)
    print(D.real)
    print(K.real)

    print(CX2.real)
    print(REV.real)
    print(CX2.mm(REV).real)
    # print(L.real)
    # print(M.real)
    # print(N.real)
    # print(R.real)
