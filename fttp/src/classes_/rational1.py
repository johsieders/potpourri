# s.siedersleben
# fasttrack to professional programming
# lesson 4: classes_
# 16.12.2020

from warmingup.warmingup2 import gcd


class Rational(object):
    def __init__(self, a, b):
        if b == 0:
            raise ValueError

        self.nominator, self.denominator = self.cancel(a, b)

    def __str__(self):
        return str(self.nominator) + "/" + str(self.denominator)

    def __eq__(self, other):
        # return other.nominator == self.nominator and self.denominator == other.denominator
        return self.nominator * other.denominator == other.nominator * self.denominator

    def __invert__(self):
        result = Rational(self.denominator, self.nominator)
        return result

    def __lt__(self, other):
        return self.nominator * other.denominator - other.nominator * self.denominator < 0

    def __le__(self, other):
        return self.nominator * other.denominator - other.nominator * self.denominator <= 0

    def __gt__(self, other):
        return self.nominator * other.denominator - other.nominator * self.denominator > 0

    def __ge__(self, other):
        return self.nominator * other.denominator - other.nominator * self.denominator >= 0

    def __add__(self, other):
        result = Rational(self.nominator * other.denominator + self.denominator * other.nominator,
                          self.denominator * other.denominator)
        return result

    def __sub__(self, other):
        result = Rational(self.nominator * other.denominator - self.denominator * other.nominator,
                          self.denominator * other.denominator)
        return result

    def __truediv__(self, other):
        return Rational(self.nominator * other.denominator, self.denominator * other.nominator)

    def __mul__(self, other):
        return Rational(self.nominator * other.nominator, self.denominator * other.denominator)

    def exp_frac(self, c):
        return self.denominator * c, self.nominator * c

    @classmethod
    def cancel(cls, a, b):
        c = gcd(a, b)
        return a // c, b // c


if __name__ == '__main__':
    d = Rational(1, 2)
    f = Rational(1, 4)
    e = Rational(0, 1)

    print(d, f)
    print(d == f)
    print(d < f)
    print(d > f)
    print(d >= f)

    print(d + e)
    print(d + e == d)
    print(d + f)
