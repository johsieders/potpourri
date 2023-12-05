# j. siedersleben, Qubits and Quantum Computing, November 2023

import unittest

from qappl import curry
from qbasics import *
from qcat import I, X, CX, TOFF


class TestQAppl(unittest.TestCase):

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
