# Ring
# js 15.01.2024

from comparables import Comparable
from rings import Ring


class EuclidianRing(Ring, Comparable):
    def get_sample_prime(self):
        """
        :return: any prime element
        (a prime number or an irreducible polynomial)
        This is useful for generating test cases.
        """
        raise NotImplementedError()

    def my_divmod(self, b):
        """
        :param q: divisor
        :return: quotient and remainder of p and q
        """
        raise NotImplementedError()

    def __divmod__(self, b):
        b = self.transform(b)
        return self.my_divmod(b)

    def __rdivmod__(self, b):
        b = self.transform(b)
        return b.my_divmod(self)

    def __floordiv__(self, b):
        b = self.transform(b)
        return self.my_divmod(b)[0]

    def __mod__(self, b):
        b = self.transform(b)
        return self.my_divmod(b)[1]

    def __rfloordiv__(self, b):
        b = self.transform(b)
        return b.my_divmod(self)[0]

    def __rmod__(self, b):
        b = self.transform(b)
        return b.my_divmod(self)[1]
