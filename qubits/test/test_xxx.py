# j. siedersleben, Qubits and Quantum Computing, November 2023

import unittest

from scratch.scratch import *


class Test_basics(unittest.TestCase):
    def test_basis2bin(self):
        n = 5
        N = 2 ** n
        B = torch.eye(N, dtype=torch.int, device=dev)
        for i in range(N):
            x = basis2bin(B[i], n)
            k = bin2int(x)
            b = bin2basis(x)
            self.assertEqual(k, i)
            self.assertTrue(torch.equal(b, B[i]))

    def test_int2bin(self):
        n = 5
        for i in range(2 ** n):
            x = int2bin(i, n)
            k = bin2int(x)
            self.assertEqual(k, i)

    def test_permute(self):
        seq = [1, 0, 4, 2, 3]
        P = permute(seq)
        n = len(seq)
        for i in range(n):
            x = int2bin(i, n)  # x is i in binary
            y = [x[seq[j]] for j in range(n)]  # x with permuted bits
            # z = perm2matrix(seq).mv(tensor(x))  # z is x with permuted bits
            k = bin2int(y)  # k is the number i is permuted to
            # h = bin2int(z)                      # h is the number i is permuted to
            self.assertEqual(P[i], k)
            # self.assertEqual(h, k)

    def test_matrix2perm(self):
        seq = [1, 0, 4, 2, 3]
        P = perm2matrix(seq)
        teq = matrix2perm(P)
        self.assertEqual(seq, teq)

    def test_chunks(self):
        n = 4
        print(getChunks([0], n))
        print(getChunks([0, 1], n))
        print(getChunks([0, 2], n))
        print(getChunks([0, 3], n))
        print(getChunks([1, 2], n))
        print(getChunks([1, 3], n))
        print(getChunks([2, 3], n))
        print(getChunks([0, 1, 2], n))

    def test_CX(self):
        psi = torch.tensor(range(8), dtype=qtype, device=dev).view(-1, 1)
        CX01 = tmm(CX, I)
        phi01a = CX01.mm(psi)
        phi01b = CXfun(psi, 0, 1)
        self.assertTrue(torch.equal(phi01a, phi01b))

        CX12 = tmm(I, CX)
        phi12a = CX12.mm(psi)
        phi12b = CXfun(psi, 1, 2)
        self.assertTrue(torch.equal(phi12a, phi12b))

        phi02b = CXfun(psi, 0, 2)
        print(f'phi02b = ', {phi02b})

    def test_restrict(self):
        psi = tensor([0, 10, 20, 30], dtype=qtype, device=dev).view(-1, 1)

        X0 = restrict(X, [0])
        phi1 = X0(psi)
        Q = tmm(I, X)
        phi2 = Q.mm(psi)
        print([0])
        print(f'phi1 = ', {phi1})
        print(f'phi2 = ', {phi2})
        print()

        X1 = restrict(X, [1])
        phi1 = X1(psi)
        Q = tmm(X, I)
        phi2 = Q.mm(psi)
        print([1])
        print(f'phi1 = ', {phi1})
        print(f'phi2 = ', {phi2})
        print()

    def test_index_tuple(self):
        a = torch.arange(8).view(2, 2, 2)
        n = len(a.shape)

        args = [1, 2]  # Q to be applied to qubits 1 and 2
        k = len(args)
        not_args = [i for i in range(n) if i not in args]

        for j in range(2 ** k):
            b = int2bin(j, k)
            fixed_indices = [b[i] for i in range(k)]
            index_tuple = create_index_tuple(a.shape, args, fixed_indices)

        x = torch.randn(2, 3, 4, 5)  # Example tensor of shape (2, 3, 4, 5).

        # The positions where you want to have colons (slices).
        # For example, [0, :, 1, :] would be positions = [1, 3].
        positions = [1, 3]

        # Example usage with fixed indices 0 and 1 for dimensions 0 and 2.
        # shape will depend on the input tensor and the positions list.

        fixed_indices = [0, 1]
        index_tuple = create_index_tuple(x.shape, positions, fixed_indices)

        # Now use the index tuple to index into x.
        result = x[index_tuple]
        print(result.shape)  # The s
