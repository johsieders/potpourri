# 4.4.2022

# Quantum Computing with Pytorch


import pandas as pd
import torch

from qbits.quantum import H, U, tmm, tpow, apply, bin2basis, int2bin


def DEUTSCH(f, n):
    H1 = tpow(H, n + 1)
    return [H1, U(f, n), H1]


def f_const(c):
    return lambda x: c


def f_mod2(x: list) -> int:
    # f_mod2 is balanced
    return x[-1]


def f_xor(x: list) -> int:
    # f_xor is balanced
    return x[0] if len(x) == 1 else x[0] ^ x[1]


def f_bernstein(a: list):
    def aux(x: list):
        return sum([a[i] * x[i] for i in range(len(a))]) % 2

    return aux


def deutsch(n: int):
    # Deutsch-Jozsa Algorithm
    print("\n\nDeutsch-Josza Algorithm\n")
    N = 2 ** n
    tbl = torch.empty(N).view(-1, 1)

    psi0 = bin2basis(n * [0])  # N
    xi = bin2basis([1])  # 2
    psi1 = tmm(psi0, xi)  # 2N

    for f in [f_const(0), f_const(1), f_xor, f_mod2]:
        D = DEUTSCH(f, n)  # 2N
        phi0 = apply(D, psi1)  # 2N
        phi1 = phi0[2 * torch.arange(N) + 1]  # N
        tbl = torch.cat((tbl, phi1), 1)

    df = pd.DataFrame(tbl, columns=['x', 'f_const0', 'f_const1', 'f_xor', 'f_mod2'])
    df['x'] = [int2bin(i, n) for i in range(2 ** n)]
    print(df)

    # expected result
    # f = const -> result = [+/-1; 0, .., 0]
    # f balanced -> result = [0; 0, .., x, .., 0]


def bernstein():
    # Bernstein-Vazirani Algorithm
    print("\n\nBernstein-Vazirani Algorithm\n")
    n = 3
    N = 2 ** n
    tbl = torch.empty(N).view(-1, 1)

    psi0 = bin2basis(n * [0])  # N
    xi = bin2basis([1])  # 2
    psi1 = tmm(psi0, xi)  # 2N

    bs = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]
    for b in bs:
        f = f_bernstein(b)
        D = DEUTSCH(f, n)  # 2N
        phi0 = apply(D, psi1)  # 2N
        phi1 = phi0[2 * torch.arange(N) + 1]  # N
        tbl = torch.cat((tbl, phi1), 1)

    # expected result
    # f = f_bernstein(b) -> result = [0, .., 1, .., 0] (1 at b)
    df = pd.DataFrame(tbl, columns=['x'] + [str(b) for b in bs])
    df['x'] = [int2bin(i, n) for i in range(2 ** n)]
    print(df)


if __name__ == '__main__':
    deutsch(3)
    bernstein()
