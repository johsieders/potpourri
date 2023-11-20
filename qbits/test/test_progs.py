# j. siedersleben, Qubits and Quantum Computing, November 2023

import time
import unittest

from qgates import *


class TestPrograms(unittest.TestCase):
    def test_inc(self):
        # start = time.time()
        # inc1 = qgate(X, 4, [0]) \
        #     .mm(qgate(CX, 4, [1, 3])) \
        #     .mm(qgate(CX, 4, [2, 3]))
        # inc2 = qgate(inc1, 5, [0, 1, 2, 3]) \
        #     .mm(qgate(TOFF, 5, [0, 1, 4])) \
        #     .mm(qgate(TOFF, 5, [0, 2, 4]))
        # end = time.time()
        # print(end - start)

        start = time.time()
        inc = qgate(X, 5, [0]) \
            .mm(qgate(CX, 5, [1, 3])) \
            .mm(qgate(CX, 5, [2, 3])) \
            .mm(qgate(TOFF, 5, [0, 1, 4])) \
            .mm(qgate(TOFF, 5, [0, 2, 4])) \
            .mm(qgate(TOFF, 5, [1, 2, 4]))
        end = time.time()
        print(end - start)

        # start = time.time()
        # self.assertListEqual(matrix2perm(inc), matrix2perm(inc2))
        # end = time.time()
        # print(end - start)
        print(matrix2perm(inc))

    def test_inc1(self):
        R = CX.mm(qgate(X, 2, [0])).mm(CX)
        self.assertListEqual(matrix2perm(R), matrix2perm(REV))
        A = CX2.mm(REV)
        self.assertListEqual(matrix2perm(A), matrix2perm(INC))
