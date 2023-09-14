from types_ import Type


class Function(object):
    """
    the Function class
    """

    def __init__(self, arg_type, res_type):
        """
        :param arg_type: type of argument
        :param res_type: type of result
        """
        super().__init__()
        self.arg_type = arg_type
        self.res_type = res_type

    def args(self):
        """
        :return: list of arguments of this function
        """
        raise NotImplementedError

    def arg_types(self):
        """
        :return: type of argument
        """
        raise NotImplementedError

    def res_type(self):
        """
        :return: type of result
        """
        raise NotImplementedError

    def __call__(self, *x):
        raise NotImplementedError

    def diff(self, arg: str):
        """
        :param arg
        :return: the derivative of self with respect to arg
        """
        raise NotImplementedError


class Plus(Function):
    """
    the Plus class
    """

    def __init__(self, f: Function, g: Function):
        """
        :param f: first argument
        :param g: second argument
        """
        super().__init__(f.arg_type, f.res_type)
        if f.res_type != g.res_type:
            raise ValueError
        self.first = f
        self.second = g

    def args(self):
        return [self.first.args(), self.second.args()]

    def __call__(self, x, y):
        if type(x) == str or type(y) == str:
            return str(x) + '+' + str(y)
        else:
            return self.first(x) + self.second(y)

    def __str__(self):
        return str(self.first) + ' + ' + str(self.second)

    def diff(self, args):
        return Plus(self.first.diff(args), self.second.diff(args))


class Mul(Function):
    """
    the Plus class
    """

    def __init__(self, f: Function, g: Function):
        """
        :param f: first argument
        :param g: second argument
        """
        super().__init__(f.arg_type, f.res_type)
        if f.arg_type != g.arg_type or f.res_type != g.res_type:
            raise ValueError
        self.first = f
        self.second = g

    def __call__(self, x):
        return self.first(x) + self.second(x)

    def __str__(self):
        return str(self.first) + ' + ' + str(self.second)

    def diff(self, idx):
        return Plus(self.diff(self.first), self.diff(self.second))


class Var(Function):
    """
    the Var class
    """

    def __init__(self, var, type: Type):
        """
        :param var: name of variable
        :param type: type of variable
        """
        super().__init__(type, type)
        self.var = var
        self.type = type

    def args(self):
        return [self.var]

    def arg_types(self):
        return [self.type]

    def res_type(self):
        return self.type

    def __str__(self):
        return self.var

    def __call__(self, x):
        return x

    def diff(self, arg):
        if arg == self.var:
            return Const('', self.type, self.type.one())
        else:
            return Const('', self.type, self.type.zero())


class Const(Function):
    """
    the Const class
    """

    def __init__(self, name, type, value):
        """
        :param name: name of constant
        :param type: type of constant
        :param value: value of constant
        """
        super().__init__(type, type)
        self.name = name
        self.type = type
        self.value = value

    def args(self):
        return []

    def arg_types(self):
        return []

    def res_type(self):
        return self.type

    def __str__(self):
        return self.name

    def __call__(self):
        return self.value

    def diff(self, var):
        return Const('', self.type, self.type.zero())


if __name__ == '__main__':
    print()
