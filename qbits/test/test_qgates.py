# j. siedersleben, Qubits and Quantum Computing, November 2023

import unittest

import torch
from torch import tensor

from basics import dev, one_at
from qgates import I, H, X, CX, CX2, FRED, U
from qgates import perm_X, perm_CX, perm_CX2
from qgates import tmm, apply, qgate, matrix2perm


class TestQGates(unittest.TestCase):

    def test_X(self):
        aux = [complex(k + 10) for k in range(2)]
        psi = tensor(aux, device=dev)
        phi1 = X.mv(psi)
        phi2 = apply(X, psi, [0])
        phi3 = psi[perm_X]
        self.assertTrue(torch.allclose(phi1, phi2))
        self.assertTrue(torch.allclose(phi1, phi3))
        G = qgate(X, 1, [0])
        self.assertTrue(torch.allclose(X, G))

        for i in range(1):
            aux = [complex(k + 10) for k in range(4)]
            psi = tensor(aux, device=dev)
            Q = tmm(X, I(1)) if i == 0 else tmm(I(1), X)
            qx = matrix2perm(Q)
            phi1 = Q.mv(psi)
            phi2 = apply(X, psi, [i])
            phi3 = psi[qx]
            self.assertTrue(torch.allclose(phi1, phi2))
            self.assertTrue(torch.allclose(phi1, phi3))
            G = qgate(X, 2, [i])
            self.assertTrue(torch.allclose(Q, G))

        aux = [complex(k + 10) for k in range(8)]
        psi = tensor(aux, device=dev)
        Q = tmm(I(2), X)
        qx = matrix2perm(Q)
        phi1 = Q.mv(psi)
        phi2 = apply(X, psi, [2])
        phi3 = psi[qx]
        self.assertTrue(torch.allclose(phi1, phi2))
        self.assertTrue(torch.allclose(phi1, phi3))
        G = qgate(X, 3, [2])
        self.assertTrue(torch.allclose(Q, G))

    def test_CX(self):
        # apply CX to [0, 1] of [0, 1]
        aux = [complex(k + 10) for k in range(4)]
        psi = tensor(aux, device=dev)
        phi1 = CX.mv(psi)
        phi2 = apply(CX, psi, [0, 1])
        phi3 = psi[perm_CX]
        self.assertTrue(torch.allclose(phi1, phi2))
        self.assertTrue(torch.allclose(phi1, phi3))
        G = qgate(CX, 2, [0, 1])
        self.assertTrue(torch.allclose(CX, G))

        # apply CX to [0, 1] of [0, 1, 2]
        aux = [complex(k + 10) for k in range(8)]
        psi = tensor(aux, device=dev)
        Q = tmm(CX, I(1))
        qx = matrix2perm(Q)
        phi1 = Q.mv(psi)
        phi2 = apply(CX, psi, [0, 1])
        phi3 = psi[qx]
        self.assertTrue(torch.allclose(phi1, phi2))
        self.assertTrue(torch.allclose(phi1, phi3))
        G = qgate(CX, 3, [0, 1])
        self.assertTrue(torch.allclose(Q, G))

        # apply CX to [1, 2] of [0, 1, 2]
        aux = [complex(k + 10) for k in range(8)]
        psi = tensor(aux, device=dev)
        Q = tmm(I(1), CX)
        qx = matrix2perm(Q)
        phi1 = Q.mv(psi)
        phi2 = apply(CX, psi, [1, 2])
        phi3 = psi[qx]
        self.assertTrue(torch.allclose(phi1, phi2))
        self.assertTrue(torch.allclose(phi1, phi3))
        G = qgate(CX, 3, [1, 2])
        self.assertTrue(torch.allclose(Q, G))

        # apply CX to [0, 2] of [0, 1, 2]
        aux = [complex(k + 10) for k in range(8)]
        psi = tensor(aux, device=dev)
        Q = qgate(CX, 3, [0, 2])
        qx = matrix2perm(Q)
        phi1 = Q.mv(psi)
        phi2 = apply(CX, psi, [0, 2])
        phi3 = psi[qx]
        self.assertTrue(torch.allclose(phi1, phi2))
        self.assertTrue(torch.allclose(phi1, phi3))

    def test_qgate(self):
        Q = qgate(CX, 2, [0, 1])
        self.assertTrue(torch.allclose(Q, CX))
        Q = qgate(FRED, 3, [0, 1, 2])
        self.assertTrue(torch.allclose(Q, FRED))

    def test_Uf(self):
        aux = [complex(k + 10) for k in range(8)]
        psi = tensor(aux, device=dev)
        f = one_at(3)

        Q = U(f, 2)
        qx = matrix2perm(Q)
        phi1 = Q.mv(psi)
        phi2 = apply(Q, psi, [0, 1, 2])
        phi3 = psi[qx]
        G = qgate(Q, 3, [0, 1, 2])
        self.assertTrue(torch.allclose(phi1, phi2))
        self.assertTrue(torch.allclose(phi1, phi3))
        self.assertTrue(torch.allclose(Q, G))

        aux = [complex(k + 10) for k in range(16)]
        psi = tensor(aux, device=dev)
        Uf = U(f, 2)
        Q = tmm(I(1), Uf)
        qx = matrix2perm(Q)
        phi1 = Q.mv(psi)
        phi2 = apply(Uf, psi, [1, 2, 3])
        phi3 = psi[qx]
        G = qgate(Uf, 4, [1, 2, 3])
        self.assertTrue(torch.allclose(phi1, phi2))
        self.assertTrue(torch.allclose(phi1, phi3))
        self.assertTrue(torch.allclose(Q, G))

    def test_CX2(self):
        H2 = tmm(H, H)
        Q = H2.mm(CX).mm(H2)
        self.assertTrue(torch.allclose(Q, CX2))

        aux = [complex(k + 10) for k in range(4)]
        psi = tensor(aux, device=dev)
        phi1 = CX2.mv(psi)
        phi2 = apply(CX2, psi, [0, 1])
        phi3 = psi[perm_CX2]
        self.assertTrue(torch.allclose(phi1, phi2))
        self.assertTrue(torch.allclose(phi1, phi3))

        aux = [complex(k + 10) for k in range(8)]
        psi = tensor(aux, device=dev)
        Q = tmm(CX2, I(1))
        qx = matrix2perm(Q)
        phi1 = Q.mv(psi)
        phi2 = apply(CX2, psi, [0, 1])
        phi3 = psi[qx]
        G = qgate(CX2, 3, [0, 1])

        self.assertTrue(torch.allclose(phi1, phi2))
        self.assertTrue(torch.allclose(phi1, phi3))
        self.assertTrue(torch.allclose(Q, G))

