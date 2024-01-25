# 4.4.2022
# 10.10,2023

# Teleportation and Superdense Coding with Pytorch

import unittest
from cmath import sqrt

import torch
from torch import tensor
from torch.linalg import vector_norm

from qapply import _apply, uncurry
from qbasics import bin2basis, tvv, tpow, qtype, dev
from qcatalogue import BELL, X, Z


class TestTele(unittest.TestCase):

    def test_superdense(self):
        """
        Superdense coding is about sending classical bits through a quantum channel.

        Victor has two qubits in the base state |0> and applies BELL to them.
        This yields the Bell state B00 = 1/sqrt(2) * (|00> + |11>) of two entangled qubits.
        He sends the first qubit to Alice and the second to Bob, both far away.

        Now, Alice wants to send two classical bits (a, b) to Bob through a quantum channel.

        This is how she does it: She applies Q = [X**b, Z**a] to the qubit received form Victor.
        Then she sends the resulting qubit to Bob (that's the quantum channel, limited by the speed of light).
        Bob applies BELL.T to the combination of the qubit received and his own, which are entangled.
        This gives him |a, b>. That's superdense coding.
        """

        # state0 is the base state |00>
        state0 = bin2basis([0, 0])
        # state0 = bin2basis([1, 1])

        # state1 is the Bell state B00 = 1/sqrt(2) * (|00> + |11>)
        state1 = BELL.mv(state0)

        for a in range(2):
            for b in range(2):
                message = bin2basis([a, b])

                # Alice encodes a and b as state2
                Xb = uncurry(tpow(X, b), 2, [0])
                Za = uncurry(tpow(Z, a), 2, [0])
                state2 = Za.mv(Xb.mv(state1))

                # She sends state2 to Bob who decodes it by applying BELL.T
                # Bob sees state3 = BELL.T * state2 = |a, b> = message
                state3 = BELL.T.mv(state2)
                self.assertTrue(torch.allclose(state3, message))

    def test_teleportation(self):
        """
        Teleportation is about sending qubits through a conventional channel. Here is the setup:
        Alice has one arbitrary qubit |message>. She also has two qubits in the base state |0>.
        She applies (I, BELL) to the three qubits, resulting in three entangled qubits in a
        superposition of 8 states. Now, Alice takes the first two qubits and flies far away,
        say to the moon. Bob stays at home, and keeps the third qubit.

        The question is: how can Alice send her qubit |message> to Bob? And the answer is yes, it's easy:
        First she applies BELL.T to her qubits, which amounts to applying (BELL.T, I) to the three
        qubits. Then she measures her two qubits and sends the result (a, b) to Bob.
        Bob will be able to reconstruct Alice's original qubit |message> by applying X**b and Z**a to his qubit.
        That's what teleportation is.

        To summarize: Teleportation allows sending qubits through a conventional channel
        provided that sender and receiver share entangled qubits,
        i.e. they (the qubits) must have met before.

        A few comments are in order:
        1. The three qubits are entangled, so the measurement of one of them
        gives information about the state of the others across any distance.
        2. It is by no means obvious how entanglement survives long trips.
        3. We assume that Alice can send the two classical bits (a, b) to Bob via any channel.
        The speed is obviously limited by the speed of light.
        4. Teleportation is instantaneous, but classical communication is not.
        5. Teleportation is not cloning, because the original qubit is destroyed.
        """

        # print("\n\nTeleportation\n")

        # message is an arbitrary qubit to be teleported.
        a0 = 0.6
        a1 = sqrt(1 - a0 ** 2)
        message = tensor([a0, a1], dtype=qtype, device=dev)

        if vector_norm(message) != 1:
            raise ValueError(f"norm(message) = {vector_norm(message)} != 1")

        # Alice and Bob start with |message, 0, 0>
        # state 0 = [a0, 0, 0, 0, a1, 0, 0, 0]
        state0 = tvv(message, bin2basis([0, 0]))

        # They apply BELL to the last two qubits which yields
        # state1 = [a0, 0, 0, a0, a1, 0, 0, a1]
        state1 = _apply(BELL, state0, [1, 2])

        # Alice takes the first two qubits and flies to the moon.
        # There she applies BELL.T to her qubits which yields
        # state2 = [a0, a1, a1, a0, a0, -a1, -a1, a0]
        state2 = _apply(BELL.T, state1, [0, 1])

        # Now, Alice measures her qubits and sends the result (a, b) to Bob.
        # state2[a, b] is the state of Bob's qubit after Alice's measurement
        state2 = state2.view(2, 2, 2)

        # Whatever the outcome, Bob applies X**b and Z**a to his qubit.
        # Note that state2[a, b] is the state of Bob's qubit after Alice's measurement,
        # which we normalize by dividing by norm(state2[a, b]).
        # So, he applies [X**b, Z**a] to state2, and gets finally |state3>
        # which equals Alice's original |message>.
        for a in range(2):
            for b in range(2):
                s2 = state2[a, b]
                s2 = s2 / vector_norm(s2)
                Xb = tpow(X, b)
                Za = tpow(Z, a)
                state3 = Za.mv(Xb.mv(s2))
                self.assertTrue(torch.allclose(state3, message))

    def test_teleportation_concise(self):
        # the same story, more concise

        # message is an arbitrary qubit to be teleported.
        a0 = 0.6
        a1 = sqrt(1 - a0 ** 2)
        message = tensor([a0, a1], dtype=qtype, device=dev)

        if vector_norm(message) != 1:
            raise ValueError(f"norm(message) = {vector_norm(message)} != 1")

        # Alice and Bob start with |message, 0, 0>
        # state 0 = [a0, 0, 0, 0, a1, 0, 0, 0]
        state0 = tvv(message, bin2basis([0, 0]))

        TELE = uncurry(BELL.T, 3, [0, 1]) \
            .mm(uncurry(BELL, 3, [1, 2]))

        state2 = TELE.mv(state0)

        for a in range(2):
            for b in range(2):
                s2 = state2.view(2, 2, 2)[a, b]
                s2 = s2 / vector_norm(s2)
                Xb = tpow(X, b)
                Za = tpow(Z, a)
                state3 = Za.mv(Xb.mv(s2))
                self.assertTrue(torch.allclose(state3, message))
