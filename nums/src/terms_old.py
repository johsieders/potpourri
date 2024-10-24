# js 29.01.2024

from rings import Ring


class Term(Ring):
    """
    This is an abstract superclass for symbolic computation
    """

    def eval(self):
        raise NotImplementedError

    def transform(self, x):
        if isinstance(x, Term):
            return x
        elif isinstance(x, str):
            return Variable(x)
        else:
            return Constant(x)

    def add_constant(self, b):
        return Add(b, self)

    def add_variable(self, b):
        return Add(b, self)

    def add_sum(self, b):
        return Add(b, self)

    def add_product(self, b):
        return Add(b, self)

    def add(self, b):
        raise NotImplementedError

    def sub(self, b):
        raise NotImplementedError

    def mul(self, b):
        raise NotImplementedError

    def __pow__(self, b):
        b = self.transform(b)
        return Pow(self, b)

    def __neg__(self):
        return Neg(self)


class Constant(Term):
    def __init__(self, value):
        self.value = value

    def add_constant(self, b):
        return Constant(self.value + b.val)

    def sub_constant(self, b):
        return Constant(self.value - b.val)

    def mul_constant(self, b):
        return Constant(self.value * b.val)

    def add(self, b):
        return b.add_constant(self)

    def sub(self, b):
        return b.sub_constant(self)

    def mul(self, b):
        return b.mul_constant(self)

    def eval(self):
        return self.value

    def __str__(self):
        return str(self.value)

    def __len__(self):
        return 1


class Variable(Term):
    def __init__(self, name, value=None):
        if len(name) == 0 or not name[0].islower():
            raise ValueError("first character must be lowercase")
        self.name = name
        self.value = value

    def set_value(self, value):
        self.value = value

    def add(self, b):
        return b.add_variable(self)

    def sub(self, b):
        return b.sub_variable(self)

    def mul(self, b):
        return b.mul_variable(self)

    def eval(self):
        return self if self.value is None else self.value

    def __str__(self):
        return f"[{self.name}: {self.value}]" if self.value else self.name

    def __len__(self):
        return 1


class Add(Term):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def add_constant(self, b):
        if isinstance(self.left, Constant):
            self.left = self.left.add_constant(b)
            return self
        elif isinstance(self.right, Constant):
            self.right = self.right.add_constant(b)
            return self
        else:
            return Add(self, b)

    def mul_constant(self, b):
        """
        multiply self (= left + right) with b
        :param b: a factor
        :return: self * b
        """
        if isinstance(self.left, Constant):
            self.left = self.left.mul_constant(b)
            return self
        elif isinstance(self.right, Constant):
            self.right = self.right.mul_constant(b)
            return self
        else:
            return Mul(self, b)

    def mul_sum(self, b):
        """
        :param b: the term to be multiplied with self which is a sum
        :return: (left + right) * b = left * b + right * b
        """
        return self.left * b + self.right * b

    def add(self, b):
        return b.add_sum(self)

    def sub(self, b):
        return b.sub_sum(self)

    def mul(self, b):
        return b.mul_sum(self)

    def eval(self):
        return self.left.eval() + self.right.eval()

    def __str__(self):
        return f"{str(self.left)} + {str(self.right)}"

    def __len__(self):
        return len(self.left) + len(self.right)


class Sub(Term):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def add(self, b):
        return b.add_diff(self)

    def eval(self):
        return self.left.eval() - self.right.eval()

    def __str__(self):
        return f"{str(self.left)} - {str(self.right)}"

    def __len__(self):
        return len(self.left) + len(self.right)


class Mul(Term):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def add(self, b):
        return b.add_prod(self)

    def eval(self):
        return self.left.eval() * self.right.eval()

    def __str__(self):
        return f"{str(self.left)} * {str(self.right)}"

    def __len__(self):
        return len(self.left) + len(self.right)


class Pow(Term):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def add(self, b):
        return b.add_power(self)

    def eval(self):
        return self.left.eval() ** self.right.eval()

    def __str__(self):
        return f"{str(self.left)} ** {str(self.right)}"

    def __len__(self):
        return len(self.left) + len(self.right)


class Neg(Term):
    def __init__(self, left):
        self.left = left

    def eval(self):
        return -self.left.eval()

    def __str__(self):
        return '-' + str(self.left)

    def __len__(self):
        return len(self.left)
