# s.siedersleben
# fasttrack to professional programming
# lesson 5: sorting
# 05.12.2020

from collections_.heap import Heap
from iterators.iterators2 import take
from iterators.trees import breadthfirst, preorder1


def heap2tree(h, index=0):
    """
    :param h: a heap as defined in heap.p
    :param index: current position within our heap, initially set to zero i.e. top of tree
    :return: a heap transformed into a tree structure represented by tuples (left_subtree, value, right_subtree)
    """
    n = len(h)
    if n == 0:
        return None

    child1 = 2 * index + 1
    child2 = 2 * index + 2
    if child1 > n - 1:
        return (None, h[index], None)
    elif child2 > n - 1:
        return (heap2tree(h, child1), h[index], None)
    else:
        return (heap2tree(h, child1), h[index], heap2tree(h, child2))


if __name__ == '__main__':

    # m = Myheap()
    # xs = [21, 1, 8, 10, 50, 2]
    # h = Myheap()
    # for x in xs:
    #     h.myheappush(x)

    h = Heap()
    xs = [21, 1, 8, 10, 50, 2]
    # xs = [0, 1, 3]
    for x in xs:
        h.heappush(x)

    print(h)

    tree = heap2tree(h, 0)
    print(tree)

    b = breadthfirst(tree)
    print(take(b, 20))

    p = preorder1(tree)
    print(take(p, 20))

    # tree = Tree(3)
    # print(tree.tree[2])
