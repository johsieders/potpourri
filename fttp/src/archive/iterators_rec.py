## trying to understand iterators
## js 14.8.2004
## completely reworked 1/9/2011


def const(c):
    """ recursive generator yielding the constant c
        This of absolutly no use. It is our first example
        of recursive iterators.
    """
    yield c
    tail = const(c)
    while True:
        yield next(tail)


def multiply(s, t):
    """ s, t : series on a ring, assuming iter(s), iter(t) work
        mul returns the product of s and t
        if len(s) == 0 or len(t) == 0: StopIteration at first call of next
        works fine with finite series (i.e. polynoms) and infinite ones.
    """
    s = iter(s)
    t_, t = tee(iter(t))  ## t saved in t_

    s0 = next(s)  ## now s = tail(s)
    t0 = next(t)  ## now t = tail(t)
    yield s0 * t0

    tail = (wadd(a, b) for a, b in wzip((s0 * x for x in t), multiply(s, t_)))
    while True:
        yield next(tail)


square = lambda t: multiply(*tee(t))


def inverse(s):
    """ s : series on a field;
        if len(s) == 0: StopIteration at fist call of next
        if len(s) > 0:  s[0] != 0, otherwise division by zero
        returns the inv t of s
        postcondition: mul(s, t) = (1, 0, 0, ...)
    """
    s, s_ = tee(iter(s))  ## s saved in s_

    s0 = next(s)  ## now s = tail(s)
    t0 = s0 / s0 / s0  ## s0/s0 = one
    yield t0

    tail = multiply(s, inverse(s_))
    while True:
        yield -t0 * next(tail)


def divide(s, t):
    return multiply(s, inverse(t))


def merge(*ts):
    """ ts is an iterable of iterables
        merges n iterables into one.
	This is a weak merge: It stops only
	when the longest iterator is at end.
    """

    ts = [iter(t) for t in ts]
    xs = next(wzip(*ts))  ## StopIteration if all t at end
    xs = [x for x in xs if x is not None]
    m = min(xs)
    yield m

    for i, x in enumerate(xs):
        if x is m:
            break
    del xs[i]  ## remove first occurrence of min

    ts += [[x] for x in xs if x is not None]
    tail = merge(*ts)
    while True:
        yield next(tail)


def hamming(*ps):
    """ ps = (p0, p1, p2, ..) contains one or more integers, generally primes
        hamming returns all multiples of p0, p1, p2, ..
    """
    yield 1

    tail = merge(*[(p * t for t in hamming(*ps)) for p in ps])
    while True:
        yield next(tail)
