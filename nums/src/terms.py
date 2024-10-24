# js 18.02.2024

from typing import Callable, List


def merge_operands(xs: List, ys: List, f: Callable):
    """
    replaces two operands with one, so a + a + b -> a * 2 + b or a * a * b -> a ** 2 * b
    It is assumed that xs and ys contain no doubles, so each operand appears at most twice.
    :param xs: a list of operands
    :param ys: another list of operands
    :param f: a function such as x * 2, or x ** 2
    :return: xs + ys with double operands replaced
    """

    def aux(zs, f):
        if len(zs) < 2:
            return zs
        elif zs[0] == zs[1]:
            return [f(zs[0])] + aux(zs[2:], f)
        else:
            return [zs[0]] + aux(zs[1:], f)

    return aux(sorted(xs + ys), f)


def merge_factors(xs: List, ys: List):
    """
    replaces two operands with one, so a + a + b -> a * 2 + b or a * a * b -> a ** 2 * b
    It is assumed that xs and ys contain no doubles, so each operand appears at most twice.
    :param xs: a list of powers
    :param ys: another list of powers
    :param f: a function such as x * 2, or x ** 2
    :return: xs + ys with double operands replaced
    """
    factors = {}
    for f in xs + ys:
        if f.base not in factors:
            factors[f.base] = f.exponent
        else:
            factors[f.base] += f.exponent
    return factors


def eval(x, **kwargs):
    """
    :param x: a value, a variable, a Product, a Sum, or a Power
    :param kwargs: a dictionary which assigns values to variables
    :return: a Term with all variables in kwargs replaced by their value.
    The result is a term if there is at least one value left, a value otherwise.
    """
    if isinstance(x, (Product, Sum, Power)):
        return x(**kwargs)
    elif isinstance(x, str) and x in kwargs.keys():
        return kwargs[x]
    else:
        return x


def check_field_operators(x):
    """
    :param x: any value
    :return: None
    This function checks if x supports the field operations.
    If not, it raises a ValueError
    """
    try:  # x must be a value which supports arithmetic operations
        a, b, c, d, e, f, g = x + x, x * x, -x, x == 0, x * 0, x * 1, x / 1
    except Exception:
        raise ValueError(f"{x} doesn't support arithmetic operations")


class Term(object):
    def __add__(self, other):
        """
        :param other: a value, a variable, a Product, a Sum, or a Power
        :return: the sum of self and other
        To be overwritten by Sum
        """
        return Sum(self) + other

    def __radd__(self, other):
        """
        :param other: a value, a variable, a Product, a Sum, or a Power
        :return: the sum of other and self
        """
        return Sum(other) + self

    def __sub__(self, other):
        return self.__add__(-other)

    def __rsub__(self, other):
        return other - self

    def __neg__(self):
        return Product(self) * -1

    def __mul__(self, other):
        """
        :param other: a value, a variable, a Product, a Sum, or a Power
        :return: product of self and other
        To be overwritten by Product; here, self is never a Product
        """
        return Product(self) * other

    def __pow__(self, other):
        """
        :param other: a value, a variable, a Product, or a Sum, or a Power
        :return: self ** other
        To be overwritten by Power; here, self is never a Power
        """
        return Power(self) ** other

    def __truediv__(self, other):
        return self * other ** -1

    def __rmul__(self, other):
        return Product(other) * self

    def __rtruediv__(self, other):
        return other / self

    def __rpow__(self, base):
        return Power(base) ** self

    def __call__(self, **kwargs):
        """
        :param kwargs: sets any of the variables contained in this term (= self)
        :return: a constant if all variables are set, otherwise a Term containing
        all variables which are not set.
        """
        raise NotImplementedError


class Product(Term):
    """
    A Product consists of two elements:
    1) the constant
    2) the list of factors. A factor can be a value, a variable, a Sum, or a Power. It cannot be a Product.

    A Product is zero iff its constant is zero, in which case the list of factors is empty.

    Two Products are equal iff their constants and their factors are equal.

    Primitives are supposed to support arithmetic operations: they can be elements of a Ring (e.g. matrices),
    an Euclidian Ring (e.g. integers, Polynomials), or a Field (e.g. reals, O2)
    Names start with a lowercase letter (e.g. 'a') and are otherwise arbitrary. A name can have or have not a value
    assigned in the values dictionary
    Products are immutable.
    All operations (e.g. +, -, *, /, **, etc.) produce a new object and leave self unchanged
    """

    def __init__(self, x):
        """
        :param x: x can be a value, a variable, a Product, a Sum, or a Power
        """
        if isinstance(x, (str, Sum, Power)):
            self.constant = 1
            self.factors = [x]
        else:
            check_field_operators(x)
            self.constant = x
            self.factors = []

    def __eq__(self, other):
        if isinstance(other, Product):
            return self.constant == other.constant and self.factors == other.factors
        else:
            return self == Product(other)

    def __len__(self):
        """
        :return: number of exponents >= 0
        """
        return len(self.factors)

    def __mul__(self, other):
        """
        :param other: a Product, a Sum
        :return: product of self and b
        """
        if self == 0 or other == 0:
            return 0
        elif self == 1:
            return other
        elif other == 1:
            return self
        elif self == other:
            return self ** 2

        elif isinstance(other, Product):  # (a * b) * (c * d) = a * b * c * d
            result = Product(self.constant * other.constant)
            # result.factors = merge_operands(self.factors, other.factors, lambda x: x ** 2)
            result.factors = self.factors + other.factors
            return result

        elif isinstance(other, Sum):  # (a * b) * (c + d) = (a * b * c) + (a * b * c)
            result = Sum(0)
            for summand in other.summands:  # summands are variables, Products, Sums, or Powers
                result += self * summand
            return result

        else:  # other is a constant, a variable, or a Power
            return self * Product(other)

    def __call__(self, **kwargs):
        """
        :param kwargs: sets any of the variables in self, just for this call.
        self is unchanged.
        :return: a constant if all variables are set, otherwise a Term containing
        all variables which are not set.
        """

        result = Product(self.constant)
        for f in self.factors:
            result *= eval(f, **kwargs)
        return result.constant if len(result) == 0 else result

    def __str__(self):
        result = [] if self.constant == 1 else [str(self.constant)]
        for f in self.factors:
            result.append(str(f))
        return ' * '.join(result)

    def __repr__(self):
        return f"{self.constant} {self.factors}"


class Sum(Term):
    """
    A Sum consists of two elements:
    1) the constant (a primitive)
    2) the list of summands (possibly empty); each summand is a Product, no summand is zero

    Datatypes:

    The constant is primitive (an element of a ring, Euclidean ring or field)
    All summands are Products
    The values are key: string; value: primitive

    A Sum is zero iff its constant is zero and the list of summands is empty

    Two Sums are equal iff their constants and their summands are equal.
    The value table is not taken into account.
    """

    def __init__(self, x):
        """
        :param x: x can be a value, a variable, a Product, or a Power
        """
        if isinstance(x, (str, Product, Power)):
            self.constant = 0
            self.summands = [x]
        else:
            check_field_operators(x)
            self.constant = x
            self.summands = []

    def __eq__(self, other):
        if isinstance(other, Sum):
            return self.constant == other.constant and self.summands == other.summands
        else:
            return self == Sum(other)

    def __len__(self):
        return len(self.summands)

    def __add__(self, other):
        """
        :param other:  a primitive, a name, a Product, or a Sum.
        :return: Sum of self and other
        """
        if isinstance(other, Sum):  # (a + b) + (c + d) = a + b + c + d
            result = Sum(self.constant + other.constant)
            # result.summands = merge_operands(self.summands, other.summands, lambda x: x * 2)
            result.summands = self.summands + other.summands
            return result

        else:
            return self + Sum(other)

    def __call__(self, **kwargs):
        """
        :param kwargs: sets any of the variables in self, just for this call.
        self is unchanged.
        :return: a constant if all variables are set, otherwise a Term containing
        all variables which are not set.
        """
        result = Sum(self.constant)
        for f in self.summands:
            result += eval(f, **kwargs)
        return result.constant if len(result) == 0 else result

    def __str__(self):
        result = [] if self.constant == 0 else [str(self.constant)]
        for f in self.summands:
            result.append(str(f))
        return ' + '.join(result)

    def __repr__(self):
        return f"{self.constant} {repr(self.summands)}"


class Power(Term):
    """
    Power objects support the ** operand.
    They consist of a base and an exponent.
    The base and exponent can be a value, a variable, a Product, or a Sum
    The exponent can be a value, a variable, a Product, a Sum, or a Power
    """

    def __init__(self, x):
        """
        :param x: x can be a value, a variable, a Product, a Sum, or a Power
        """

        if isinstance(x, (str, Product, Sum)):
            self.constant = 1
            self.base = x
            self.exponent = Product(1)
        else:
            check_field_operators(x)
            self.constant = x
            self.base = Product(1)
            self.exponent = Product(1)

    def __eq__(self, other):
        if isinstance(other, Power):
            return (self.constant == other.constant and
                    self.base == other.base and
                    self.exponent == other.exponent)
        else:
            return self == Power(other)

    def __pow__(self, other):
        """
        :param other: a value, a Product, or a Sum
        :return: self ** other
        """
        if self == 0 or other == 1:
            return self
        elif other == 0:
            return 1
        elif isinstance(other, (str, Product, Sum)):
            result = Power(self.constant) ** other
            result.exponent = self.exponent * other
            return result

    def __call__(self, **kwargs):
        """
        :param kwargs: sets any of the variables in self.var_table,
        overwriting existing values just for this call. self is unchanged.
        :return: a constant if all variables are set, otherwise a Term containing
        all variables which are not set.
        """
        result = self.constant * self.base(**kwargs)
        return result ** self.exponent(**kwargs)

    def __str__(self):
        constant_str = '' if self.constant == 1 else f"{self.constant} * "
        exponent_str = '' if self.exponent == 1 else f" ** {self.exponent}"
        return f"{constant_str} {self.base} {exponent_str}"

    def __repr__(self):
        return f"{self.constant} {self.base} {self.exponent}"
