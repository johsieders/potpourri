# Python time iterators
# js, 15.8.04

from timeit import *

if __name__ == '__main__':
    t = Timer('take(100, const(8))', 'from iterators import const; from it.util import take')
    result = t.repeat(3, 100)
    print('standard iterator:  100 * take(100, const(8)) : ', result)

    t = Timer('take(100, const(8))', 'from iterators_rec import const; from it.util import take')
    result = t.repeat(3, 100)
    print('recursive iterator: 100 * take(100, const(8)) : ', result)
