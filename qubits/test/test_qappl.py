# j. siedersleben, Qubits and Quantum Computing, November 2023

import unittest

from qapply import curry, shrink
from qbasics import *
from qcatalogue import I, X, CX, TOFF


class TestQAppl(unittest.TestCase):

    def test_shrink(self):
        # testing CX
        A00 = tensor([0], dtype=qtype)
        A01 = tensor([1], dtype=qtype)
        Q = shrink(CX, [[0, 0], [1, 0]])
        self.assertTrue(torch.allclose(Q, A01))
        Q = shrink(CX, [[0, 0], [1, 1]])
        self.assertTrue(torch.allclose(Q, A01))
        Q = shrink(CX, [[0, 1], [1, 0]])
        self.assertTrue(torch.allclose(Q, A00))
        Q = shrink(CX, [[0, 1], [1, 1]])
        self.assertTrue(torch.allclose(Q, A00))

        A1 = tensor([[1, 0], [0, 0]], dtype=qtype)
        Q = shrink(CX, [[0, 0]])
        self.assertTrue(torch.allclose(Q, I(1)))
        Q = shrink(CX, [[0, 1]])
        self.assertTrue(torch.allclose(Q, X))
        Q = shrink(CX, [[1, 0]])
        self.assertTrue(torch.allclose(Q, A1))
        Q = shrink(CX, [[1, 1]])
        self.assertTrue(torch.allclose(Q, A1))

        Q = shrink(CX, [])
        self.assertTrue(torch.allclose(Q, CX))

        # testing X
        Q = shrink(X, [])
        self.assertTrue(torch.allclose(X, Q))

        Q = shrink(X, [[0, 0]])
        self.assertTrue(torch.allclose(Q, A00))
        Q = shrink(X, [[0, 1]])
        self.assertTrue(torch.allclose(Q, A00))

        # testing TOFF
        Q = shrink(TOFF, [])
        self.assertTrue(torch.allclose(TOFF, Q))
        Q = shrink(TOFF, [[0, 0]])
        self.assertTrue(torch.allclose(Q, I(2)))
        Q = shrink(TOFF, [[0, 1]])
        self.assertTrue(torch.allclose(Q, CX))
        Q = shrink(TOFF, [[1, 1]])
        self.assertTrue(torch.allclose(Q, CX))

    def test_curry(self):
        Q = curry(CX, [[0, 0]])
        print(Q, '\n')
        # self.assertTrue(torch.allclose(Q, I(1)))
        Q = curry(CX, [[0, 1]])
        print(Q, '\n')
        # self.assertTrue(torch.allclose(Q, X))
