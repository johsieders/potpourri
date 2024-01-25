# 4.4.2022
# 6.10.2023

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

from cmath import exp, pi, sqrt
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
    result = zeros(2 ** len(b), dtype=qtype, device=dev)
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


def inverse_permutation(perm: list) -> list:
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
    according to perm and leaving all other indices in place. So,
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


def apply(Q: tensor, x: tensor, args: list) -> tensor:
    """
    :param Q: a tensor, shape = (2**k, 2**k)
    :param x: a vector, shape = (2**n); k <= n
    :param args: a list; len(args) = k
    :return: result of Q applied to the qubits of x given by args, so:

    X.shape = (2, 2)
    apply(X, x, [0]) applies X to qubit 0 of x
    apply(X, x, [1]) applies X to qubit 1 of x

    CX.shape = (4, 4)
    apply(CX, x, [0, 1]) applies CX to qubits 0 and 1 of x
    apply(CX, x, [1. 2]) applies CX to qubits 1 and 2 of x
    apply(CX, x, [0, 2]) applies CX to qubits 0 and 2 of x
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
    # The non-args-part of idx runs through all non-arg qubits.
    idx = [slice(None)] * n

    y = x.view(n * [2])  # a cube, shape = (2, 2, .., 2)
    result = zeros(N, dtype=qtype).view(n * [2])  # a cube, shape = (2, 2, .., 2)

    # run through all non-args qubits
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


def extend(Q: tensor, args: list, n: int) -> tensor:
    """
    :param Q: a tensor, shape = (2**k, 2**k)
    :param args: a list of indices; len(args) = k
    :param n: number of qubits Q is to be extended to
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
        a = apply(Q, B[j], args)
        result[:, j] = a


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

#
# # Controlled NOT  = H2 * CX * H2
# CX2 = tensor([[1, 0, 0, 0],
#               [0, 0, 0, 1],
#               [0, 0, 1, 0],
#               [0, 1, 0, 0]], dtype=qtype, device=dev)
#
# # controlled Z
# CZ = tensor([[1, 0, 0, 0],
#              [0, 1, 0, 0],
#              [0, 0, 1, 0],
#              [0, 0, 0, -1]], dtype=qtype, device=dev)
#
# BELL = CX.mm(tmm(H, I))
#
# # SWAP = CX * CX2 * CX
# SWAP = tensor([[1, 0, 0, 0],
#                [0, 0, 1, 0],
#                [0, 1, 0, 0],
#                [0, 0, 0, 1]], dtype=qtype, device=dev)
#
# # REV = CX * (tmm(X, I)) * CX
# REV = tensor([[0, 0, 0, 1],
#               [0, 0, 1, 0],
#               [0, 1, 0, 0],
#               [1, 0, 0, 0]], dtype=qtype, device=dev)
#
#
