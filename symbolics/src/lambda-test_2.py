from lambda_calculus import Variable, Abstraction, Application
from lambda_calculus.visitors.normalisation import BetaNormalisingVisitor

if __name__ == '__main__':
    c17 = Abstraction('x', Variable('17'))
    print(c17)
    result = Application(c17, Variable('a'))
    print(result)
    b = BetaNormalisingVisitor().skip_intermediate(result)
    print(b)

    const = Abstraction('c', Abstraction('x', Variable('c')))
    r17 = Application(Application(const, Variable('17')), Variable('a'))
    print(r17)
    b = BetaNormalisingVisitor().skip_intermediate(r17)
    print(b)

    print(r17.free_variables())
    print(r17.bound_variables())
