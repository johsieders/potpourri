# j. siedersleben, Qubits and Quantum Computing, November 2023

import unittest
from basics import *
from qugates import I, X, CX, perm_X, perm_CX, U, tmm


class TestBasics(unittest.TestCase):

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
        Q = tmm(I, X)
        qx = matrix2perm(Q)
        phi1 = Q.mv(psi)
        phi2 = apply(X, psi, [1])
        # px = permute_x(perm_CX, [0, 1], 3)
        phi3 = psi[qx]

    def test_extend(self):
        T = extend(X, [0], 2)

    def test_CX(self):
        aux = [complex(k + 10) for k in range(4)]
        psi = tensor(aux, device=dev)
        phi1 = CX.mv(psi)
        phi2 = apply(CX, psi, [0, 1])
        phi3 = psi[perm_CX]
        self.assertTrue(torch.allclose(phi1, phi2))
        self.assertTrue(torch.allclose(phi1, phi3))

        aux = [complex(k + 10) for k in range(8)]
        psi = tensor(aux, device=dev)
        Q = tmm(CX, I)
        qx = matrix2perm(Q)
        phi1 = Q.mv(psi)
        phi2 = apply(CX, psi, [0, 1])
        # px = permute_x(perm_CX, [0, 1], 3)
        phi3 = psi[qx]

        self.assertTrue(torch.allclose(phi1, phi2))
        self.assertTrue(torch.allclose(phi1, phi3))

        # print(psi)
        # print(phi1)
        # print(phi2)
        # print(phi3)

    def test_Uf(self):
        aux = [complex(k + 10) for k in range(8)]
        psi = tensor(aux, device=dev)
        f = one_at(3)
        Q = U(f, 2)
        perm_Uf = matrix2perm(Q)
        phi1 = Q.mv(psi)
        phi2 = apply(Q, psi, [0, 1, 2])
        phi3 = psi[perm_Uf]

        self.assertTrue(torch.allclose(phi1, phi2))
        self.assertTrue(torch.allclose(phi1, phi3))

        aux = [complex(k + 100) for k in range(16)]
        psi = tensor(aux, device=dev)
        f = one_at(3)
        Q = tmm(I, U(f, 2))
        perm_Uf = matrix2perm(Q)
        phi1 = Q.mv(psi)
        phi2 = apply(Q, psi, [1, 2, 3])
        phi3 = psi[perm_Uf]

        self.assertTrue(torch.allclose(phi1, phi2))
        self.assertTrue(torch.allclose(phi1, phi3))

    def test_CX2(self):
        H2 = tmm(H, H)
        Q = H2.mm(CX).mm(H2)

        aux = [complex(k + 10) for k in range(4)]
        psi = tensor(aux, device=dev)
        phi1 = CX2.mv(psi)
        phi2 = apply(CX2, psi, [0, 1])
        phi3 = psi[perm_CX2]
        phi4 = Q.mv(psi)
        self.assertTrue(torch.allclose(phi1, phi2))
        self.assertTrue(torch.allclose(phi1, phi3))
        self.assertTrue(torch.allclose(phi1, phi4))

        aux = [complex(k + 10) for k in range(8)]
        psi = tensor(aux, device=dev)
        Q = tmm(CX2, I)
        px = matrix2perm(Q)
        phi1 = Q.mv(psi)
        phi2 = apply(CX2, psi, [0, 1])
        phi3 = psi[px]

        self.assertTrue(torch.allclose(phi1, phi2))
        self.assertTrue(torch.allclose(phi1, phi3))










