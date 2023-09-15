from typing import List

from types_ import Type


class Function(object):
    """
    the Function class
    """

    def __init__(self, *fs):
        self.args = merge_args(*fs)

    def match_arg(self, arg):
        return arg in self.args if arg in self.args else None

    def get_args(self):
        """
        :return: list of arguments of this function
        """
        return self.args


def merge_args(*fs: Function) -> List[Function]:
    """
    :param fs: functions
    :returns: union of fs with no duplicates
    """
    merge = []
    for f in fs:
        if f not in merge:
            merge.append(f)
    return merge


class Plus(Function):
    """
    the Plus class
    """

    def __call__(self, *x):
        return Plus(*x)

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
