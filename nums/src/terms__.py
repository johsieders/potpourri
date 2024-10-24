# js 29.01.2024
from fields import Field


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


class Product(Field):
    """
    A Product consists of three elements:
    1) the constant which is handled directly
    2) the dictionary of factors (possibly empty) with key = name or value of variable, value = exponent != 0
    3) the dictionary of values of variables (possibly empty) with key = name of variable,
    value = value of variable != None

    Exponents can be constants or variables.
    Products are immutable. All operations (e.g. +, -, *, /, etc.) produce a new object and leave self unchanged
    Invariants:
    The Product is zero if the constant is zero, in which case both tables are empty.
    """

    def __init__(self, x, value=None):
        """
        :param x: x can be a value, a name of a variable or a Product.
        A value or a name will be transformed into a product.
        The value is must accept all arithmetic operations.
        """
        if isinstance(x, str):
            self.constant = 1
            self.factors = {x: 1}
            self.values = {} if value is None else {x: value}
        elif isinstance(x, Product):
            self.constant = x.constant
            self.factors = dict(x.factors)
            self.values = dict(x.values)
        else:
            check_field_operators(x)
            self.constant = x
            self.factors = {}
            self.values = {}

    def __eq__(self, other):
        if isinstance(other, Product):
            return self.constant == other.constant and self.factors == other.factors
        else:
            return self == Product(other)

    def is_constant(self):
        """
        :return: True if there is a constant only, no variables,and no constants with variable exponents
        """
        return len(self.factors) == 0

    def __add__(self, b):
        return Sum(self) + b

    def __sub__(self, other):
        return self + -other

    def __neg__(self):
        return self * -1

    def __mul__(self, other):
        """
        :param other: a value, a Product, or a Sum
        :return: product of self and b
        """
        if self == 0 or other == 0:
            return 0
        if self == 1:
            return other
        if other == 1:
            return self

        result = Product(self)  # (a * b) * (c * d) = a * b * c * d

        if isinstance(other, Product):
            result.constant *= other.constant
            for f, exponent in other.factors.items():  # merge factors
                if f in result.factors:  # add exponents if factors are equal
                    result.factors[f] += exponent
                    if result.factors[f] == 0:  # remove factors with exponent = 0
                        del result.factors[f]
                else:
                    result.factors[f] = exponent  # append new factors

            result.values.update(other.values)

        elif isinstance(other, Sum):  # (a * b) * (c + d) = (a * b * c) + (a * b * c)
            result = Sum(0)
            for summand in other.summands:  # summands are Products
                result += self * summand

        else:  # b is a variable name or a constant
            result = self * Product(other)

        return result

    def inv(self):
        """
        :return: 1 / self
        constant is inverted, exception, if constant == 0
        all exponents of self are multiplied by -1
        """
        result = Product(self)
        result.constant = 1 / result.constant
        for var, exponent in result.factors.items():
            result.factors[var] *= -1
        return result

    def __truediv__(self, other):
        if isinstance(other, Product):
            return self * other.inv()
        else:
            return self / Product(other)

    def __rmul__(self, other):
        if isinstance(other, Product):
            return other.__mul__(self)
        else:
            return Product(other) * self

    def __rtruediv__(self, other):
        if isinstance(other, Product):
            return other / self
        else:
            return Product(other) / self

    def __pow__(self, other):
        """
        :param other: a value, a Product, or a Sum
        :return: self ** exponent
        """
        if self == 0 or other == 1:
            return self
        elif other == 0:
            return 1

        result = Product(self)

        # multiply all exponents in result.values with other (=exponent)
        if isinstance(other, Product) and other.is_constant():
            for f in result.factors:
                result.factors[f] *= other.constant  # multiply exponents with other.constant

            result.constant **= other.constant

        elif isinstance(other, Product) and not other.is_constant():
            for f in result.factors:
                result.factors[f] *= other  # multiply exponents with other

            if abs(result.constant) != 1:
                result.factors[abs(result.constant)] = other  # move result.constant to factors
                result.constant = 1 if result.constant >= 0 else -1
            result.values.update(other.values)

        else:  # b is a variable name or a constant
            result = self ** Product(other)

        return result

    def __rpow__(self, base):
        if isinstance(base, Product):
            return base ** self
        else:
            return Product(base) ** self

    def __call__(self, **kwargs):
        """
        :param kwargs: sets any of the variables in self.var_table,
        overwriting existing values just for this call. self is unchanged.
        :return: a constant if all variables are set, otherwise a Term containing
        all variables which are not set.
        """
        values = dict(self.values)
        values.update(kwargs)

        result = Product(self.constant)
        for f, exponent in self.factors.items():
            base = values[f] if f in values else f
            result *= Product(base) ** Product(exponent)(**kwargs)
        return result.constant if self.is_constant() else result

    def __str__(self):
        str_keys = [str(k) for k in self.factors.keys()]
        factors = sorted(str_keys)
        if self.is_constant():
            return str(self.constant)

        result = [] if self.constant == 1 else [str(self.constant)]

        for f in self.factors.keys():  # todo: brackets
            exponent = self.factors[f]
            str_exponent = f"({exponent})" if isinstance(exponent, Product) and len(exponent.factors) > 1 \
                else f"{exponent}"
            str_f = f if exponent == 1 else f"{f} ** {str_exponent}"
            result.append(str_f)

        return ' * '.join(result)

    def __repr__(self):
        return f"{self.constant} {self.factors} {self.values}"


class Sum(Field):
    """
    A product is a constant factor and a list of variables
    """

    def __init__(self, x, value=None):
        """
        :param x: x can be a value, a string, a Product, or a Sum
        an item or a product
        """
        if isinstance(x, Product):
            self.constant = 0
            self.factors = dict(x.factors)
            self.summands = [x]
        elif isinstance(x, Sum):
            self.factors = dict(x.factors)
            self.summands = list(x.summands)
        else:
            # x is a name or a value
            Sum(Product(x, value))

    def __eq__(self, other):  # todo: correct?
        other = Sum(other)
        return self.summands == other.summands

    def __mul__(self, x):
        """
        :param b: a literal, a Product, or a Sum
        :return: product of self and b
        """
        return Product(x) * self

    def __rmul__(self, b):
        return self.__mul__(b)

    def __pow__(self, b):
        result = Product(self)
        # todo
        return result

    def __rpow__(self, b):
        b = Product(self)
        return b.__pow__(self)

    def __call__(self, **kwargs):
        vt = self.get_ftable()
        vt.update(kwargs)
        result = self.constant
        for s in self.summands:
            result += s(**vt)
        return result

    def __str__(self):
        summands = sorted(self.summands, key=lambda s: len(s.exponents))
        result = [str(self.constant)] if self.constant != 0 or len(summands) == 0 else []
        result += [str(s) for s in self.summands]
        return ' + '.join(result)

    def __repr__(self):
        return f"{self.constant} {self.ftable} {repr(self.summands)}"
