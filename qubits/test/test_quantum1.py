# j. siedersleben, Qubits and Quantum Computing, November 2023

import unittest

from scratch.scratch import *


class Testquantum(unittest.TestCase):
    def test_matrix_perm(self):
        perm_in = [0, 1, 4, 5, 2, 3, 6, 7]
        M = perm2matrix(perm_in)
        print(M.real)
        perm_out = matrix2perm(M)
        print(perm_out)
        self.assertEqual(perm_in, perm_out)

    def test_CXfun(self):
        x = torch.tensor([0, 1, 2, 3], dtype=qtype, device=dev).view(-1, 1)

        y1 = CX.mm(x)
        y2 = CXfun(x, 0, 1)
        print(f'CX.mm(x) = {y1}')
        print(f'CXfun(x, 0, 1) = {y2}')
        self.assertTrue(torch.allclose(y1, y2))

    def test_restricted3(self):
        x = torch.tensor([0, 1, 2, 3, 4, 5, 6, 7], dtype=qtype, device=dev).view(-1, 1)

        M01a = matrix2perm(tmm(CX, I))  # apply CX to qubits 0 and 1
        M01b = CXfun(x, 0, 1).flatten().real  # apply CX to qubits 0 and 1
        M01b = [int(i) for i in M01b.tolist()]
        self.assertEqual(M01a, M01b)

        M12a = matrix2perm(tmm(I, CX))  # apply CX to qubits 1 and 2
        M12b = CXfun(x, 1, 2).flatten().real  # apply CX to qubits 1 and 2
        M12b = [int(i) for i in M12b.tolist()]
        self.assertEqual(M12a, M12b)

        P102 = perm2matrix(permute([1, 0, 2]))  # swap columns 0 and 1
        P021 = perm2matrix(permute([0, 2, 1]))  # swap columns 1 and 2

        M02a = P021.mm(perm2matrix(M01a)).mm(P021)  # apply CX to qubits 0 and 2
        M02b = P102.mm(perm2matrix(M12a)).mm(P102)  # apply CX to qubits 0 and 2
        M02c = CXfun(x, 0, 2).flatten().real  # apply CX to qubits 1 and 2
        M02c = [int(i) for i in M02c.tolist()]
        self.assertEqual(M02a, M02b)
        self.assertEqual(M02a, M02c)

        # print()
        # print(f'M01a = {matrix2perm(M01a)}')
        # print(f'CXfun(0, 1) = {CXfun(x, 0, 1).real}')
        # print()
        #
        # print(f'M12 = {matrix2perm(M12)}')
        # print(f'CXfun(1, 2) = {CXfun(x, 1, 2).real}')
        # print()
        #
        # print(f'P102 = {matrix2perm(P102)}')
        # print(f'P021 = {matrix2perm(P021)}')
        # print(f'M02a = {matrix2perm(M02a)}')
        # print(f'CXfun(0, 2) = {CXfun(x, 0, 2).real}')
        #
        # self.assertTrue(torch.allclose(M02a, M02b))

    def test_restricted4(self):
        M01 = tmm(tmm(CX, I), I)  # apply CX to qubits 0 and 1
        M12 = tmm(I, tmm(I, CX))  # apply CX to qubits 2 and 3
        M23 = tmm(tmm(I, CX), I)  # apply CX to qubits 1 and 2

        P0213 = perm2matrix(permute([0, 2, 1, 3]))  # swap columns 1 and 2
        P0321 = perm2matrix(permute([0, 3, 2, 1]))  # swap columns 1 and 3

        M02 = P0213.mm(M01).mm(P0213)  # apply CX to qubits 0 and 2
        M03 = P0321.mm(M23).mm(P0321)  # apply CX to qubits 2 and 3
        M13 = P0213.mm(M12).mm(P0213)  # apply CX to qubits 1 and 3

        print(f'M01 = {matrix2perm(M01)}')
        print(f'M12 = {matrix2perm(M12)}')
        print(f'M23 = {matrix2perm(M23)}')
        print(f'P0213 = {matrix2perm(P0213)}')
        print(f'P0321 = {matrix2perm(P0321)}')
        print(f'M02 = {matrix2perm(M02)}')
        print(f'M03 = {matrix2perm(M03)}')
        print(f'M13 = {matrix2perm(M13)}')
