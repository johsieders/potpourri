# Generating types
# I generate all legal combinations of builtin types (int, float complex)
# composed types (polynomials, rationals and Fp)


from fp import Fp
from polynomials import Polynomial
from rationals import Rational


def gen_fields(depth):
    if depth == 0:
        return

    yield 'float'
    yield 'complex'

    for t in gen_euclidian_rings(depth - 1):
        yield 'Rational[' + t + ']'

    for t in gen_euclidian_rings(depth - 1):
        yield 'Fp[' + t + ']'


def gen_euclidian_rings(depth):
    if depth == 0:
        return

    yield 'int'
    for t in gen_fields(depth - 1):
        yield 'Polynomial[' + t + ']'


def gen_fields_m(depth):
    if depth == 0:
        return

    yield float
    yield complex

    for t in gen_euclidian_rings_m(depth - 1):
        yield lambda x: Rational(t(x))

    for t in gen_euclidian_rings_m(depth - 1):
        yield lambda x: Fp(t(x), 11)


def gen_euclidian_rings_m(depth):
    yield int
    for t in gen_fields_m(depth - 1):
        yield lambda x: Polynomial(t(x))


def gen_fields_t(depth) -> list:
    if depth == 0:
        return

    yield [float(x) for x in (0, 1, 2, 3)]
    yield [complex(x) for x in (0, 1, 2, 3)]

    for t in gen_euclidian_rings_t(depth - 1):
        yield [Rational(x) for x in t]

    for t in gen_euclidian_rings_t(depth - 1):
        yield [Fp(x, x.get_sample_prime()) for x in t]


def gen_euclidian_rings_t(depth) -> list:
    class _int(int):
        def get_sample_prime(self):
            return 11

    class _Polynomial(Polynomial):
        def get_sample_prime(self):
            return _Polynomial(1, 0, 0, 1)

    if depth == 0:
        return

    yield [_int(x) for x in (0, 1)]

    for t in gen_fields_t(depth - 1):
        tmp = []
        for a in t:
            for b in t:
                tmp.append(_Polynomial(a, b))
        yield tmp
