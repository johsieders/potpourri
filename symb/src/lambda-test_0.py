# Johannes Siedersleben, QAware GmbH, Munich, Germany
# 2023-09-14

# Trying to understand lambda calculus using the lambda_calculus package

from lambda_calculus.terms.logic import TRUE, FALSE, AND, OR, NOT, IF_THEN_ELSE
from lambda_calculus.terms.pairs import PAIR, FIRST, SECOND, NIL, NULL

if __name__ == '__main__':
    print(PAIR)
    # p = Application.with_arguments(PAIR, FIRST)

    # print(p)
    # q = Application.with_arguments(p, TRUE)
    # print(q)

    print(FIRST)
    print(SECOND)
    print(NIL)
    print(NULL)

    print(TRUE)
    print(FALSE)
    print(AND)
    print(OR)
    print(NOT)
    print(IF_THEN_ELSE)
