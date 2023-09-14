# Johannes Siedersleben
# 21.08.2023
# trying lambda-calculus

# term.abstract('x', 'y') -> Lx.Ly.term
# term.apply_to('a', 'b') -> Lx.Ly.term a b
# term.beta_reduction() -> performs at most one beta-reduction
# BetaNormalisingVisitor().skip_intermediate(term) -> performs all beta-reductions
# Lx.Ly.term a b -> term(a b) that is: x, y replaced with a, b

# cons = Lx.Ly.Lf.(f x y)   OR: def cons x y = Lf.(f x y) with f = head or tail
# head = Lx.Ly.x            OR: def head x y = x
# tail = Lx.Ly.y            OR: def tail x y = y
# (cons a b) => Lf.(f a b) = (a, b)
# (cons a b head) => (head a b) = a
# (cons a b tail) => (tail a b) = b
# (cons a (cons b c)) => (a, (b, c))
# (cons a (cons b (cons c d))) = (a, (b, (c, d)))

# def cond = Lx.Ly.Lc.(c x y)     ## same as pair, c = condition
# def true = Lx.Ly.x              ## same as head
# def false = Lx.Ly.y             ## same as tail
# (cond a b) => Lf.(f a b)
# (cond a b true) => true a b => a
# (cond a b false) => false a b => b
# (cond a b c) => c ? a : b

# def not = La.(cond false true)
# def and = La.Lb.(a b false)
# def or = La.Lb.(a b true)

# def zero = Lx.x       # identity
# def iszero = true    # (zero iszero) == (identity true) => true; (n iszero) = (false, pred n) true => false
# def succ = Ln.Ls.((s false) n) = (cons false n) = (false, n)
# def one = (succ zero) = (false, zero)
# def two = (succ one) = (false, one) = (false, (false, zero))
# def three = (succ two) = (false, two) = (false, (false, one)) = (false, (false, (false, zero)))
# def pred = Ln.(n false)    doesn't work for zero, hence
# def pred = (cond zero (n tail) (iszero n))  =  (iszero n) ? zero : (n tail)
#          = ((iszero n) zero (n tail))

# eta-reduction: Lx.(f x) -> f
# term.eta_reduction() -> reduced term

# Recursion with the lambda calculus
# A. Recursive definition of multiplication for use with Y
# def m f x y = y == 0 ? 0 : (x + (f x y-1))
# Here, f is an artificial parameter to be used as the function
# to be called recursively
#
# B. Y-Combinator
# Y = Lf.Lg.((f (g g)) Lg.(f (g g)))
#
# C. Fixpoint property of Y
# (Y m) => ((Lg.(m (g g)) Lg.(m (g g)))
#       => (m (Lg.(m (g g)) Lg.(m (g g))))
#       == (m (Y m))
#
# D. Application
# (Y m x y) => (m (Y m) x y)    # apply m to f = (Y m), x and y
#           => y == 0 ? 0 : (x + (Y m x y-1))
#
# This is how recursion works with the lambda calculus
#
# E. Omega
# omega = Lx.(x x) = (Lx.(x x)) (Lx.(x x)) = omega omega
# omega = (Lx.(x x)) (Lx.(x x)) = (Lx.(x x)) omega = omega omega


import unittest

from lambda_calculus import Variable
from lambda_calculus.terms.arithmetic import ISZERO, SUCCESSOR, PREDECESSOR, number
from lambda_calculus.terms.logic import IF_THEN_ELSE
from lambda_calculus.terms.pairs import PAIR, FIRST, SECOND, NIL
from lambda_calculus.visitors.normalisation import BetaNormalisingVisitor


class MyTestCase(unittest.TestCase):

    def test_const(self):
        c17 = Variable('17').abstract('x')  # Lx.17
        c17 = c17.apply_to(Variable('a'))  # Lx.17 a
        c17 = c17.beta_reduction()  # 17
        self.assertEqual(str(c17), '17')

        const = Variable('c').abstract('c', 'x')  # Lc.Lx.c
        c18 = const.apply_to(Variable('18'))  # Lx.18
        c18 = c18.beta_reduction()  # 18
        c18 = c18.apply_to(Variable('a'))  # Lx.18 a
        c18 = c18.beta_reduction()  # 18
        self.assertEqual(str(c18), '18')

        c19 = const.apply_to(Variable('19'), Variable('a'))  # (Lc.Lx.c) 19 a
        c19 = BetaNormalisingVisitor().skip_intermediate(c19)  # 19
        self.assertEqual(str(c19), '19')

    def test_pair(self):
        p = PAIR.apply_to(Variable('a'), Variable('b'))  # Lx.Ly.Lf.((f x) y) a b

        # my first, second
        first = Variable('x').abstract('x', 'y')  # Lx.Ly.x
        second = Variable('y').abstract('x', 'y')  # Lx.Ly.y

        p = BetaNormalisingVisitor().skip_intermediate(p)  # Lf.((f a) b)

        frst = p.apply_to(first)  # Lf.((f a) b) Lx.Ly.x
        scnd = p.apply_to(second)  # Lf.((f a) b) Lx.Ly.y

        frst = BetaNormalisingVisitor().skip_intermediate(frst)
        scnd = BetaNormalisingVisitor().skip_intermediate(scnd)

        self.assertEqual(str(frst), 'a')
        self.assertEqual(str(scnd), 'b')

        # his FIRST, SECOND
        frst = FIRST.apply_to(p)  # Lf.((f a) b) Lx.Ly.x
        scnd = SECOND.apply_to(p)  # Lf.((f a) b) Lx.Ly.y

        frst = BetaNormalisingVisitor().skip_intermediate(frst)
        scnd = BetaNormalisingVisitor().skip_intermediate(scnd)

        self.assertEqual(str(frst), 'a')
        self.assertEqual(str(scnd), 'b')

    def test_eta(self):
        v = Variable('f').apply_to(Variable('x')).abstract('x')  # Lx.(f x)
        w = v.eta_reduction()
        self.assertEqual(str(w), 'f')

    def test_alpha(self):
        apply = Variable('f').apply_to(Variable('x')).abstract('f', 'x')  # Lf.Lx.(f x)
        result = apply.apply_to(Variable('g'), Variable('y'))  # Lf.Lx.(f x) g y
        result = BetaNormalisingVisitor().skip_intermediate(result)  # (g y)
        self.assertEqual(str(result), '(g y)')

        apply1 = apply.alpha_conversion('y')
        apply2 = apply1.alpha_conversion('z')

        result = apply.apply_to(Variable('x'), Variable('y'))  # Lf.Lx.(f x) x y
        print(result)

    def test_list(self):
        cons = PAIR
        head = Variable('h').abstract('h', 't')  # (λh.λt.h)
        tail = Variable('t').abstract('h', 't')  # (λh.λt.t)

        x1 = cons.apply_to(Variable('1'), NIL)
        h = x1.apply_to(head)
        t = x1.apply_to(tail)
        h = BetaNormalisingVisitor().skip_intermediate(h)
        t = BetaNormalisingVisitor().skip_intermediate(t)
        self.assertEqual(str(h), '1')
        self.assertEqual(t, NIL)

        x2 = cons.apply_to(Variable('2'), x1)
        h = x2.apply_to(head)
        t = x2.apply_to(tail).apply_to(tail)
        h = BetaNormalisingVisitor().skip_intermediate(h)
        t = BetaNormalisingVisitor().skip_intermediate(t)
        self.assertEqual(str(h), '2')
        self.assertEqual(t, NIL)

    def test_nil(self):
        # NIL returns the second argument and ignores arguments one and three
        # NIL = (λx.λx.λy.x)

        a = NIL.apply_to(Variable('a'))
        print(a)
        a = BetaNormalisingVisitor().skip_intermediate(a)
        print(a)

        b = NIL.apply_to(Variable('a'), Variable('b'))
        print(b)
        b = BetaNormalisingVisitor().skip_intermediate(b)
        print(b)

        c = NIL.apply_to(Variable('a'), Variable('b'), Variable('c'))
        print(c)
        c = BetaNormalisingVisitor().skip_intermediate(c)
        print(c)

        n = NIL.apply_to(Variable('a'))
        h = NIL.apply_to(FIRST)
        t = NIL.apply_to(SECOND)

        print(n)
        print(h)
        print(t)
        print()

        n = BetaNormalisingVisitor().skip_intermediate(n)
        h = BetaNormalisingVisitor().skip_intermediate(h)
        t = BetaNormalisingVisitor().skip_intermediate(t)

        print(n)
        print(h)
        print(t)

    def test_numbers(self):
        zero = number(0)
        a = ISZERO.apply_to(zero)
        a = BetaNormalisingVisitor().skip_intermediate(a)

        one = SUCCESSOR.apply_to(zero)
        one = BetaNormalisingVisitor().skip_intermediate(one)
        two = number(2)
        three = number(3)

        zero1 = PREDECESSOR.apply_to(one)
        zero1 = BetaNormalisingVisitor().skip_intermediate(zero1)

        a1 = ISZERO.apply_to(zero1)
        a1 = BetaNormalisingVisitor().skip_intermediate(a1)

    def test_cond(self):
        id = Variable('x').abstract('x')  # Lx.x
        print(id)
        idy = id.apply_to(Variable('y'))
        idy = BetaNormalisingVisitor().skip_intermediate(idy)
        b0 = ISZERO.apply_to(number(0))
        b0 = BetaNormalisingVisitor().skip_intermediate(b0)  # True: Lx.Ly.x
        b1 = ISZERO.apply_to(number(1))
        b1 = BetaNormalisingVisitor().skip_intermediate(b1)  # False: Lx.Ly.y
        print(b0)
        print(b1)

        iz = IF_THEN_ELSE.apply_to(ISZERO.apply_to(Variable('x'), Variable('a'), Variable('b')))
        print(iz.free_variables())
        print(iz.bound_variables())

        iz.abstract('x')
        a0 = iz.apply_to(number(0))
        # a1 = iz.apply_to(number(1))
        a0 = BetaNormalisingVisitor().skip_intermediate(a0)
        # a1 = BetaNormalisingVisitor().skip_intermediate(a1)
        print(a0)
        # print(a1)

    def test_rec(self):
        pass
