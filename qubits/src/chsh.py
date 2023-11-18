# js 18/10/2023


# Bell's Theorem with Pytorch
#

from cmath import sqrt

from torch import tensor

from scratch.quantum import BELL, X, Z, tmm, bin2basis


def expectancy(A: tensor, psi: tensor) -> float:
    """
    :param A: an (n x n) tensor (the observable)
    :param psi: a vector
    :return: <A>(psi) = <psi|A|psi> the expected measured value when A is applied to |psi>
    """
    result = psi.T.mm(A.mm(psi))
    return result.item()


def chsh(A0: tensor, A1: tensor, B0: tensor, B1: tensor, psi: tensor) -> float:
    """
    :param A0: an (n x n) tensor (Alice's first observable)
    :param A1: an (n x n) tensor (Alice's second observable)
    :param B0: an (n x n) tensor (Bob's first observable)
    :param B1: an (n x n) tensor (Bob's second observable)

    :param psi: a state
    :return: (E[A0, B0] + E[A0, B1] + E[A1, B0] - E[A1, B1])(psi)
    """

    return \
            expectancy(tmm(A0, B0), psi) + expectancy(tmm(A0, B1), psi) + \
            expectancy(tmm(A1, B0), psi) - expectancy(tmm(A1, B1), psi)


if __name__ == '__main__':
    A0 = Z
    A1 = X

    B0 = -1 / sqrt(2) * (X + Z)
    B1 = 1 / sqrt(2) * (X - Z)
    psi = BELL.mm(bin2basis([1, 1]))

    ex = chsh(A0, A1, B0, B1, psi)

    print(f"psi = {psi}")
    print(f"<A0, B0> + <A0, B1> + <A1, B0> - <A1, B1> = {ex} (should be 2*sqrt(2))")
