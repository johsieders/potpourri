# 4.4.2022
# 10.10,2023

# Teleportation and Superdense Coding with Pytorch

from cmath import sqrt

from torch import tensor

from scratch.quantum import BELL, I, X, Z, tmm, tpow, applyX, bin2basis, norm, qtype


def superdense():
    """
    Superdense coding is about sending classical bits through a quantum channel.

    Victor has two qbits in the base state |0> and applies BELL to them.
    This yields the Bell state B00 = 1/sqrt(2) * (|00> + |11>) of two entangled qbits.
    He sends the first qubit to Alice and the second to Bob, both far away.

    Now, Alice wants to send two classical bits (a, b) to Bob through a quantum channel.

    This is how she does it: She applies Q = [X**a, Z**b] to the qubit received form Victor.
    Then she sends the resulting qubit to Bob (that's the quantum channel, limited by the speed of light).
    Bob applies BELL.T to the combination of the qubit received and his own, which are entangled.
    This gives him |a, b>. That's superdense coding.
    """

    print("\n\nSuperdense Coding\n")

    # state0 is the base state |00>
    state0 = bin2basis([0, 0])
    # state0 = bin2basis([1, 1])

    # state1 is the Bell state B00 = 1/sqrt(2) * (|00> + |11>)
    state1 = BELL.mm(state0)

    for a in range(2):
        for b in range(2):
            message = bin2basis([a, b])
            # Alice encodes a and b as
            Q = [tmm(tpow(X, b), I), tmm(tpow(Z, a), I)]

            # and applies Q to state1
            state2 = applyX(Q, state1)

            # state2 is sent to Bob who decodes it by applying BELL.T
            # Bob sees state3 = BELL.T * state2 = |a, b> = message
            state3 = BELL.T.mm(state2)
            print(state3 - message)  # should be zero


def teleportation():
    """
    Teleportation is about sending qbits through a conventional channel. Here is the setup:
    Alice has one arbitrary qubit |psi>. She also has two qbits in the base state |0>.
    She applies (I, BELL) to the three qbits, resulting in three entangled qbits in a
    superposition of 8 states. Now, Alice takes the first two qbits and flies far away,
    say to the moon. Bob stays at home, and keeps the third qubit.

    The question is: how can Alice send her qubit |psi> to Bob? And the answer is yes, it's easy:
    First she applies BELL.T to her qbits, which amounts to applying (BELL.T, I) to the three
    qbits. Then she measures her two qbits and sends the result (a, b) to Bob.
    Bob will be able to reconstruct Alice's original qubit |psi> by applying X**b and Z**a to his qubit.
    That's what teleportation is.

    To summarize: Teleportation allows sending qbits through a conventional channel
    provided that sender and receiver share entangled qbits,
    i.e. they (the qbits) must have met before.

    A few comments are in order:
    1. The three qbits are entangled, so the measurement of one of them
    gives information about the state of the others across any distance.
    2. It is by no means obvious how entanglement survives long trips.
    3. We assume that Alice can send the two classical bits (a, b) to Bob via any channel.
    The speed is obviously limited by the speed of light.
    4. Teleportation is instantaneous, but classical communication is not.
    5. Teleportation is not cloning, because the original qubit is destroyed.
    """

    print("\n\nTeleportation\n")

    # psi is an arbitrary qubit to be teleported.
    a0 = 0.6
    a1 = sqrt(1 - a0 ** 2)
    psi = tensor([a0, a1], dtype=qtype).view(-1, 1)

    if norm(psi) != 1:
        raise ValueError(f"norm(psi) = {norm(psi)} != 1")

    # Alice and Bob start with |psi, 0, 0>
    # state 0 = [a0, 0, 0, 0, a1, 0, 0, 0]
    state0 = tmm(psi, bin2basis([0, 0]))

    # They apply BELL to the last two qbits which yields
    # state 1 = [a0, 0, 0, a0, a1, 0, 0, a1]
    state1 = tmm(I, BELL).mm(state0)

    # Alice takes the first two qbits and flies to the moon.
    # There she applies BELL.T to her qbits which yields
    # state 2 = [a0, a1, a1, a0, a0, -a1, -a1, a0]
    state2 = tmm(BELL.T, I).mm(state1)

    # Now, Alice measures her qbits and sends the result (a, b) to Bob.
    # state2[a, b] is the state of Bob's qubit after Alice's measurement
    state2 = state2.view(2, 2, 2)

    # Whatever the outcome, Bob applies X**b and Z**a to his qubit.
    # Note that state2[a, b] is the state of Bob's qubit after Alice's measurement,
    # which we normalize by dividing by q = norm(state2[a, b]).
    # So, he applies Q = [X**b, Z**a] to state2[a, b] / q,
    # and gets finally |phi> which equals Alice's original |psi>.
    for a in range(2):
        for b in range(2):
            q = norm(state2[a, b])  # should be 0.5
            Q = [tpow(X, b), tpow(Z, a)]
            phi = applyX(Q, state2[a, b] / q)
            print((phi - psi).view(1, -1))  # should be zero


if __name__ == '__main__':
    superdense()
    # teleportation()
