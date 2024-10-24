# j.siedersleben
# fasttrack to professional programming
# lesson 1: warm up
# 15.11.2020


# from __future__ import annotations
import sys
from typing import List, Tuple, Union, Callable, Sequence, NewType

# from collections.abc import Sequence

Cid = NewType('cid', int)

Interval = NewType('Interval', Tuple[int, int])


def func0(xs: Sequence[int]) -> int:
    return sum(xs)


def func1(xs: List[int]) -> int:
    return sum(xs)


def func2(x: Union[int, str]) -> int:
    return x if type(x) is int else ord(x)


def func3(x: int) -> Callable[[int], int]:
    return lambda y: x + y


if __name__ == '__main__':
    iv = Interval((2, 3))
    print(iv)
    print(sys.version)

    s = func1([2, 3, 4])
    print(s)

    a = func2('a')
    print(a)

    f = func3(7)
    print(f(8))
