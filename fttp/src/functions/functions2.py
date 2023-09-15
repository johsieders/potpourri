# j.siedersleben
# fasttrack to professional programming
# lesson 3: functions
# 28.11.2020

from functools import reduce
from operator import mul

from warmingup.warmingup2 import normstring


def sortByLetter(strings, n):
    """
    sort list of strings by n-th letter
    :param strings: a list of strings
    :param n: n an integer, 0 <= n < min{len(s), s in strings}
    :return: None
    """
    strings.sort(key=lambda s: s[n])


###############
### anagram ###
###############

def anagram_key1(s):
    t = list(normstring(s))
    t.sort()
    return ''.join(t)


def anagram_key2(s):
    t = list(normstring(s))
    t.sort()
    return ''.join(t) + s


def anagram_sort1(xs):
    """
    :param xs: list of strings
    :return: None
    sorts xs in anagram order
    anagrams come in any order
    """
    xs.sort(key=anagram_key1)


def anagram_sort2(xs):
    """
    :param xs: list of strings
    :return: None
    sorts xs in anagramm order;
    anagrams are sorted
   """
    xs.sort(key=anagram_key2)


##############################
### playing with functions ###
##############################

def addFun1(f, g):
    """
    :param f: a function expecting one argument and returning something that can be added
    :param g: another function of that sort
    :return: a function expecting one argument and returning f + g
    """

    def result(x):
        return f(x) + g(x)

    return result


def addFun(f, g):
    """
    :param f: a function expecting one argument and returning something that can be added
    :param g: another function of that sort
    :return: a function expecting one argument and returning f + g
    identical to addFun1
    """
    return lambda x: f(x) + g(x)


def compose(f, g):
    """
    :param f: a function expecting one argument and returning anything
    :param g: a function expecting one argument and returning one value
    :return: a function expecting one argument and returning f o g
    """
    return lambda x: f(g(x))


def curry(f, x):
    """
    :param f: a function expecting two arguments
    :param x: a value the first argument of f is to be bound to
    :return: f with the first argument bound to x
    """
    return lambda y: f(x, y)


def flip(f):
    """
    :param f: a function expecting two arguments
    :return: f with flipped arguments
    """
    return lambda x, y: f(y, x)


##############################
###  getting on with map   ###
##############################

def times2(xs):
    """
    :param xs: a list of elements which can be multiplied by 2
    :return: a list containing the doubles
    This is called list comprehension
    """
    return [2 * x for x in xs]


def times21(xs):
    """
    :param xs: a list of elements which can be multiplied by 2
    :return: a list containing the doubles
    identical to times2; that's the classical way
    """
    return map(lambda x: 2 * x, xs)


##############################
### getting on with reduce ###
##############################

def multiplyAll(xs):
    return reduce(mul, xs, 1)


def composeAll(fs):
    """
    :param fs: a list of functions expecting one argument and returning one value
    :return: the composition f0 o f1 o ... fn-1, returns identity if len(fs) = 0
    """
    result = lambda x: x

    for f in fs:
        result = compose(result, f)

    return result


def composeAll1(fs):
    """
    :param fs: a list of functions expecting one argument and returning one value
    :return: the composition f0 o f1 o ... fn-1, returns identity if len(fs) = 0
    This is cool.
    """
    return reduce(compose, fs, lambda x: x)


def binary2nary(f):
    """
    :param f: a function expecting two arguments
    :return: a function reducing n arguments to f
    """

    def nary(*x):
        if len(x) == 0:
            raise ValueError
        elif len(x) == 1:
            return x[0]
        else:
            start = f(x[0], x[1])
            return start if len(x) == 2 else reduce(f, x[2:], start)

    return nary


def composeAll2():
    """
    :return: a function F which accepts a list of functions given as *f
    and returns the composition f0 o f1 o ... fn-1; identity if len(fs) = 0
    This is even cooler.
    """
    return binary2nary(compose)


##############################
### getting on with Horner ###
##############################

def horner(a, x):
    """
    :param a: coefficients of a polynom p: a0 + a1 x + a2 x2 + ...
    :param x: argument for p
    :return: p(x)
    """
    aux = list(a)
    aux.reverse()
    return reduce(lambda s, t: x * s + t, aux)


def polynom(a):
    """
    :param a: coefficients of a polynom p: a0 + a1 x + a2 x2 + ...
    :return: function p which evaluates the polynom
    """
    return curry(horner, a)


if __name__ == '__main__':
    def f(x):
        return 2 * x


    def g(x):
        return 3 * x


    def add(a, b):
        return a + b


    d = curry(add, 27)
    d(15)

    h = addFun1(f, g)
    c = compose(f, g)

    a = [1, 3, 3]
    horner(a, 1)
    p = polynom(a)
    p(1)

    print(c(5))
