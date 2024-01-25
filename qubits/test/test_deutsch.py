# 4.4.2022

# Quantum Computing with Pytorch

import unittest

import pandas as pd
import torch

from qbasics import bin2basis, int2bin, bin2int
from qcatalogue import DEUTSCH


# Deutsch-Jozsa Algorithm
# We are give a binary function f which is guaranteed to be either constant or balanced.
# We want to find out which one it is using only one evaluation of f.
# Here is the idea: Given n >= 1 (the number of arguments f takes), we proceed as follows
# 1. We apply H^n to the state |0>^n and get a state |psi>, the superposition of all 2^n basis states.
# 2. We apply U(f) to |psi> and get a state |psi'>.
# 3. We apply H^n to the state |psi'> and get a state |psi''>.
# 4. We measure |psi''> and get a binary index x.
# 5. If f is constant, then x = 0^n. If f is balanced, then x != 0^n.

# The proof is easy: If f is constant, then U(f) = I, and |psi''> = |psi>.
# If f is balanced, then U(f) = U, and |psi''> = H^n * U * H^n * |0>^n = H^n * U * |0>^n = H^n * |1>^n.
# The probability of measuring |0>^n is 1, and the probability of measuring |1>^n is 0.


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


class TestDeutsch(unittest.TestCase):
    def test_deutsch(self):
        # Deutsch-Jozsa Algorithm
        # print("\n\nDeutsch-Josza Algorithm\n")
        n = 3
        N = 2 ** n
        tbl = torch.zeros(N).view(-1, 1)

        psi = bin2basis(n * [0] + [1])  # 2N
        for f in [f_const(0), f_const(1), f_xor, f_mod2]:
            D = DEUTSCH(f, n)  # 2N
            phi = D.mv(psi)  # 2N
            phi1 = phi.view(-1, 2)[:, 1]  # N, impair elements of phi
            if f in [f_xor, f_mod2]:  # balanced
                self.assertAlmostEqual(0, phi1[0].item(), places=9)
            else:  # const
                self.assertAlmostEqual(1, abs(phi1[0].item()), places=6)
            tbl = torch.cat((tbl, phi1.real.view(-1, 1)), dim=1)

        df = pd.DataFrame(tbl, columns=['x', 'f_const0', 'f_const1', 'f_xor', 'f_mod2'])
        df['x'] = [int2bin(i, n) for i in range(2 ** n)]
        # print(df)

        # expected result
        # f = const -> result = [+/-1; 0, .., 0]
        # f balanced -> result = [0; 0, .., x, .., 0]

    def test_bernstein(self):
        # Bernstein-Vazirani Algorithm
        # print("\n\nBernstein-Vazirani Algorithm\n")
        n = 4
        N = 2 ** n
        tbl = torch.zeros(N).view(-1, 1)

        psi = bin2basis(n * [0] + [1])  # 2N
        bs = [[0, 0, 0, 0], [1, 0, 1, 0], [1, 0, 1, 1], [1, 1, 1, 1]]
        for a in bs:
            f = f_bernstein(a)
            D = DEUTSCH(f, n)  # 2N
            phi = D.mv(psi)  # 2N
            j = bin2int(a)
            phi1 = phi.view(-1, 2)[:, 1]  # N, impair elements of phi
            self.assertAlmostEqual(1, phi1[j].item(), places=6)

            tbl = torch.cat((tbl, phi1.real.view(-1, 1)), 1)

        # expected result
        # f = f_bernstein(b) -> result = [0, .., 1, .., 0] (1 at bin2int(b))
        df = pd.DataFrame(tbl, columns=['x'] + [str(b) for b in bs])
        df['x'] = [int2bin(i, n) for i in range(2 ** n)]
        # print(df)
