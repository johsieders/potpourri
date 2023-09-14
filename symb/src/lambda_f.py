# lambda calculus with f
# J. Siedersleben, 30.08.2023


def cons_(*args):
    return args, f'({args[2]} {args[0]} {args[1]})'


class Term(object):
    def __init__(self, bound_vars, body):
        self.bound_vars = bound_vars
        self.body = body

    def __str__(self):
        return str(self.body)

    def __call__(self, var):
        return self.term(*args)


class cons(object):
    def term(self, *args):
        return f'({str(args[2])} {str(args[0])} {str(args[1])})'

    def __call__(self, *args):
        return args, self.term(*args)


def curry(f, arg):
    def g(*args):
        return f(arg, *args)

    return g


if __name__ == '__main__':
    a, b = cons_('x', 'y', 'f')
    u, v = curry(cons_, 'a')('b', 'g')

    c = cons()
    x, y = c('x', 'y', 'f')

    print(a, b)
