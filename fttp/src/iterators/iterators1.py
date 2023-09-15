# from classes_.polynomial import *
# from iterators2 import *
from iterators.trees import pre2tree


# def naturals(start: int = 0) -> Iterator:
#     """
#     :param start: an integer
#     :return: the naturals
#     """
#     while start < 3:
#         yield start
#         start += 1
#
#
# class Faculty(object):
#     def __iter__(self):
#         return faculty()


def preorder2tree(xs: list) -> tuple:
    """
    :param xs: a integer list
    :return: a binary tree, resulting from the preordered list xs
    cheating solution
    """
    if len(xs) == 0:
        return None
    value = xs.pop(0)
    return preorder2tree(xs), value, None


def preorder2tree1(xs: list) -> tuple:
    """
    :param xs: a integer list
    :return: a binary tree, resulting from the preordered list xs
    """
    # todo
    if len(xs) == 0:
        return None
    value = xs.pop(0)
    return preorder2tree1(xs), value, None


if __name__ == '__main__':
    # c = take(cos_taylor(), 20)
    # p = Polynomial(c)
    # for x in range(-3, 3):
    #     print(p(x) - cos(x))

    xs = [1, 2, 21, 2]
    tree = pre2tree(xs)
    print(tree)
