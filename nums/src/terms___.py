# js 29.01.2024

class Term(object):
    def __eq__(self, other):
        raise NotImplementedError

    def __neg__(self):
        raise NotImplementedError

    def gcd(self, other):
        raise NotImplementedError

    def __call__(self, **kwargs):
        raise NotImplementedError

    def __add__(self, other):
        return Sum(self) + other

    def __radd__(self, other):
        return Sum(other) + self

    def __sub__(self, other):
        return Sum(self) + -other

    def __rsub__(self, other):
        return Sum(other) + -self

    def __mul__(self, other):
        return Product(self) * other

    def __rmul__(self, other):
        return Product(other) * self

    def __pow__(self, other):
        return Power(self) ** other

    def __rpow__(self, other):
        return Power(other) ** self

    def __truediv__(self, other):
        return self * other ** -1

    def __rtruediv__(self, other):
        return other * self ** -1


def check_field_operators(val):
    """
    :param val: any value
    :return: None
    This function checks if val supports the arithmetic operations.
    If not, it raises a ValueError
    """
    try:  # x must be a value which supports arithmetic operations
        a, b, c, d, e, f, g = val + val, val * val, -val, val == 0, val * 0, val * 1, val / 1
    except Exception:
        raise ValueError(f"{val} doesn't support arithmetic operations")


class Value(Term):
    def __init__(self, v):
        if isinstance(v, Value):
            self.val = v.val
        else:
            check_field_operators(v)
            self.val = v

    def __eq__(self, other):
        if isinstance(other, Value):
            return self.val == other.val
        else:
            return self == Value(other)

    def __neg__(self):
        return Value(-self.val)

    def __add__(self, other):
        if isinstance(other, Value):
            return Value(self.val + other.val)
        else:
            return other.__radd__(self.val)

    def __radd__(self, other):
        if isinstance(other, Value):
            return Value(other.val + self.val)
        else:
            return other + self.val

    def __mul__(self, other):
        if isinstance(other, Value):
            return Value(self.val * other.val)
        else:
            return other.__rmul__(self.val)

    def __rmul__(self, other):
        if isinstance(other, Value):
            return Value(other.val * self.val)
        else:
            return other * self.val

    def __truediv__(self, other):
        if isinstance(other, Value):
            return Value(self.val / other.val)
        else:
            return other.__rtruediv__(self.val)

    def __rtruediv__(self, other):
        if isinstance(other, Value):
            return Value(other.val / self.val)
        else:
            return other / self.val

    def __pow__(self, other):
        if isinstance(other, Value):
            return Value(self.val ** other.val)
        else:
            return other.__rpow__(self.val)

    def __rpow__(self, other):
        if isinstance(other, Value):
            return Value(other.val ** self.val)
        else:
            return other ** self.val

    def __call__(self, **kwargs):
        return self.val

    def __str__(self):
        return str(self.val)


class Identifier(Term):
    def __init__(self, id, val=None):
        if isinstance(id, Identifier):
            self.identifier = id.identifier
            self.val = id.val
        elif isinstance(id, str):
            if val is None:
                self.val = None
            else:
                self.val = Value(val)
            if id[0].islower():
                self.identifier = id
            else:
                raise ValueError(f"illegal {id}")
        else:
            raise ValueError(f"illegal arguments for Identifier")

    def __eq__(self, other):
        if isinstance(other, Identifier):
            return self.identifier == other.identifier
        else:
            return self == Identifier(other)

    def __neg__(self):
        return Product(self) * -1

    def __call__(self, **kwargs):  # todo
        if self.val is None:
            return self.identifier
        else:
            return self.val(**kwargs)

    def __str__(self):
        return f"{self.identifier}={self.val}"


class Product(Term):
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

    def __init__(self, x=None):
        """
        :param x: can be a Value, an Identifier, a Product, a Sum, a Power, or a raw value
        """
        if x is None:
            self.val = Value(1)
            self.factors = set()
        elif isinstance(x, Value):
            self.val = x.val
            self.factors = set()
        elif isinstance(x, str):
            self.val = 1
            self.factors = {Identifier(x)}
        elif isinstance(x, Identifier) or isinstance(x, Sum) or isinstance(x, Power):
            self.val = 1
            self.factors = {x}
        elif isinstance(x, Product):
            self.val = x.val
            self.factors = x.factors
        else:
            self.val = Value(x)
            self.factors = set()

    def __eq__(self, other):
        if isinstance(other, Product):
            return self.val == other.val and self.factors == other.factors
        else:
            return self == Product(other)

    def __len__(self):
        """
        :return:
        """
        return len(self.factors)

    def __neg__(self):
        result = Product(self)
        result.val *= -1
        return result

    def gcd(self, other):
        if isinstance(other, Product):
            gcd = Product(1)
            for f in set(self.factors) & set(other.factors):
                gcd *= f
            return gcd

    def __mul__(self, other):
        """
        :param other: a value, a Product, or a Sum
        :return: product of self and other
        """
        if self == 0 or other == 0:
            return 0
        elif self == 1:
            return other
        elif other == 1:
            return self

        # (a * b) * (c * d) = a * b * c * d

        if isinstance(other, Value):
            result = Product(self)
            result.val *= other.val

        elif isinstance(other, str):
            result = self * Product(other)

        elif isinstance(other, Product):
            result = Product(self)
            result.val *= other.val
            result.factors = {}
            aux = sorted(result.factors | other.factors)
            for i, f in enumerate(aux[-1]):
                g = aux[i + 1]
                if f == g:
                    result.factors.append(Power(f))
                else:
                    result.factors.append(f)


        elif isinstance(other, Sum):  # (a * b) * (c + d) = (a * b * c) + (a * b * d)
            result = Sum(0)
            for s in other.summands:
                result += self * s

        else:  # b is  a value or a Power
            result = self * Product(other)

        return result

    def __truediv__(self, other):
        if isinstance(other, Product):
            return self * other ** -1
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

        return Product(self) ** other

    def __rpow__(self, other):
        return Product(other) ** self

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


class Sum(Term):
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


class Power(Term):
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

    def __init__(self, x=None):
        """
        :param x: can be a Value, an Identifier, a Product, a Sum, a Power, or a raw value
        """
        if x is None:
            self.value = Value(1)
            self.factors = []
        elif isinstance(x, str):
            self.value = 1
            self.factors = [Identifier(x)]
        elif isinstance(x, Product):
            self.value = x.val
            self.factors = x.factors
        elif isinstance(x, Sum):
            self.value = 1
            self.factors = [x]
        elif isinstance(x, Power):
            self.value = 1
            self.factors = [x]
        else:
            self.value = Value(x)
            self.factors = []

    def __eq__(self, other):
        if isinstance(other, Product):
            return self.value == other.val and self.factors == other.factors
        else:
            return self == Product(other)

    def __len__(self):
        """
        :return:
        """
        return len(self.factors)

    def __neg__(self):
        result = Product(self)
        result.val *= -1
        return result

    def __mul__(self, other):
        """
        :param other: a value, a Product, or a Sum
        :return: product of self and other
        """
        if self == 0 or other == 0:
            return 0
        elif self == 1:
            return other
        elif other == 1:
            return self

        # (a * b) * (c * d) = a * b * c * d

        if isinstance(other, Value):
            result = Product(self)
            result.val *= other.val
            return result
        elif isinstance(other, str):
            pass

        elif isinstance(other, Product):
            tmp_value = self.value * other.val
            tmp_factors = self.factors + other.factors
            for f in set(tmp_factors):
                cnt = tmp_factors.count(f)
                if cnt == 1:
                    result.factors.append(f)
                else:
                    result.factors.append(Power(f, cnt))


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
