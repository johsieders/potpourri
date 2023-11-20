# j. siedersleben, Qubits and Quantum Computing, November 2023

import unittest

from basics import *


class TestBasics(unittest.TestCase):
    def test_basis2bin(self):
        n = 5
        N = 2 ** n
        B = torch.eye(N)
        for j in range(N):
            b = basis2bin(B[j], n)
            k = bin2int(b)
            psi = bin2basis(b)
            self.assertEqual(k, j)
            self.assertTrue(torch.equal(psi, B[j]))

    def test_int2bin(self):
        n = 5
        for i in range(2 ** n):
            b = int2bin(i, n)
            k = bin2int(b)
            self.assertEqual(k, i)

    def test_matrix2perm(self):
        p = [1, 0, 4, 2, 3]
        M = perm2matrix(p)
        q = matrix2perm(M)
        self.assertEqual(p, q)

    def test_permute(self):
        perm_x = permute([0, 1, 2])
        self.assertListEqual(perm_x, list(range(8)))
        perm_x = permute([1, 0, 2])
        self.assertListEqual(perm_x, [0, 1, 4, 5, 2, 3, 6, 7])

        perm_x = permute_x([0, 1, 2], [0, 1, 2], 3)
        self.assertListEqual(perm_x, list(range(8)))
        perm_x = permute_x([1, 0, 2], [0, 1, 2], 3)
        self.assertListEqual(perm_x, [0, 1, 4, 5, 2, 3, 6, 7])

        perm_x = permute_x([0, 1, 2], [0, 1, 2], 4)
        self.assertListEqual(perm_x, list(range(16)))
        perm_x = permute_x([1, 0, 2], [0, 1, 2], 4)
        self.assertListEqual(perm_x, [0, 1, 2, 3, 8, 9, 10, 11, 4, 5, 6, 7, 12, 13, 14, 15])

    def test_inverse_perm(self):
        psi = torch.arange(32) + 100

        p = list(range(32))
        p.reverse()
        q = inverse_perm(p)
        self.assertTrue(torch.allclose(psi, psi[p][q]))

        p1 = list(range(16))
        p2 = list(range(16, 32))
        p = p2 + p1
        q = inverse_perm(p)
        psi = torch.arange(32) + 100
        self.assertTrue(torch.allclose(psi, psi[p][q]))
        r = compose(p, q)
        self.assertListEqual(r, list(range(32)))

    def test_compose(self):
        p = [1, 2, 4, 3, 0]
        q = [2, 4, 0, 1, 3]
        p1 = inverse_perm(p)
        q1 = inverse_perm(q)
        self.assertListEqual(compose(p, p1), list(range(5)))
        self.assertListEqual(compose(q, q1), list(range(5)))
