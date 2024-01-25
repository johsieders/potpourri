from bisect import bisect_right
from collections.abc import Callable, Iterable, Iterator
from functools import reduce


def fmerge(op: Callable, *fs: Iterable) -> Iterator:
    """
    fs: an iterable of step functions f
    returns a new step function F stepping at each step of any input function
    defined by F(x) = fun(*fs(x))
    """

    def weak(xs):
        ys = [x for x in xs if x is not None]
        return reduce(op, ys) if ys else None

    fs = [iter(f) for f in fs]

    val = {}
    head = {}.fromkeys(fs)  # dictionary of last read entries, key = f

    lastval = []  # any value not occurring in one of the f

    while True:
        for f in fs:  # fill heads by reading next (step, value)
            if head[f] is None:
                head[f] = next(f, None)

        hs = [h[0] for h in iter(head.values()) if h]
        if hs:  # determine m = next step
            try:
                im = hs.index(None)
                m = None
            except ValueError:
                im = min(range(len(head)), key=lambda h: h[0])
                m = head[im][0]
        else:  # all f are done
            return head[]

        for f in fs:  # update values
            if head[f] and head[f][0] == m:
                val[f] = head[f][1]
                head[f] = None
                break

        v = weak(iter(val.values()))
        if v != lastval:  # check if value has changed
            lastval = v
            yield m, v


class Stepfun:
    """ step functions are stepwise constant. They are given by a list
        (step, value). Step functions are assumed to be right-continuous.
        The first step is always at -oo represented by None.
        Step functions are constant from and including the last step until
        +oo.
        Intervals where the function is undefined are indicated by None.
        Example: The list ((None, None), (0, 100), (10, 200), (20, None))
        defines a function which is 100 on the interval [0, 10),
        200 on [10, 20) and undefined elsewhere.
        Steps must be non-descending.
        The constructor does the following:
        Of n equal steps the last one wins: [.., (0, 10), (0, 20)] is the same as [.., (0, 20)]
        Of n equal values, the first one wins: [.., (0, 10), (5, 10)] is the same as [.., (0, 10)]


        __call__(x) returns the function value at x
    """

    def __init__(self, sf):
        sf = iter(sf)
        self.steps = []
        self.values = []
        laststep, lastval = next(sf)
        if laststep is not None:
            raise ValueError
        self.steps.append(laststep)
        self.values.append(lastval)
        for s, v in sf:
            if laststep is not None and s < laststep:
                raise ValueError
            if s == laststep:
                self.values[-1] = v
                lastval = v
            elif v != lastval:
                self.steps.append(s)
                self.values.append(v)
                laststep = s
                lastval = v

    def __call__(self, x):
        i = bisect_right(self.steps, x, lo=1) - 1
        return self.values[i]

    def __iter__(self):
        return zip(self.steps, self.values)

    def fmerge(self, op: Callable, *fs: Iterable):
        return fmerge(op, self, fs)
