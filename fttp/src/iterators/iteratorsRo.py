## trying to understand iterators
## js 14.8.2004
## completely reworked 1/7/2011
## merge revised, fmerge added 3/6/2013


def multiply(s, t):
    """ s, t : series on a ring, assuming iter(s), iter(t) work
        mul returns the product of s and t
        if len(s) == 0 or len(t) == 0: StopIteration at first call of next
        works fine with finite series (i.e. polynoms) and infinite ones.
    """
    s, t = iter(s), iter(t)
    xs, xt = [], []  ## store elements read from s and t
    k = 0  ## count yielded elements

    while True:
        try:
            xs.append(next(s))
        except StopIteration:
            pass
        try:
            xt.append(next(t))
        except StopIteration:
            pass

        x = None  ## start without using 0
        lb = max((0, k - len(xt) + 1))  ## stay within rectangle
        ub = min((k + 1, len(xs)))
        for i in range(lb, ub):
            if x is None:
                x = xs[i] * xt[k - i]
            else:
                x += xs[i] * xt[k - i]

        if x is None:
            raise StopIteration
        else:
            k += 1  ## that many elements yielded
            yield x

    ## This code does basically this:
    ## 
    ## x = 0
    ## for i in range(len(xs)):
    ##     x += xs[i] * xt[k-i]
    ##
    ## zeroing missing elements of xs and xt.
    ## The values lb (lower bound) and ub(upper bound)
    ## describe the rectangle of indices to be considered.


square = lambda s: multiply(*tee(s))


def inverse(s):
    """ s : series on a field;
        if len(s) == 0: StopIteration at fist call of next
        if len(s) > 0:  s[0] != 0, otherwise division by zero
        returns the inv t of s
        postcondition: mul(s, t) = (1, 0, 0, ...)
    """
    s = iter(s)  ## the iterator to be inverted
    xs, xt = [], []

    x = next(s)  ## may raise StopIteration
    one = x / x  ## there is no 1
    zero = x - x  ## there is no 0

    xs.append(x)  ## read part of s
    xt.append(one / x)  ## coefficients of t=1/s
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


def divide(s, t):
    return multiply(s, inverse(t))


def merge(*ts):
    """ ts is an iterable of iterables
        merges n iterables into one.
        This is a weak merge: It stops only
        when the longest iterator is exhausted        
    """

    ts = [iter(t) for t in ts]
    head = {}.fromkeys(ts)  ## dictionary of last read entries

    while True:
        for t in ts:
            if head[t] is None:
                try:
                    head[t] = (next(t),)  ## replace Nones
                except StopIteration:
                    pass

        hs = [h[0] for h in head.itervalues() if h]
        if hs:
            m = min(hs)
        else:  ## all ts are done
            raise StopIteration

        for t in ts:
            if head[t] and head[t][0] == m:  ## remove used t
                head[t] = None  ## but only once to keep duplicates
                break

        yield m


def fmerge(op, *fs):
    """ fs: an iterable of step functions f
        returns a new step function F stepping at each step of any input function
        defined by F(x) = fun(*fs(x))
    """

    def weak(xs):
        ys = [x for x in xs if x is not None]
        return reduce(op, ys) if ys else None

    fs = [iter(f) for f in fs]

    head = {}.fromkeys(fs)  ## dictionary of last read entries, key = f
    val = {}.fromkeys(fs)  ## dictionary of current value at f
    lastval = fs  ## any value not occurring in one of the f

    while True:
        for f in fs:  ## fill heads by reading next (step, value)
            if head[f] is None:
                try:
                    head[f] = next(f)
                except StopIteration:
                    pass

        hs = [h[0] for h in head.itervalues() if h]
        if hs:  ## determine m = next step
            m = min(hs)
        else:  ## stop if all f are done
            raise StopIteration

        for f in fs:  ## update values
            if head[f] and head[f][0] == m:
                val[f] = head[f][1]
                head[f] = None

        v = weak(val.itervalues())
        if v != lastval:  ## check if value has changed
            lastval = v
            yield m, v
