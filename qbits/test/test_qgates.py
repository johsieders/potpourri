# j. siedersleben, Qubits and Quantum Computing, November 2023

import unittest

import torch
from torch import tensor

from basics import dev, matrix2perm
from qgates import I, X, perm_X, tmm, apply


class TestQgates(unittest.TestCase):

    def test_X(self):
        aux = [complex(k + 10) for k in range(2)]
        psi = tensor(aux, device=dev)
        phi1 = X.mv(psi)
        phi2 = apply(X, psi, [0])
        phi3 = psi[perm_X]
        self.assertTrue(torch.allclose(phi1, phi2))
        self.assertTrue(torch.allclose(phi1, phi3))

        aux = [complex(k + 10) for k in range(4)]
        psi = tensor(aux, device=dev)
        Q = tmm(X, I(1))
        qx = matrix2perm(Q)
        phi1 = Q.mv(psi)
        phi2 = apply(X, psi, [0])
        phi3 = psi[qx]
        self.assertTrue(torch.allclose(phi1, phi2))
        self.assertTrue(torch.allclose(phi1, phi3))

        aux = [complex(k + 10) for k in range(4)]
        psi = tensor(aux, device=dev)
        Q = tmm(I(1), X)
        qx = matrix2perm(Q)
        phi1 = Q.mv(psi)
        phi2 = apply(X, psi, [1])
        phi3 = psi[qx]
        self.assertTrue(torch.allclose(phi1, phi2))
        self.assertTrue(torch.allclose(phi1, phi3))

        aux = [complex(k + 10) for k in range(8)]
        psi = tensor(aux, device=dev)
        Q = tmm(I(1), tmm(I(1), X))
        qx = matrix2perm(Q)
        phi1 = Q.mv(psi)
        phi2 = apply(X, psi, [2])
        phi3 = psi[qx]
        self.assertTrue(torch.allclose(phi1, phi2))
        self.assertTrue(torch.allclose(phi1, phi3))

    # def test_CX(self):
    #     aux = [complex(k + 10) for k in range(4)]
    #     psi = tensor(aux, device=dev)
    #     phi1 = CX.mv(psi)
    #     phi2 = apply(CX, psi, [0, 1])
    #     phi3 = psi[perm_CX]
    #     self.assertTrue(torch.allclose(phi1, phi2))
    #     self.assertTrue(torch.allclose(phi1, phi3))
    #
    #     aux = [complex(k + 10) for k in range(8)]
    #     psi = tensor(aux, device=dev)
    #     Q = tmm(CX, I)
    #     qx = matrix2perm(Q)
    #     phi1 = Q.mv(psi)
    #     phi2 = apply(CX, psi, [0, 1])
    #     # px = permute_x(perm_CX, [0, 1], 3)
    #     phi3 = psi[qx]
    #
    #     self.assertTrue(torch.allclose(phi1, phi2))
    #     self.assertTrue(torch.allclose(phi1, phi3))
    #
    #     # print(psi)
    #     # print(phi1)
    #     # print(phi2)
    #     # print(phi3)
    #
    # def test_Uf(self):
    #     aux = [complex(k + 10) for k in range(8)]
    #     psi = tensor(aux, device=dev)
    #     f = one_at(3)
    #     Q = U(f, 2)
    #     perm_Uf = matrix2perm(Q)
    #     phi1 = Q.mv(psi)
    #     phi2 = apply(Q, psi, [0, 1, 2])
    #     phi3 = psi[perm_Uf]
    #
    #     self.assertTrue(torch.allclose(phi1, phi2))
    #     self.assertTrue(torch.allclose(phi1, phi3))
    #
    #     aux = [complex(k + 100) for k in range(16)]
    #     psi = tensor(aux, device=dev)
    #     f = one_at(3)
    #     Q = tmm(I, U(f, 2))
    #     perm_Uf = matrix2perm(Q)
    #     phi1 = Q.mv(psi)
    #     phi2 = apply(Q, psi, [1, 2, 3])
    #     phi3 = psi[perm_Uf]
    #
    #     self.assertTrue(torch.allclose(phi1, phi2))
    #     self.assertTrue(torch.allclose(phi1, phi3))
    #
    # def test_CX2(self):
    #     H2 = tmm(H, H)
    #     Q = H2.mm(CX).mm(H2)
    #
    #     aux = [complex(k + 10) for k in range(4)]
    #     psi = tensor(aux, device=dev)
    #     phi1 = CX2.mv(psi)
    #     phi2 = apply(CX2, psi, [0, 1])
    #     phi3 = psi[perm_CX2]
    #     phi4 = Q.mv(psi)
    #     self.assertTrue(torch.allclose(phi1, phi2))
    #     self.assertTrue(torch.allclose(phi1, phi3))
    #     self.assertTrue(torch.allclose(phi1, phi4))
    #
    #     aux = [complex(k + 10) for k in range(8)]
    #     psi = tensor(aux, device=dev)
    #     Q = tmm(CX2, I)
    #     px = matrix2perm(Q)
    #     phi1 = Q.mv(psi)
    #     phi2 = apply(CX2, psi, [0, 1])
    #     phi3 = psi[px]
    #
    #     self.assertTrue(torch.allclose(phi1, phi2))
    #     self.assertTrue(torch.allclose(phi1, phi3))
    #
