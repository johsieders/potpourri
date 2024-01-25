# Comparable
# js 15.01.2024

class Comparable(object):
    """
    This is an abstract class which defines <=, >, and >= using <
    """

    def transform(self, x):
        raise NotImplementedError

    def lt(self, x):
        raise NotImplementedError

    def __lt__(self, b):
        b = self.transform(b)
        return self.lt(b)

    def __le__(self, b):
        return self < b or self == b

    def __ge__(self, b):
        return not (self < b)

    def __gt__(self, b):
        return not (self <= b)
