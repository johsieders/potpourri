# j. siedersleben, Qubits and Quantum Computing, November 2023

import time
import unittest

from qgates import *


class TestPrograms(unittest.TestCase):
    def test_add(self):
        start = time.time()
        S = qgate(X, 4, [0]) \
            .mm(qgate(CX, 4, [0, 3])) \
            .mm(qgate(CX, 4, [1, 3])) \
            .mm(qgate(CX, 4, [2, 3]))

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
        perm = matrix2perm(S)
        for j in range(N):
            b = int2bin(j, n)
            if b[3] == 1:
                B.append(b[:3] + int2bin(perm[j], n)[3:])

        self.assertListEqual(result_sum, B)

        C = qgate(TOFF, 4, [0, 1, 3]) \
            .mm(qgate(TOFF, 4, [0, 2, 3])) \
            .mm(qgate(TOFF, 4, [1, 2, 3]))

        # col0 = first summand
        # col1 = second summand
        # col2 = carry in
        # col3 = carry out == 1 if number of preceding ones is larger than one

        B = []
        perm = matrix2perm(C)
        for j in range(N):
            b = int2bin(j, n)
            if b[3] == 0:
                B.append(b[:3] + int2bin(perm[j], n)[3:])

        result_carry = [[0, 0, 0, 0],
                        [0, 0, 1, 0],
                        [0, 1, 0, 0],
                        [0, 1, 1, 1],
                        [1, 0, 0, 0],
                        [1, 0, 1, 1],
                        [1, 1, 0, 1],
                        [1, 1, 1, 1]]

        self.assertListEqual(result_carry, B)

        # apply S (sum) to qbits [0, 1, 2, 3]
        # and then C (carry) to qbits [0, 1, 2, 4]
        ADD = qgate(C, 5, [0, 1, 2, 4]) \
            .mm(qgate(S, 5, [0, 1, 2, 3]))

        B = []
        n = 5
        N = 2 ** n
        perm = matrix2perm(ADD)
        for j in range(N):
            b = int2bin(j, n)
            if b[3] == 1 and b[4] == 0:
                B.append(b[:3] + int2bin(perm[j], n)[3:])

        result_ADD = [[0, 0, 0, 0, 0],
                      [0, 0, 1, 1, 0],
                      [0, 1, 0, 1, 0],
                      [0, 1, 1, 0, 1],
                      [1, 0, 0, 1, 0],
                      [1, 0, 1, 0, 1],
                      [1, 1, 0, 0, 1],
                      [1, 1, 1, 1, 1]]

        self.assertListEqual(result_ADD, B)

        # start = time.time()
        # inc = qgate(X, 5, [0]) \
        #     .mm(qgate(CX, 5, [1, 3])) \
        #     .mm(qgate(CX, 5, [2, 3])) \
        #     .mm(qgate(TOFF, 5, [0, 1, 4])) \
        #     .mm(qgate(TOFF, 5, [0, 2, 4])) \
        #     .mm(qgate(TOFF, 5, [1, 2, 4]))
        # end = time.time()
        # print(end - start)

        # start = time.time()
        # self.assertListEqual(matrix2perm(inc), matrix2perm(inc2))
        # end = time.time()
        # print(end - start)
        # print(matrix2perm(inc))

    def test_inc(self):
        R = CX.mm(qgate(X, 2, [0])).mm(CX)
        self.assertListEqual(matrix2perm(R), matrix2perm(REV))
        A = CX2.mm(REV)
        self.assertListEqual(matrix2perm(A), matrix2perm(INC))
