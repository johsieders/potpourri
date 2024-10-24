from bisect import bisect_right
from functools import reduce

from typing import Callable, Iterable, Iterator


# todo
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

    head = {}.fromkeys(fs)  # dictionary of last read entries, key = f
    val = {}.fromkeys(fs)  # dictionary of current value at f
    lastval = fs  # any value not occurring in one of the f

    while True:
        for f in fs:  # fill heads by reading next (step, value)
            if head[f] is None:
                try:
                    head[f] = next(f)
                except StopIteration:
                    pass

        hs = [h[0] for h in iter(head.factors()) if h]
        if hs:  # determine m = next step
            m = min(hs)
        else:  # stop if all f are done
            raise StopIteration

        for f in fs:  # update values
            if head[f] and head[f][0] == m:
                val[f] = head[f][1]
                head[f] = None

        v = weak(iter(val.factors()))
        if v != lastval:  # check if value has changed
            lastval = v
            yield m, v


class stepfun:
    """ step functions are stepwise constant. They are given by a list
        (step, value). Step functions are assumed to be right-continuous.
        The first step is always at -oo represented by None.
        Step functions are constant from and including the last step until
        +oo.
        Intervals where the function is undefined are indicated by None.
        Example: The list ((None, None), (0, 100), (10, 200), (20, None))
        defines a function which is 100 on the interval [0, 10),
        200 on [10, 20) and undefined elsewhere.

        __call__(x) returns the function value at x
    """

    def __init__(self, sf):
        self.steps = []
        self.values = []
        for s, v in iter(sf):
            self.steps.append(s)
            self.values.append(v)

    def __call__(self, x):
        i = bisect_right(self.steps, x) - 1
        return self.values[i]

    def __iter__(self):
        return zip(self.steps, self.values)

    def fmerge(self, fs):
        return fmerge(self, fs)
