# checkInvariants Z over p
# js 12/08/2004
# reworked 20/07/2023
# reworked 16/01/2024


from unittest import TestCase

from gen_types import *
from mp import Mp


class TestGenTypes(TestCase):
    def test_gen(self):
        n = 3
        cnt = 0
        print('Fields')
        for t in gen_fields(n):
            print(cnt, t)
            cnt += 1

        print()
        print('Euclidian Rings')
        for t in gen_euclidian_rings(n):
            print(cnt, t)
            cnt += 1

    def test_gen_m(self):
        n = 4
        cnt = 0
        print('Fields')
        for m in gen_fields_m(n):
            print(cnt, m(1))
            cnt += 1

        print()
        print('Euclidian Rings')
        for m in gen_euclidian_rings_m(n):
            print(cnt, m(1))
            cnt += 1

    def testX(self):
        a = Mp(3, [7])
        b = Polynomial(a)
        c = Mp(b, [Polynomial(1, 0, 1)])
        print(c)

        a = Fp(3, 7)
        b = Polynomial(a)
        c = Fp(b, Polynomial(1, 0, 1))
        print(c)
