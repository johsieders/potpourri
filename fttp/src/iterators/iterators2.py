# j.siedersleben
# fasttrack to professional programming
# lesson 6: iterators
# 28.12.2020


from collections import deque
from itertools import chain, cycle, islice
from operator import add

from nums import Number
from warmingup.types import Iterable, Iterator, Callable, Sequence


def yielding1(n: int):
    """
    simplest example of yield
    """
    for k in range(n):
        yield k


def sending1(n):
    """
    :param n: an integer
    :return: depends on what you send
    """
    k = (yield n)  # first call of next yields n
    if k is not None:
        n = k
    else:
        n += 1
    yield n  # second call of next yields n+1 or k


def sending3(i0):
    i1 = (yield i0)  # yield returns what is sent, otherwise None
    yield i1  # sent message is ignored
    i3 = (yield i1)
    yield i3
    print('values received  ', i0, i1, i3)
    yield None


def counter(maximum) -> Iterator[int]:
    i = 0
    while i < maximum:
        val = (yield i)
        # If value provided, change counter
        if val is not None:
            i = val
        else:
            i += 1


def const(c: any) -> Iterator[any]:
    """
    :param c: any
    :return: a constant iterator
    """
    yield c
    yield from const(c)


def naturals(start: int = 0) -> Iterator[int]:
    """
    :param start: an integer
    :return: the naturals
    """
    while True:
        yield start
        start += 1


def naturals1(start: int = 0) -> Iterator[int]:
    """
    :param start: an integer
    :return: the naturals
    """
    yield start
    yield from naturals(start + 1)


def take(t: Iterator, n: int) -> list:
    """
    :param t: an iterator
    :param n: number of elements requested
    :return: list of first k elements with k = min(n, len(t))
    This avoids fiddling with StopIteration
    """
    return list(islice(t, n))


def faculty() -> Iterator[int]:
    """
    :return: un iterator yielding the factorials
    """
    factor = 1
    current = 1
    while True:
        yield current
        current *= factor
        factor += 1


def fun(f: Callable, *args: any) -> Iterator[any]:
    """
    :param f: a function taking k arguments, e.g. k = 2
    :param args: k arguments accepted by f
    :return: n iterator yielding arg0, arg1, f(arg0, arg1), f(arg1, f(arg0, arg1)), ..
    """
    for arg in args:
        yield arg

    while True:
        args = args[1:] + (f(*args),)
        yield args[-1]


def ari(increment: Number, start: Number = 0) -> Iterator[Number]:
    """
    :param increment: any number
    :param start: any number, starting value
    :return: the arithmetic series staring at start
    """
    return fun(lambda x: x + increment, start)


def geo(factor: Number, start: Number = 1) -> Iterator[Number]:
    """
    :param factor: any number
    :param start: any number, starting value
    :return: the geometric series staring at start
    """
    return fun(lambda x: x * factor, start)


def alternate() -> Iterator[Number]:
    a = ari(1)
    g = geo(2)
    while True:
        yield next(a)
        yield next(g)


def fibo() -> Iterator[int]:
    """
    :return: iterator yielding the fibonacci series
    """
    return fun(add, 1, 1)


class Fibo(object):
    def __iter__(self):
        return fibo()


def exp_taylor() -> Iterator[float]:
    """
    :return: iterator yielding the coefficients of the Taylor series of exp_taylor
    """
    return (1 / k for k in faculty())


def sin_taylor() -> Iterator[float]:
    """
    :return: iterator yielding the coefficients of the Taylor series of sin
    """
    return (a * b for a, b in zip(cycle((0, 1, 0, -1)), exp_taylor()))


def cos_taylor() -> Iterator[float]:
    """
    :return: iterator yielding the coefficients of the Taylor series of sin
    """
    return (a * b for a, b in zip(cycle((1, 0, -1, 0)), exp_taylor()))


def skip_duplicates(t: Iterable) -> Iterator:
    """"
    :param t: an iterator
    :return: an iterator skipping successive duplicates
    """
    t = iter(t)
    last = next(t)
    yield last

    while True:
        x = next(t)
        if x != last:
            last = x
            yield last


def merge(*ts: Iterable) -> Iterator:
    """
    :param ts: a list of n non-descending iterables, n >= 0
    :return: merge of n iterables into one
    This is a weak merge:
    It doesn't stop before the longest iterator is exhausted
    """
    ts = [iter(t) for t in ts]
    heads = {}.fromkeys(ts)  # dictionary of last read entries, initially all None

    while True:
        # get first element of each iterable if there is one
        for t in ts:
            if heads[t] is None:
                h = take(t, 1)  # try to read next element
                heads[t] = h[0] if len(h) > 0 else None

        # get non-exhausted entries
        active_ts = [t for t in ts if heads[t] is not None]
        if not active_ts:  # no active entry left
            return
        else:
            # get non-exhausted entry with minimum value
            min_t = min(active_ts, key=lambda t: heads[t])
            yield heads[min_t]
            heads[min_t] = None  # to be updated on next loop


def merge1(s: Iterable, t: Iterable) -> Iterator:
    """
    :param s: a non-descending iterable,
    :param t: a non-descending iterable,
    :return: merge of s and t into one
    This is a weak merge:
    It doesn't stop before the longest iterator is exhausted
    Elegant but inefficient (max recursion depth)
    """
    s, t = iter(s), iter(t)  # get iterator from iterable
    head_s, head_t = take(s, 1), take(t, 1)  # take first element

    if not head_s:
        yield from chain(head_t, t)  # restore first element of t
    elif not head_t:
        yield from chain(head_s, s)  # restore first element of s
    elif head_s[0] <= head_t[0]:
        yield head_s[0]
        yield from merge1(s, chain(head_t, t))
    else:
        yield head_t[0]
        yield from merge1(chain(head_s, s), t)


def tee1(t: Iterable, n: int = 2) -> Sequence[Iterator]:
    """
    :param t: an iterable
    :param n: number of forks
    :return: n copies of t, to be iterated on independently
    This is a remake of itertools.tee
    """
    t = iter(t)
    buffer = [deque() for _ in range(n)]

    def gen(q: deque) -> Iterator:
        while True:
            if not q:  # when the local deque is empty
                x = next(t)  # fetch a new value and
                for d in buffer:  # load x into buffer
                    d.append(x)
            yield q.popleft()

    return tuple(gen(d) for d in buffer)


def hamming(*ps: int) -> Iterator[int]:
    """
    :param ps: ps = (p0, p1, p2, ..) contains one or more integers, generally primes
    :return: an iterator yielding all multiples of p0, p1, p2, ..

    This solution follows Dijkstra: "An exercise attributed to R.W. Hamming":

    Let q be the sequence of multiples produced so far.
    Then append min{p*x | x in q, p in ps, p*x > max(q)} to q.
    The next number to be produced is min(q)
    """

    q = [1]  # q contains all nums produced so far
    while True:
        yield q[-1]
        mq = max(q)
        q.append(min([p * x for p in ps for x in q if p * x > mq]))
