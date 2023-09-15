# j.siedersleben
# fasttrack to professional programming
# lesson 7: searching
# 20.11.2020


def insert(tree: list, x: any) -> list:
    """
    :param tree: a 2-3-tree
    :param x: element to be inserted
    :return: top-level node, if
    """

    # find subtree where x belongs
    if len(tree) == 0:
        subtree = []
    elif x <= tree[1]:
        subtree = tree[0]
    elif len(tree) == 3 or x <= tree[3]:
        subtree = tree[2]
    else:
        subtree = tree[4]

    if subtree:  # insert x in subtree
        new_node = insert(subtree, x)
    else:  # create new node
        new_node = [[], x, []]

    if not new_node:  # x was dispatched in subtree
        return []

    if len(tree) == 0:  # tree was empty
        return new_node

    elif len(tree) == 3:  # new node to be dispatched here
        if new_node[1] <= tree[1]:
            tree[:1] = new_node
        else:
            tree[2:] = new_node
        return []

    else:  # len(tree) == 5
        # new node will be dispatched by parent
        # node to be returned contains a middle node and two children
        if new_node[1] <= tree[1]:  # tree[1] is in the middle
            return [new_node, tree[1], tree[2:]]
        elif new_node[1] <= tree[3]:  # new_node[1] in the middle
            return [tree[:2] + [new_node[0]], new_node[1], [new_node[2]] + tree[3:]]
        else:  # tree[3] in the middle
            return [tree[:3], tree[3], new_node]


class RBtree(object):
    def __init__(self):
        self.tree = []

    def insert(self, x):
        t = insert(self.tree, x)
        if t:
            self.tree = t
