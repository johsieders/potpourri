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
        return other.nominator == self.nominator and self.denominator == other.denominator

    def __lt__(self, other):
        if self.denominator == other.denominator:
            return self.nominator < other.nominator
        else:
            c = gcd(self.denominator, other.denominator)
            self.nominator, self.denominator = self.exp_frac(c)
            other.nominator, other.denominator = other.exp_frac(c)
            return self.nominator < other.nominator if self.denominator == other.denominator else print("Error")

    def __le__(self, other):
        if self.denominator == other.denominator:
            return self.nominator <= other.nominator
        else:
            c = gcd(self.denominator, other.denominator)
            self.nominator, self.denominator = self.exp_frac(c)
            other.nominator, other.denominator = other.exp_frac(c)
            return self.nominator <= other.nominator if self.denominator == other.denominator else print("Error")

    def __gt__(self, other):
        if self.denominator == other.denominator:
            return self.nominator > other.nominator
        else:
            c = gcd(self.denominator, other.denominator)
            self.nominator, self.denominator = self.exp_frac(c)
            other.nominator, other.denominator = other.exp_frac(c)
            return self.nominator > other.nominator if self.denominator == other.denominator else print("Error")

    def __ge__(self, other):
        if self.denominator == other.denominator:
            return self.nominator >= other.nominator
        else:
            c = gcd(self.denominator, other.denominator)
            self.nominator, self.denominator = self.exp_frac(c)
            other.nominator, other.denominator = self.exp_frac(c)
            return self.nominator >= other.nominator if self.denominator == other.denominator else print("Error")

    def __add__(self, other):
        if self.denominator == other.denominator:
            return Rational(self.nominator + other.nominator, self.denominator)
        else:
            c = gcd(self.denominator, other.denominator)
            self.denominator, self.nominator = self.exp_frac(c)
            other.denominator, other.nominator = self.exp_frac(c)
            return Rational(self.nominator + other.nominator, self.denominator)

    def __sub__(self, other):
        if self.denominator == other.denominator:
            return Rational(self.nominator - other.nominator, self.denominator)
        else:
            c = gcd(self.denominator, other.denominator)
            self.denominator, self.nominator = self.exp_frac(c)
            other.denominator, other.nominator = self.exp_frac(c)
            return Rational(self.nominator - other.nominator, self.denominator)

    def __divmod__(self, other):
        if self.denominator == other.denominator:
            return Rational(self.nominator - other.nominator, self.denominator)
        else:
            c = gcd(self.denominator, other.denominator)
            self.denominator, self.nominator = self.exp_frac(c)
            other.denominator, other.nominator = self.exp_frac(c)
            return Rational(self.nominator - other.nominator, self.denominator)

    def exp_frac(self, c):
        return self.denominator * c, self.nominator * c

    @classmethod
    def cancel(cls, a, b):
        c = gcd(a, b)
        return a // c, b // c


class B(object):
    def __init__(self, text):
        self.text = text

    def print1(self):
        print(self.text + " " + "I am class B")


class Ski(object):
    _objectCounter = 0

    def __init__(self, name, price):
        self.nameOfRobot = name
        self.__price = price
        type(self)._objectCounter += 1

    def set_with(self, tail_width, set_under_foot_width, top_width):
        self.set_top_with = top_width
        self.set_under_foot_width = set_under_foot_width
        self.set_tail_width = tail_width

    def set_binding(self, typ, brand):
        self.typ = typ
        self.brand = brand

    def show_price(self):
        return str(self.__price) + " Euro"

    @staticmethod
    def numberOfSkis():
        return Ski._objectCounter


if __name__ == '__main__':
    d = Rational(1, 2)
    f = Rational(2, 4)

    print(d, f)
    print(d == f)
    print(d < f)
    print(d > f)
    print(d >= f)
    print(f <= f)

    print(d + f)

    my_ski = Ski("Black Crows", 500)
    my_ski.set_with(110, 105, 113)
    my_ski.set_binding("pin", "G3")

    theresaSki = Ski("4front", 400)

    print("Number of Skis")
    print(Ski.numberOfSkis())
    print(my_ski.show_price())
