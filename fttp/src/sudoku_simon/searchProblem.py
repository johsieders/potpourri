# s.siedersleben
# fasttrack to professional programming
# lesson ??: programming the sudoku_simon game
# 27.1.2021
from typing import Iterator


class SearchProblem(object):
    def __init__(self):
        pass

    def done(self) -> bool:
        raise NotImplementedError

    def get_state(self) -> any:
        raise NotImplementedError

    def __iter__(self) -> Iterator:
        raise NotImplementedError

    def do_step(self, step):
        raise NotImplementedError

    def undo_step(self, step):
        raise NotImplementedError


def search_by_function(problem: SearchProblem) -> list:
    if problem.done():
        return problem.get_state()
    result = []
    for step in problem:
        problem.do_step(step)
        result += search_by_function(problem)
        problem.undo_step(step)
    return result
