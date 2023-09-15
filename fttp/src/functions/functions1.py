anagrams = ['Old Testament',
            'most talented',
            'carthose',
            'orchestra',
            'contaminated',
            'no admittance',
            'emigrants',
            'streaming',
            'Amery',
            'Mayer',
            'Cinerama',
            'American',
            'World Cup team',
            'talcum powder',
            'William Ewart Gladstone',
            'Wild agitator, means well']

xs = ['otto', 'anna', 'ttoo', 'oott', 'nnaa']


def sortByLetter(xs, n):
    """
    :param xs: list of strings
    :param n:
    :return:
    """

    def myKey(s):
        return s[n]

    xs.sort(key=myKey)

    # xs.sort(key=lambda s : s[n])


def anagram0(xs):
    """
    :param xs: list of strings
    :return: there is no return, this function works in place and sorts xs using the sortAnagramKey
    """

    def sortAnagramKey(s):
        """
        :param s: string
        :return: a sorted string
        """
        return "".join(sorted(list(s)))

    xs.sort(key=sortAnagramKey)


def anagram1(xs):
    """
    :param xs: list of strings
    :return: there is no return, this function works in place and sorts xs using the sortAnagramKey
    """

    def sortAnagramKey(s):
        """
        :param s: string
        :return: a sorted string
        """
        return s[0] + "".join(sorted(list(s)))

    xs.sort(key=sortAnagramKey)


def power0(x, n):
    """
    :param x: any number
    :param n: positive integer
    :return: the n-th power of x
    comment: recursive solution
    """

    if n == 0:
        return 1
    else:
        return x * power0(x, n - 1)


def power1(x, n):
    from functools import reduce
    import numpy as np
    """
    :param x:
    :param n:
    :return:
    """
    xs = np.ones(n) * x
    result = reduce(lambda a, b: a * b, xs)
    return result


def merge0(xs, ys):
    """
    :param xs: list with integers, sorted, smallest int first
    :param ys: list with integers, sorted smallest int first
    :return: a new sorted list including all elements of xs and ys
    """
    from functools import reduce
    zs = xs + ys
    dummy = list(zs)
    result = []
    for _ in dummy:
        max_val = reduce(lambda a, b: a if a < b else b, zs)
        result.append(max_val)
        zs.remove(max_val)
    return result


def merge1(xs, ys):
    """
    :param xs: list with integers of length n, sorted, smallest int first
    :param ys: list with integers of length n, sorted smallest int first
    :return: a new sorted list including all elements of xs and ys
    """
    result = []

    for x, y in zip(xs, ys):
        if x > y:
            result.append(y)
            result.append(x)
        else:
            result.append(x)
            result.append(y)
    return result


def compose(f, g):
    """
    :param f: a function accepting integers and floats returning floats
    :param g: a function accepting integers and floats returning floats
    :return: a function accepting integers and floats returning floats f(g(x))
    """

    def result(x):
        return f(g(x))

    return result


def curry(f, x):
    return lambda y: f(x, y)


if __name__ == '__main__':
    xs = ['otto', 'ttoo', 'oott', 'nnaa', 'anna']
    ys = list(xs)
    anagram1(xs)
    print(xs)
    ys.sort(key=lambda s: s[0] + "".join(sorted(list(s))))
    print(ys)
    print(power1(2, 2))

    xs = [1, 2, 3]
    ys = [2, 4, 5]

    zs = merge0(xs, ys)
    print(zs)
    zs = merge1(xs, ys)
    print(zs)
