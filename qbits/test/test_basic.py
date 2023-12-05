# j. siedersleben, Qubits and Quantum Computing, November 2023

import unittest

from basics import *
from qcatalogue import X, CX, TOFF


class TestBasics(unittest.TestCase):
    def test_basis2bin(self):
        n = 5
        N = 2 ** n
        B = torch.eye(N)
        for j in range(N):
            b = basis2bin(B[j])
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
        # This is to explain torch.permute
        # bs is just all three-dimensional binary indices
        # [[0, 0, 0], ... , [1, 1, 1]]
        # x is an arbitrary tensor with x.dim() = 3
        # p is an arbitrary permutation of three indices

        bs = [int2bin(j, 3) for j in range(8)]
        x = torch.arange(8).view(2, 2, 2)
        p = [2, 0, 1]

        # x.permute(p) does essentially this: The statement
        #
        # y = x.permute(p)
        #
        # creates a new tensor via  y[p[.]] = x[.], or:
        # y[permuted index] = x[original index].
        # This is what happens in the next 3 lines
        y = torch.zeros_like(x)
        for b in bs:
            y[tuple([b[i] for i in p])] = x[tuple(b)]
        z = x.permute(p)
        self.assertTrue(torch.allclose(y, z))
        #
        # If you want to permute the other way round, that is:
        # y[original index] = x[permuted index],
        # you have to call torch.permute(inv_perm(p))
        y = torch.zeros_like(x)
        for b in bs:
            y[tuple(b)] = x[tuple([b[i] for i in p])]
        z = x.permute(inv_perm(p))
        self.assertTrue(torch.allclose(y, z))

    def test_inv_perm(self):
        psi = torch.arange(32) + 100

        p = list(range(32))
        p.reverse()
        q = inv_perm(p)
        self.assertTrue(torch.allclose(psi, psi[p][q]))
        self.assertTrue(torch.allclose(psi, psi[q][p]))

        p1 = list(range(16))
        p2 = list(range(16, 32))
        p = p2 + p1
        q = inv_perm(p)
        psi = torch.arange(32) + 100
        self.assertTrue(torch.allclose(psi, psi[p][q]))
        r = compose(p, q)
        self.assertListEqual(r, list(range(32)))

    def test_compose(self):
        p = [1, 2, 4, 3, 0]
        q = [2, 4, 0, 1, 3]
        p1 = inv_perm(p)
        q1 = inv_perm(q)
        self.assertListEqual(compose(p, p1), list(range(5)))
        self.assertListEqual(compose(q, q1), list(range(5)))

    def test_curry(self):

        # testing CX
        A00 = tensor([0], dtype=qtype)
        A01 = tensor([1], dtype=qtype)
        Q = curry(CX, [[0, 0], [1, 0]])
        self.assertTrue(torch.allclose(Q, A01))
        Q = curry(CX, [[0, 0], [1, 1]])
        self.assertTrue(torch.allclose(Q, A01))
        Q = curry(CX, [[0, 1], [1, 0]])
        self.assertTrue(torch.allclose(Q, A00))
        Q = curry(CX, [[0, 1], [1, 1]])
        self.assertTrue(torch.allclose(Q, A00))

        A1 = tensor([[1, 0], [0, 0]], dtype=qtype)
        Q = curry(CX, [[0, 0]])
        self.assertTrue(torch.allclose(Q, I(1)))
        Q = curry(CX, [[0, 1]])
        self.assertTrue(torch.allclose(Q, X))
        Q = curry(CX, [[1, 0]])
        self.assertTrue(torch.allclose(Q, A1))
        Q = curry(CX, [[1, 1]])
        self.assertTrue(torch.allclose(Q, A1))

        Q = curry(CX, [])
        self.assertTrue(torch.allclose(Q, CX))

        # testing X
        Q = curry(X, [])
        self.assertTrue(torch.allclose(X, Q))

        Q = curry(X, [[0, 0]])
        self.assertTrue(torch.allclose(Q, A00))
        Q = curry(X, [[0, 1]])
        self.assertTrue(torch.allclose(Q, A00))

        # testing TOFF
        Q = curry(TOFF, [])
        self.assertTrue(torch.allclose(TOFF, Q))
        Q = curry(TOFF, [[0, 0]])
        self.assertTrue(torch.allclose(Q, I(2)))
        Q = curry(TOFF, [[0, 1]])
        self.assertTrue(torch.allclose(Q, CX))
        Q = curry(TOFF, [[1, 1]])
        self.assertTrue(torch.allclose(Q, CX))
