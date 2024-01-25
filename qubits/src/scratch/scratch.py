# 29.3.2022
# testing tensors
import random
from cmath import exp, pi, sqrt

import torch
from torch import tensor, empty, zeros

qtype = torch.complex64


def int2bin(j, n):
    """
    :param i: an integer >= 0
    :param n: length of list
    :return: binary digits of i as a list of length at least n
    6, 3 -> [1, 1, 0]
    6, 4 -> [0, 1, 1, 0]
    """
    return [int(c) for c in bin(j)[2:].rjust(n, '0')]


def bin2int(b):
    """
    :param b: a binary number given as list, e.g. [0,1,0,0,1]
    :return: integer value of this number, e.g.
    [0,1,0,0,1] -> 9
    """
    result = 0
    for digit in b:
        result = (result << 1) | digit
    return result


def U(f, n):
    N = 2 ** n
    U = zeros((N, N), dtype=qtype)
    for i in range(N):
        x = int2bin(i, n)
        y = x[:-1] + [f(x[:-1]) ^ x[-1]]
        U[bin2int(x), bin2int(y)] = 1
    return U


def tmul(a, b):
    """
    :param a: a tensor
    :param b: a tensor
    :return: result = tensor product of a and b; size(r) = (m_a * m_b, n_a * n_b)
    result[i, j] = a[i] * b[j]
    where i is an index of a and j an index of b
    """
    m_a, n_a = a.size()
    m_b, n_b = b.size()
    result = empty(m_a * m_b, n_a * n_b, dtype=a.dtype)
    for i in range(m_a):
        for j in range(n_a):
            result[i * m_b:(i + 1) * m_b, j * n_b:(j + 1) * n_b] = a[i, j] * b
    return result


def tpow(A, n):
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


# identity
I = tensor([[1, 0],
            [0, 1]], dtype=qtype)

# NOT, Pauli-X
X = tensor([[0, 1],
            [1, 0]], dtype=qtype)

# Pauli-Y
Y = tensor([[0, -1j],
            [1j, 0]], dtype=qtype)

# Pauli-Z
Z = tensor([[1, 0],
            [0, -1]], dtype=qtype)

# Phase
S = tensor([[1, 0],
            [0, 1j]], dtype=qtype)

# Hadamard
H = 1 / sqrt(2) * tensor([[1, 1],
                          [1, -1]], dtype=qtype)
# pi/8
T = tensor([[1, 0],
            [0, exp(1j * pi / 4)]])

# Controlled NOT
CX = tensor([[1, 0, 0, 0],
             [0, 1, 0, 0],
             [0, 0, 0, 1],
             [0, 0, 1, 0]], dtype=qtype)

# controlled Z
CZ = tensor([[1, 0, 0, 0],
             [0, 1, 0, 0],
             [0, 0, 1, 0],
             [0, 0, 0, -1]], dtype=qtype)

# SWAP
SWAP = tensor([[1, 0, 0, 0],
               [0, 0, 1, 0],
               [0, 1, 0, 0],
               [0, 0, 0, 1]], dtype=qtype)

# Toffoli
TOFF = tensor([[1, 0, 0, 0, 0, 0, 0, 0],
               [0, 1, 0, 0, 0, 0, 0, 0],
               [0, 0, 1, 0, 0, 0, 0, 0],
               [0, 0, 0, 1, 0, 0, 0, 0],
               [0, 0, 0, 0, 1, 0, 0, 0],
               [0, 0, 0, 0, 0, 1, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 1],
               [0, 0, 0, 0, 0, 0, 1, 0]], dtype=qtype)

BELL = CX.mm(tmul(H, I))

H1 = tensor([[1, 1],
             [1, -1.]], dtype=qtype)

BELL1 = CX.mm(tmul(H1, I))


def vmul(x, y):
    return x.mm(y.T).view(-1, 1)


class QLayer(object):
    def __init__(self, n):
        self.rng = set(range(n))
        self.gates = []

    def addGate(self, gate, idx):
        reduction = list(self.rng - set(idx))
        self.gates.append([gate, reduction])

    def __call__(self, x):
        ys = []
        for g, reduction in self.gates:
            y = (x.sum(reduction) if reduction else x).view(-1, 1)
            ys.append(g.mm(y))
        result = ys[0]
        for y in ys[1:]:
            result = vmul(result, y)
        return result


if __name__ == '__main__':
    H = tensor([[1, 1],
                [1, -1.]])

    CNOT = tensor([[1, 0, 0, 0],
                   [0, 1, 0, 0],
                   [0, 0, 0, 1],
                   [0, 0, 1, 0.]])

    H2 = tmul(H, H)

    # x = tensor([2, 3, 10, 11, 20, 21, 100, 110.]).view(2, 2, 2)
    x = tensor([2, 3, 5, 10.]).view(2, 2)
    # x = tensor([1, 2.]).view(-1, 1)

    y = vmul(x[[0]].T, x[[1]].T)

    q = QLayer(2)
    q.addGate(H, [0])
    q.addGate(H, [1])

    r = q(x)
    s = H2.mm(y)

    print(r)
    print(s)

    # for i in range(2):
    #     for j in range(2):
    #         for k in range(2):
    #             print(i, j, k, x[i, j, k].item())

    # print()
    # print(x.sum([1, 2]))
    # print(x.sum([0, 2]))
    # print(x.sum([0, 1]))
    # print()
    # print(x.sum(0))
    # print(x.sum(1))
    # print(x.sum(2))

    # x0 = torch.tensor([2., 3.]).view(-1, 1)
    # x1 = torch.tensor([5., 10.]).view(-1, 1)
    # v = vmul(x0, x1).view(-1, 1)
    # z = H2.mm(v)
    #
    # y0 = H.mm(x0)
    # y1 = H.mm(x1)
    # w = vmul(y0, y1)
    #
    # print()
    # print(v)
    # print(w)
    # print(z)
