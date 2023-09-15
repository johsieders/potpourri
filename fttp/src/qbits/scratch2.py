# 23.3.2022
# testing tensors

import random
from cmath import exp, pi, sqrt

import torch
from torch import tensor, empty, zeros

qtype = torch.complex64


class Qtensor(torch.Tensor):

    def __init__(self, x):
        super().__init__(x, dtype=torch.complex64)

    def qmm(self, B: torch.Tensor) -> torch.Tensor:
        """
        :param B: a tensor
        :return: result = tensor product of A and B; size(R) = (m_A * m_B, n_A * n_B)
        result[ii, jj] = A[ii] * B[jj]
        where ii is a multi-dim index of a and jj a multi-dim index of b
        """
        m_A, n_A = self.size()
        m_B, n_B = B.size()
        result = empty(m_A * m_B, n_A * n_B, dtype=self.dtype)
        for i in range(m_A):
            for j in range(n_A):
                result[i * m_B:(i + 1) * m_B, j * n_B:(j + 1) * n_B] = self[i, j] * B
        return Qtensor(result)

    def qmv(self, psi: torch.Tensor) -> torch.Tensor:
        """
        :param psi: a vector
        :return: result = tensor product of A and B; size(R) = (m_A * m_B, n_A * n_B)
        result[i, j] = A[i] * B[j]
        where i is a multi-dim index of a and j a multi-dim index of b
        """
        B = psi.view(-1, 1)
        return self.mm(B)

    def qpow(self, n):
        if n == 0:
            return Qtensor(torch.eye(self.size()[0]))
        if n == 1:
            return self
        else:
            n, r = divmod(n, 2)
            B = self.qpow(n)
            C = B.qmm(B)
            return C if r == 0 else self.qmm(C)


def int2bin(i, n):
    """
    :param i: an integer >= 0
    :param n: length of list
    :return: binary index of length max(n, log2(i))
    6, 2 -> [1, 1, 0]
    6, 3 -> [1, 1, 0]
    6, 4 -> [0, 1, 1, 0]
    """
    return [int(c) for c in bin(i)[2:].rjust(n, '0')]


def bin2int(ii):
    """
    :param ii: a binary index, e.g. [0,1,0,0,1]
    :return: integer value of this number, [0,1,0,0,1] -> 9
    """
    result = 0
    for digit in ii:
        result = (result << 1) | digit
    return result


def basis(ii):
    """
    :param ii: a binary number given as list, e.g. [0,1, 1]
    :return: the corresponding base vector, size = (2**n, 1).
    Example:
    basis([0, 0, 0]) = [1, 0, 0, 0, 0, 0, 0, 0].T
    basis([0, 1, 1]) = [0, 0, 0, 1, 0, 0, 0, 0].T
    basis([1, 1, 1]) = [0, 0, 0, 0, 0, 0, 0, 1].T
    """
    result = zeros(2 ** len(ii), dtype=qtype)
    result[bin2int(ii)] = 1
    return Qtensor(result)


def apply(Q, x):
    result = Q[0].mm(x)
    for q in Q[1:]:
        result = q.mm(result)
    return result


def U(f, n):
    """
    :param f: a binary function of n - 1 binary variables
    :param n: the number n >= 2
    :return: the unitary (2**n x 2**n) matrix U(f)
    """
    N = 2 ** n
    U = zeros((N, N), dtype=qtype)
    for i in range(N):
        ii = int2bin(i, n)
        head, tail = ii[:-1], ii[-1]
        j = bin2int(head + [f(head) ^ tail])
        U[i, j] = 1
    return U


def reorder(perm):
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
    return [bin2int([b[i] for i in perm]) for b in binaries]


def tmul(A, B):
    """
    :param A: a tensor
    :param B: a tensor
    :return: result = tensor product of A and B; size(R) = (m_A * m_B, n_A * n_B)
    result[i, j] = A[i] * B[j]
    where i is a multi-dim index of a and j a multi-dim index of b
    """
    m_A, n_A = A.size()
    m_B, n_B = B.size()
    result = empty(m_A * m_B, n_A * n_B, dtype=A.dtype)
    for i in range(m_A):
        for j in range(n_A):
            result[i * m_B:(i + 1) * m_B, j * n_B:(j + 1) * n_B] = A[i, j] * B
    return result


def tpow(A, n):
    if n == 0:
        return torch.eye(A.size()[0], dtype=A.dtype)
    if n == 1:
        return A
    else:
        n, r = divmod(n, 2)
        B = tpow(A, n)
        C = tmul(B, B)
        return C if r == 0 else tmul(A, C)


def measure(x):
    n = x.size()[0]
    return random.choices(range(2 ** n), weights=x ** 2)


identity
I = Qtensor([[1, 0],
             [0, 1]])

# NOT, Pauli-X
X = Qtensor([[0, 1],
             [1, 0]])

# Pauli-Y
Y = Qtensor([[0, -1j],
             [1j, 0]])

# Pauli-Z
Z = Qtensor([[1, 0],
             [0, -1]])

# Phase
S = Qtensor([[1, 0],
             [0, 1j]])

# Hadamard
H = 1 / sqrt(2) * Qtensor([[1, 1],
                           [1, -1]])
# pi/8
T = Qtensor([[1, 0],
             [0, exp(1j * pi / 4)]])

# Controlled NOT
CX = Qtensor([[1, 0, 0, 0],
              [0, 1, 0, 0],
              [0, 0, 0, 1],
              [0, 0, 1, 0]])

# controlled Z
CZ = Qtensor([[1, 0, 0, 0],
              [0, 1, 0, 0],
              [0, 0, 1, 0],
              [0, 0, 0, -1]])

# SWAP
SWAP = Qtensor([[1, 0, 0, 0],
                [0, 0, 1, 0],
                [0, 1, 0, 0],
                [0, 0, 0, 1]])

# Toffoli
TOFF = Qtensor([[1, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 1, 0]])

# BELL = CX.mm(tmul(H, I))
# BELL = CX.mm(H.qmm(I))

H1 = Qtensor([[1, 1],
              [1, -1.]])

BELL1 = CX.mm(tmul(H1, I))


# Deutsch-Jozsa Algorithm

def f_const(c):
    return lambda x: c


def f_mod2(x):
    return x[-1]


def f_xor(x):
    return x[0] if len(x) == 1 else x[0] ^ x[1]


def DEUTSCH(f, n):
    H1 = tmul(tpow(H, n - 1), I)
    return [H1, U(f, n), H1]


def DEUTSCH_(f, n):
    Hn = H.qp
    Hn = tpow(H, n)
    return [Hn, U(f, n), Hn]


if __name__ == '__main__':
    pass
    print(BELL)

    n = 3
    y = 1 / sqrt(2) * tensor([1, -1], dtype=qtype)
    psi = basis((n - 1) * [0]).qmv(y)
    psi_ = basis((n - 1) * [0] + [1])

    # Hn = tpow(H, n)
    # f = f_const(1)
    # # f = f_xor
    # Uf = U(f, n)
    # print('\n', psi_)
    # print('\n', Hn.real)
    # print('\n', Uf.real)
    # # print('\n', Uf.mm(Hn))
    # # print('\n', Hn.mm(Uf.mm(Hn)))
    # # print('\n', Hn.mm(Uf.mm(Hn)).mm(psi_))

    # print(H1)
    # print()
    # print(Uf)
    # print()
    # print(Uf.mm(H1))
    #
    # fs = [f_const(0), f_const(1), f_xor, f_mod2]
    # tbl = torch.empty(2 ** n).view(-1, 1)
    #
    # for f in fs:
    #     tbl = torch.cat((tbl, apply(DEUTSCH(f, n), psi).real), 1)
    #
    # df = pd.DataFrame(tbl, columns=['idx', 'f_const0', 'f_const1', 'f_xor', 'f_mod2'])
    # df['idx'] = [int2bin(i, n) for i in range(2 ** n)]
    # print(df)
    # print())
    #
    # tbl = torch.empty(2 ** n).view(-1, 1)
    # for f in fs:
    #     tbl = torch.cat((tbl, apply(DEUTSCH_(f, n), psi_).real), 1)
    #
    # print('\n', psi_)
    # df = pd.DataFrame(tbl, columns=['idx', 'f_const0', 'f_const1', 'f_xor', 'f_mod2'])
    # df['idx'] = [int2bin(i, n) for i in range(2 ** n)]
    # print(df)

    # Superdense Coding

    # def DENSE(a, b):
    #     return [BELL, tmul(tpow(X, a), I), tmul(tpow(Z, b), I), BELL.T]
    #
    # for a in range(2):
    #     for b in range(2):
    #         y = apply(DENSE(a, b), basis([0, 0])).view(2, 2)
    #         print(y[b, a])

    # Teleportation

    # TELE = [tmul(I, BELL),
    #         tmul(BELL.T, I)]       # BELL.T == BELL ** (-1)
    #
    # alpha = 0.1
    # psi = tensor([alpha, sqrt(1 - alpha ** 2)], dtype=qtype).view(-1, 1)
    # x = tmul(psi, basis([0, 0]))
    # y = apply(TELE, x).view(2, 2, 2)
    #
    # for a in range(2):
    #     for b in range(2):
    #         phi = 2 * tpow(Z, a).mm(tpow(X, b).mm(y[a, b].view(-1, 1)))
    #         print(phi - psi)
