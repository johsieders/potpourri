# s.siedersleben
# fasttrack to professional programming
# lesson 5: sorting
# 27.12.2020

from collections_.heap1 import Myheap


def bubble_sort(xs):
    """
    this function sorts in place using two methods
    :param xs: unsorted list
    :return: xs sorted; sorts on place
    """
    n = len(xs)
    if n <= 1:
        return

    for i in range(n - 1):
        for j in range(n - i - 1):
            if xs[j] > xs[j + 1]:
                xs[j], xs[j + 1] = xs[j + 1], xs[j]


def bubble_sort1(xs):
    """
    this function sorts returns a new sorted list, method recursive
    :param xs: unsorted list
    :return: a new list xs sorted, NOT on place
    """
    n = len(xs)
    if n <= 1:
        return xs
    else:
        for i in range(n - 1):
            if xs[i] > xs[i + 1]:
                xs[i], xs[i + 1] = xs[i + 1], xs[i]
    return bubble_sort1(xs[:-1]) + [xs[-1]]


def heap_sort(xs):
    """
    heapsort
    :param xs: a list
    :return: a new list containing xs sorted using the class Myheap from collections_
    """
    h = Myheap()
    for x in xs:
        h.myheappush(x)
    return [h.myheappop() for _ in range(len(h))]


if __name__ == '__main__':
    # ll = [4, 3, 2, 10, 11, 15]
    ll = [5, 4, 3, 2, 1]
    print(ll)
    print(heap_sort(ll))
