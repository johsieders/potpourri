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
    if depth == 0:
        return

    yield int
    for t in gen_fields_m(depth - 1):
        yield lambda x: Polynomial(t(x))
