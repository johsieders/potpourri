# Python time iterators
# js, 8.6.04

from timeit import *

if __name__ == '__main__':
    t = Timer('take(50, hamming__(2,3,5))', 'from iterators import hamming__, take')
    result = t.repeat(2, 20)
    print('20*take(50, hamming-new(2,3,5)) : ', result)

    ##    t = Timer('take(50, hamming(2,3,5))', 'from iterators_new import hamming, take')
    ##    result = t.repeat(2, 20)
    ##    print '20*take(50, hamming-newnew(2,3,5)) : ', result

    t = Timer('take(50, hamming(2,3,5))', 'from iterators_classic import hamming, take')
    result = t.repeat(2, 20)
    print('20*take(50, hamming-classic(2,3,5)) : ', result)

    print()

    t = Timer('take(100, product(isin(), icos()))', 'from iterators import product, isin, icos, take')
    result = t.repeat(2, 20)
    print('20*take(100, product-new(isin(), icos())) : ', result)

    ##    t = Timer('take(50, product(isin(), icos()))', 'from iterators_new import product, isin, icos, take')
    ##    result = t.repeat(2, 20)
    ##    print '20*take(50, product-newnew(isin(), icos())) : ', result

    t = Timer('take(100, product(isin(), icos()))', 'from iterators_classic import product, isin, icos, take')
    result = t.repeat(2, 20)
    print('20*take(100, product-classic(isin(), icos())) : ', result)

    print()

    ##    t = Timer('take(100, inv(iexp()))', 'from iterators import inv, iexp, take')
    ##    result = t.repeat(2, 20)
    ##    print '20*take(100, inv-new(iexp())) : ', result

    ##    t = Timer('take(100, inv(iexp()))', 'from iterators_new import inv, iexp, take')
    ##    result = t.repeat(2, 20)
    ##    print '20*take(100, inv-newnew(iexp())) : ', result

    t = Timer('take(100, inv(iexp()))', 'from iterators_classic import inv, iexp, take')
    result = t.repeat(2, 20)
    print('20*take(100, inv-classic(iexp())) : ', result)
