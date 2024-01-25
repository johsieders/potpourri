# Abstract ring, abstract field
# js 16.01.2024

from rings import Ring


class Field(Ring):
    """
    This is an abstract class that extends Comparable and Ring.
    It adds division and power with negative exponent
    """

    def div(self, b):
        raise NotImplementedError

    def __abs__(self):
        raise NotImplementedError

    def __pow__(self, n: int):
        return 1 / self ** -n if n < 0 else super().__pow__(n)

    def __truediv__(self, b):
        b = self.transform(b)
        return self.div(b)

    def __rtruediv__(self, b):
        b = self.transform(b)
        return b.div(self)
