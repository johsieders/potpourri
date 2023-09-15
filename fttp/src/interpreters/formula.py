# 

from __future__ import nested_scopes


def interpret(formula, dictionary):
    """ Interpretation einer Formel in Postfix-Form
    Erlaubte Operatoren: AND, OR, NOT
    Das dictionary enth�lt die auszuf�hrenden Funktionen """

    stack = []
    for token in formula.split():
        if token == "AND":
            p = stack.pop()
            q = stack.pop()
            stack.append(lambda x: q(x) & p(x))
        elif token == "OR":
            p = stack.pop()
            q = stack.pop()
            stack.append(lambda x: q(x) | p(x))
        elif token == "NOT":
            p = stack.pop()
            stack.append(lambda x: not p(x))
        else:
            stack.append(dictionary[token])
    return stack.pop()
