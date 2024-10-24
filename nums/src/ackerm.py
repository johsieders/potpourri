from _collections_abc import Callable
from typing import Any


# from The Little Typer p. 70 ff
def which_Nat(target: int, base: int, step: Callable[int, Any]) -> int:
    return base if target == 0 else step(target - 1)


def iter_Nat(target: int, base: int, step: Callable[Any, Any]) -> int:
    return base if target == 0 else step(iter_Nat(target - 1, base, step))


def rec_Nat(target: int, base: int, step: Callable[Any, Any]) -> int:
    return base if target == 0 else step(target - 1, rec_Nat(target - 1, base, step))


step_pls = lambda n: n + 1
pls = lambda a, b: iter_Nat(a, b, step_pls)

step_gauss = lambda a, b: a + b + 1
gauss = lambda n: rec_Nat(n, 0, step_gauss)


def ackermann(m: int, n: int) -> int:
    """
    :param m: an integer greater than or equal to 0
    :param n: an integer greater than or equal to 0
    :return: the ackermann(m, n)
    """
    if m == 0:
        return 2 * n + 1
    elif n == 0:
        return ackermann(m - 1, 1)
    else:
        return ackermann(m - 1, ackermann(m, n - 1))
