# j.siedersleben
# fasttrack to professional programming
# lesson 6: iterators applied to trees
# 2.1.2021

from collections import deque

from warmingup.types_ import Iterator
from warmingup.warmingup2 import log2


# We consider binary trees. Each node has a value,
# a left subtree, and a right subtree.
# Nodes are represented by triples
# [left_subtree, value, right_subtree],
# left and right subtrees being None or a triple of the same type.
# A tree is represented by its root.
# There is no difference between a node and a tree.
# The empty subtree is None,
# a subtree with one only node is [None, value, None]

# Traversing a tree depth first:
# There are six permutations of (left, value, right)
# four of which have a name:

# preorder: value, left, right
# inorder: left, value, right
# revinorder: right, value, left
# postorder: right, left, value

# two varieties of depth first are not used:
# no name: value, right, left
# no name: left, right, value

# Traversing a tree breadth first is by layer:
# the root comes first (layer 0),
# then its children (layer 1),
# then their children (layer 2)
# and so on.


def bfo2tree(bfo: list, i=0) -> tuple:
    """"
    :param bfo: a tree represented as a list in breadth first order (bfo)
    :param i: index of a node >= 0
    :return: this tree represented as a binary tree, each node being
    a triple (left_subtree, value, right_subtree)
    None represents the empty tree, so bfo2tree([]) is None
    """
    if bfo:
        left = bfo2tree(bfo, 2 * i + 1) if 2 * i + 1 < len(bfo) else None
        right = bfo2tree(bfo, 2 * i + 2) if 2 * i + 2 < len(bfo) else None
        return left, bfo[i], right


def pre2tree(pre: list) -> tuple:
    """"
    :param pre: a tree represented as a list in preorder
    :param i: index of a node >= 0
    :return: this tree represented as a binary tree, each node being
    a triple (left_subtree, value, right_subtree)
    None represents the empty tree, [] gives None
    """
    left_subtree = None

    if pre:
        depth = log2(len(pre)) + 1
        head, tail = pre[:depth], pre[depth:]

        left_subtree = (None, head.pop(), None)
        for d in range(1, depth):
            parent = head.pop()
            right_subtree = pre2tree(tail[:d])
            left_subtree = (left_subtree, parent, right_subtree)

    return left_subtree


###############################################
# recursive implementation of
# preorder, inorder, revinorder and postorder
###############################################

def preorder(tree: tuple) -> Iterator:
    if tree is not None:
        yield tree[1]
        yield from preorder(tree[0])
        yield from preorder(tree[2])


def preorder2(tree: tuple) -> list:
    result = []

    def aux(t: tuple):
        if t is not None:
            result.append(t[1])
            aux(t[0])
            aux(t[2])

    aux(tree)
    return result


def inorder(tree: tuple) -> Iterator:
    if tree is not None:
        yield from inorder(tree[0])
        yield tree[1]
        yield from inorder(tree[2])


def revinorder(tree: tuple) -> Iterator:
    if tree is not None:
        yield from revinorder(tree[2])
        yield tree[1]
        yield from revinorder(tree[0])


def postorder(tree: tuple) -> Iterator:
    if tree is not None:
        yield from postorder(tree[2])
        yield from postorder(tree[0])
        yield tree[1]


def breadthfirst(*trees: tuple) -> Iterator:
    """
    :param trees: binary trees given as [left_subtree, value, right_subtree]
    :return: iterator of values in breadth-first-order
    """
    if trees:
        kids = []
        for tree in trees:
            if tree is not None:  # yield this layer and build the next one
                yield tree[1]
                kids.append(tree[0])
                kids.append(tree[2])
        yield from breadthfirst(*kids)  # yield next layer


###############################################
# stack-based implementation of
# preorder and inorder
###############################################

def preorder1(tree: tuple) -> Iterator:
    if tree is not None:
        stack = [tree]
        while len(stack) > 0:
            tree = stack.pop()
            if tree is not None:
                yield tree[1]
                stack.append(tree[2])
                stack.append(tree[0])


def inorder1(tree: tuple) -> Iterator:
    if tree is not None:
        stack = [tree]
        while len(stack) > 0:
            tree = stack.pop()
            if tree is not None:  # descend left subtree
                stack.append(tree)
                stack.append(tree[0])
            elif len(stack) > 0:  # bottom reached, one step up
                tree = stack.pop()
                yield tree[1]
                stack.append(tree[2])  # descend right right subtree


###############################################
# deque-based implementation of breadth-first
###############################################

def breadthfirst1(tree: tuple) -> Iterator:
    """
    :param tree: a binary tree given as [left_subtree, value, right_subtree]
    :return: iterator of values in breadth-first-order
    compare this to preorder1
    """
    if tree is not None:
        queue = deque([tree])
        while len(queue) > 0:
            tree = queue.popleft()
            if tree is not None:
                yield tree[1]
                queue.append(tree[0])
                queue.append(tree[2])


def breadthfirst2(tree: tuple) -> list:
    """
    :param tree: a binary tree given as [left_subtree, value, right_subtree]
    :return: list of values in breadth-first-order
    """
    result = []
    if tree is not None:
        queue = deque([tree])
        while len(queue) > 0:
            tree = queue.popleft()
            if tree is not None:
                result.append(tree[1])  # this replaces yield tree[1]
                queue.append(tree[0])
                queue.append(tree[2])
    return result
