# 4.4.2022

# Quantum Computing with Pytorch

from cmath import sqrt

from torch import tensor

from qbits.quantum import CX, H, I, X, Z, tmm, tpow, apply, bin2basis, qtype

BELL = CX.mm(tmm(H, I))
TELE = [tmm(I, BELL), tmm(BELL.T, I)]  # BELL.T == BELL ** (-1)


def DENSE(a, b):
    return [BELL, tmm(tpow(X, a), I), tmm(tpow(Z, b), I), BELL.T]


def superdense():
    print("\n\nSuperdense Coding\n")

    # Superdense coding: send classical bits (a and b) through a quantum channel
    # Alice takes the first qubit and applies X**a and Z**b to it.
    # She sends the resulting qbit to Bob.
    # Bob sees |a, b>

    psi = bin2basis([0, 0])
    for a in range(2):
        for b in range(2):
            phi = apply(DENSE(a, b), psi)
            print(phi)


def teleportation():
    print("\n\nTeleportation\n")

    # Teleportation: send qubits through a conventional channel
    # Alice takes the two qubits (|phi> and the first leaving B), applies B.T to it,
    # gets the base state |a, b> and sends it to Bob.
    # Bob applies applies X**a and Z**b to his qubit and gets |phi>

    alpha = 0.1
    psi0 = tensor([alpha, sqrt(1 - alpha ** 2)], dtype=qtype).view(-1, 1)
    psi1 = bin2basis([0, 0])
    psi = tmm(psi0, psi1)
    phi = apply(TELE, psi).view(2, 2, 2)

    for a in range(2):
        for b in range(2):
            Q = [2 * tpow(X, b), tpow(Z, a)]
            phi0 = apply(Q, phi[a, b])
            print((phi0 - psi0).view(1, -1))


if __name__ == '__main__':
    superdense()
    teleportation()
