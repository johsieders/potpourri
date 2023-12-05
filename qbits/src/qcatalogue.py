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

from cmath import exp, pi, sqrt

import torch
from torch import tensor

from basics import I, qtype, dev, int2bin, perm2matrix, tmm


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

BELL = CX.mm(tmm(H, I(1)))
