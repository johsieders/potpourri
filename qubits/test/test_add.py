# j. siedersleben, Qubits and Quantum Computing, November 2023

import unittest

import qcatalogue
from qapply import curry
from qbasics import bin2int
from qcatalogue import *


class TestAdd(unittest.TestCase):
    def test_add(self):
        # start = time.time()
        # S = uncurry(CX, 4, [2, 3]) \
        #     .mm(uncurry(CX, 4, [1, 3])) \
        #     .mm(uncurry(CX, 4, [0, 3])) \
        #     .mm(uncurry(X, 4, [0]))

        S = uncurry(X, 4, [0]) \
            .mm(uncurry(CX, 4, [2, 3])) \
            .mm(uncurry(CX, 4, [1, 3])) \
            .mm(uncurry(CX, 4, [0, 3]))

        # col0 = first summand
        # col1 = second summand
        # col2 = carry in
        # col3 = sum == 1 if number of preceding ones is unpair
        result_sum = [[0, 0, 0, 0],
                      [0, 0, 1, 1],
                      [0, 1, 0, 1],
                      [0, 1, 1, 0],
                      [1, 0, 0, 1],
                      [1, 0, 1, 0],
                      [1, 1, 0, 0],
                      [1, 1, 1, 1]]

        B = []
        n = 4
        N = 2 ** n
        pSum = matrix2perm(S)
        for j in range(N):
            b = int2bin(j, n)
            if b[3] == 1:
                B.append(b[:3] + int2bin(pSum[j], n)[3:])

        self.assertListEqual(result_sum, B)

        C = uncurry(TOFF, 4, [1, 2, 3]) \
            .mm(uncurry(TOFF, 4, [0, 2, 3])) \
            .mm(uncurry(TOFF, 4, [0, 1, 3]))

        # col0 = first summand
        # col1 = second summand
        # col2 = carry in
        # col3 = carry out == 1 if number of preceding ones is larger than one

        B = []
        pCarry = matrix2perm(C)
        for j in range(N):
            b = int2bin(j, n)
            if b[3] == 0:
                B.append(b[:3] + int2bin(pCarry[j], n)[3:])

        result_carry = [[0, 0, 0, 0],
                        [0, 0, 1, 0],
                        [0, 1, 0, 0],
                        [0, 1, 1, 1],
                        [1, 0, 0, 0],
                        [1, 0, 1, 1],
                        [1, 1, 0, 1],
                        [1, 1, 1, 1]]

        self.assertListEqual(result_carry, B)

        # apply S (sum) to qubits [0, 1, 2, 3]
        # and then C (carry) to qubits [0, 1, 2, 4]
        ADD = uncurry(C, 5, [0, 1, 2, 4]) \
            .mm(uncurry(S, 5, [0, 1, 2, 3]))

        B = []
        n = 5
        N = 2 ** n
        pADD = matrix2perm(ADD)
        for j in range(N):
            b = int2bin(j, n)
            if b[3] == 1 and b[4] == 0:
                B.append(b[:3] + int2bin(pADD[j], n)[3:])

        result_ADD = [[0, 0, 0, 0, 0],
                      [0, 0, 1, 1, 0],
                      [0, 1, 0, 1, 0],
                      [0, 1, 1, 0, 1],
                      [1, 0, 0, 1, 0],
                      [1, 0, 1, 0, 1],
                      [1, 1, 0, 0, 1],
                      [1, 1, 1, 1, 1]]

        self.assertListEqual(result_ADD, B)
        self.assertListEqual(pADD, qcatalogue.pADD)

    def test_curry(self):
        R = curry(qcatalogue.ADD, [[3, 1], [4, 0]])

        r = []
        for j in range(8):
            for i in range(32):
                if R[i, j] == 1:
                    r.append(int2bin(i, 5))

        p = [bin2int(b[:3]) for b in r]

        # q = inv_perm(p)
        # for i in q:
        #     print(r[i])

    def test_inc(self):
        R = CX.mm(uncurry(X, 2, [0])).mm(CX)
        self.assertListEqual(matrix2perm(R), matrix2perm(REV))
        A = CX2.mm(REV)
        self.assertListEqual(matrix2perm(A), matrix2perm(INC))
