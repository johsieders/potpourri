# 4.4.2022

# Quantum Computing with Pytorch


from math import pi, sqrt, asin, sin, cos

from torch import arange, eye, zeros

from scratch.quantum import H, I, U, X, applyX, tmm, tpow, bin2basis, int2bin, one_at, qtype, dev


def U__(f, n):
    """
    :param f: a binary function of n binary variables
    :param n: the number n >= 2, N = 2 ** n
    :return: the unitary (2*N x 2*N) matrix U(f)
    """
    N = 2 ** n
    U = zeros((2 * N, 2 * N), dtype=qtype, device=dev)
    for i in range(N):
        F = X if f(int2bin(i, n)) else I
        U[2 * i: 2 * i + 2, 2 * i: 2 * i + 2] = F
    return U


def V(n):
    result = -eye(2 ** n, dtype=qtype, device=dev)
    result[0, 0] = 1
    return result


def GROVER(f, n):
    k = int(pi * sqrt(2 ** n) / 4)
    Hn = tpow(H, n)
    H1 = tmm(Hn, H)
    Dn = Hn.mm(V(n)).mm(Hn)
    D1 = tmm(Dn, I)
    Uf = U(f, n)

    return [H1] + k * [Uf, D1]


def grover(n, val):
    # prepare GROVER
    f = one_at(val)
    G = GROVER(f, n)

    # prepare input psi1
    psi0 = bin2basis(n * [0])  # N
    xi = bin2basis([1])  # 2
    psi1 = tmm(psi0, xi)  # 2N

    # apply GROVER
    psi = applyX(G, psi1)

    # get output psi2
    psi2 = psi[2 * arange(2 ** n)] * sqrt(2)
    return psi2


def grover_(n):
    # Grover Algorithm
    print("\n\nGrover Algorithm\n")

    N = 2 ** n
    f = one_at(3)

    theta = asin(sqrt(1 / N))
    alpha0 = sin(theta)
    alpha1 = cos(theta)

    H1 = tpow(H, n + 1)  # 2N
    Uf = U(f, n)  # 2N
    V1 = V(n + 1)  # 2N
    D1 = H1.mm(V1).mm(H1)  # 2N

    tau0 = bin2basis(n * [0])  # N
    xi = bin2basis([1])  # 2
    tau1 = tmm(tau0, xi)  # 2N

    psi0 = H1.mm(tau1)  # psi0 = alpha0 * phi0 + alpha1 * phi1
    psi_ = Uf.mm(psi0)  # psi_ = -alpha0 * phi0 + alpha1 * phi1

    phi0 = 1 / 2 * (psi0 - psi_) / alpha0
    phi1 = 1 / 2 * (psi0 + psi_) / alpha1  # orthogonal to phi0

    qpsi0 = alpha0 * phi0 + alpha1 * phi1  # = psi0
    qpsi_ = -alpha0 * phi0 + alpha1 * phi1  # = psi_

    # orthogonality
    print('\n phi0 * phi1\n', phi0.T.mm(phi1))
    print('\n psi0 * psi_\n', psi0.T.mm(psi_))

    # phi0 , phi1
    print('\n phi0\n', phi0)
    print('\n phi1\n', phi1)

    # psi0 , qpsi0 must be equal
    print('\n psi0\n', psi0)
    print('\n qpsi0\n', qpsi0)

    # psi_, qpsi_ must be equal
    print('\n psi_\n', psi_)
    print('\n qpsi_\n', qpsi_)


def grover___(n, val, count):
    # Grover Algorithm

    f = one_at(val)

    Hn = tpow(H, n)  # 2N
    Uf = U(f, n)  # 2N
    Vn = V(n)  # N
    Dn = Hn.mm(Vn).mm(Hn)  # N
    D1 = tmm(Dn, I)  # 2 N

    psi0 = bin2basis(n * [0])  # N
    xi = bin2basis([1])  # N
    psi1 = tmm(Hn.mm(psi0), H.mm(xi))  # 2N

    for _ in range(count):
        psi2 = Uf.mm(psi1)
        psi1 = D1.mm(psi2)

    return psi1


if __name__ == '__main__':

    n = 8
    val = 1
    N = 2 ** n
    cmax = int(pi * sqrt(N) / 4)

    psi = None
    for cnt in range(cmax + 1):
        psi = grover___(n, val, cnt)

    print('\n', cmax)
    print(psi[2 * val].item())
    print(psi[2 * val + 2].item())
    print()

    # aux.norm = probability to get one of val, val+1
    aux = psi[[2 * val, 2 * val + 1]]
    print(aux)
    print(aux.norm())

    # psi2 = grover(n, val)

    #
    # print('\n', psi2[val].item())
    # print(psi2[val - 1].item())
