class Type(object):
    """
    this is the Type class
    """

    def zero(self):
        raise NotImplementedError

    def one(self):
        raise NotImplementedError


class Float(Type):

    def zero(self):
        return 0.

    def one(self):
        return 1.


class Vector(Type):

    def __init__(self, type, length):
        self.type = type
        self.length = length


if __name__ == '__main__':
    print()
