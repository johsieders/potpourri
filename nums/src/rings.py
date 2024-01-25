# Abstract ring, abstract field
# js 16.01.2024


class Ring(object):
    """
    This abstract class implements a Ring
    To be implemented by subclass:
    transform(), eq(), add(), sub(), and mul()
    There is no division and no divmod
    """

    def transform(self, x):
        raise NotImplementedError

    def add(self, b):
        raise NotImplementedError

    def sub(self, b):
        raise NotImplementedError

    def mul(self, b):
        raise NotImplementedError

    def eq(self, b):
        raise NotImplementedError

    def __eq__(self, b):
        b = self.transform(b)
        return self.eq(b)

    def __ne__(self, b):
        b = self.transform(b)
        return not self.eq(b)

    def __bool__(self):
        zero = self.transform(0)
        return not self.eq(zero)

    def __add__(self, b):
        b = self.transform(b)
        return self.add(b)

    def __sub__(self, b):
        b = self.transform(b)
        return self.sub(b)

    def __mul__(self, b):
        b = self.transform(b)
        return self.mul(b)

    def __neg__(self):
        zero = self.transform(0)
        return zero.sub(self)

    def __pos__(self):
        return self

    def __pow__(self, n: int):
        if n < 0:
            raise ValueError("exponent must not be negative")
        elif n == 0:
            return self.transform(1)
        elif n == 1:
            return self
        else:
            n0 = n // 2
            n1 = n - n0
            return (self ** n0) * (self ** n1)

    def __radd__(self, b):
        b = self.transform(b)
        return b.add(self)

    def __rsub__(self, b):
        b = self.transform(b)
        return b.sub(self)

    def __rmul__(self, b):
        b = self.transform(b)
        return b.mul(self)
