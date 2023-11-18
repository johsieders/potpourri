## itertools.tee1(iterable, n=2)
## Return n independent iterators from a single iterable. Equivalent to:
from collections import deque


def tee(t, n=2):
    t = iter(t)
    deques = [deque() for _ in range(n)]

    def gen(mydeque):
        while True:
            if not mydeque:  # when the local deque is empty
                newval = next(t)  # fetch a new value and
                for d in deques:  # load it to all the deques
                    d.append(newval)
            yield mydeque.popleft()

    return tuple(gen(d) for d in deques)

## Once tee1() has made a split, the original iterable should not be used anywhere else;
## otherwise, the iterable could get advanced without the tee1 objects being informed.

## This itertool may require significant auxiliary storage 
##(depending on how much temporary data needs to be stored). 
## In general, if one iterator uses most or all of the data before another iterator starts, 
## it is faster to use list() instead of tee1().
