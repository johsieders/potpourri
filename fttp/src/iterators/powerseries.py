# trying to understand iterators
# js 14.8.2004
# completely reworked 1/7/2011
# merge revised, fmerge added 3/6/2013

from itertools import tee, zip_longest
from operator import add, sub

from warmingup.types_ import Iterator


def weak(op):
    def aux(x, y):
        if not x:
            return y
        elif not y:
            return x
        else:
            return op(x, y)

    return aux


def add_iter(s, t) -> Iterator:
    return (weak(add)(a, b) for (a, b) in zip_longest(s, t))


def sub_iter(s, t) -> Iterator:
    return (weak(sub)(a, b) for (a, b) in zip_longest(s, t))


def mul_iter(s, t) -> Iterator:
    """
    :param s: series on a ring, assuming iter(s), iter(t) work
    :param t: series on a ring, assuming iter(s), iter(t) work
    :return: product of s and t

    if len(s) == 0 or len(t) == 0: StopIteration at first call of next
    works fine with finite series (i.e. polynomials) and infinite ones.
    """

    s, t = iter(s), iter(t)
    xs, xt = [], []  # store elements read from s and t
    k = 0  # count yielded elements

    while True:
        try:
            xs.append(next(s))
        except StopIteration:
            pass
        try:
            xt.append(next(t))
        except StopIteration:
            pass

        x = None  # start without using 0
        lb = max((0, k - len(xt) + 1))  # stay within rectangle
        ub = min((k + 1, len(xs)))
        for i in range(lb, ub):
            if x is None:
                x = xs[i] * xt[k - i]
            else:
                x += xs[i] * xt[k - i]

        if x is None:
            raise StopIteration
        else:
            k += 1  # that many elements yielded
            yield x

    # This code does basically this:
    #
    # x = 0
    # for i in range(len(xs)):
    #    x += xs[i] * xt[k-i]
    #
    # zeroing missing elements of xs and xt.
    # The values lb (lower bound) and ub(upper bound)
    # describe the rectangle of indices being considered.


def square(t):
    return mul_iter(*tee(t, 2))


def inv_iter(s):
    """
    s : series on a field;
    if len(s) == 0: StopIteration at fist call of next
    if len(s) > 0:  s[0] != 0, otherwise division by zero
    returns the inv t of s
    postcondition: mul(s, t) = (1, 0, 0, ...)
    """
    s = iter(s)  # the iterator to be inverted
    xs, xt = [], []

    x = next(s)  # may raise StopIteration
    one = x / x  # there is no 1
    zero = x - x  # there is no 0

    xs.append(x)  # read part of s
    xt.append(one / x)  # coefficients of t=1/s
    yield xt[-1]

    while True:
        try:
            xs.append(next(s))
        except StopIteration:
            xs.append(zero)

        y = zero
        for (i, x) in enumerate(xt):
            y += x * xs[-i - 1]

        xt.append(-y * xt[0])
        yield xt[-1]


def div_iter(s, t):
    return mul_iter(s, inv_iter(t))


class Powerseries(Iterator):
    # todo
    def __init__(self, t):
        self.iterator = t

    def __next__(self):
        return next(self.iterator)

    __add__ = add_iter
    __sub__ = sub_iter
    __mul__ = mul_iter
    __invert__ = inv_iter
    __truediv__ = div_iter
