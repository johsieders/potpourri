from lambda_calculus import Variable, Abstraction, Application
from lambda_calculus.visitors.normalisation import BetaNormalisingVisitor

if __name__ == '__main__':
    # Nesting
    term = Application(Variable("+"), Variable("x"))
    term = Application(term, Variable("y"))
    term = Abstraction("y", term)
    term = Abstraction("x", term)
    term = Application(term, Variable("y"))
    term = Application(term, Variable("3"))
    term = Abstraction("y", term)
    term = Application(term, Variable("4"))

    # Utilities
    x = Variable.with_valid_name("x")
    y = Variable.with_valid_name("y")

    term1 = Application.with_arguments(Variable.with_valid_name("+"), (x, y))
    term1 = Abstraction.curried(("x", "y"), term1)
    term1 = Application.with_arguments(term1, (y, Variable.with_valid_name("3")))
    term1 = Abstraction("y", term1)
    term1 = Application(term1, Variable.with_valid_name("4"))

    # Method chaining
    term2 = Variable("+") \
        .apply_to(x, y) \
        .abstract("x", "y") \
        .apply_to(y, Variable("3")) \
        .abstract("y") \
        .apply_to(Variable("4"))

    # Evaluation
    b = BetaNormalisingVisitor().skip_intermediate(term2)
    print(b)

    a = Application.with_arguments(
        Variable("+"),
        (Variable("4"), Variable("3"))
    )
    print(a)

    # term = TRUE
    # x = Variable('x')
    # y = Variable('y')
    # z = Variable('z')
    # t = Variable('t')
    #
    # first = Application(Application(TRUE, x), y)
    #
    # print(term)
    # print(x)
    # print(first)
    # first.beta_reduction()
    # print(first)
