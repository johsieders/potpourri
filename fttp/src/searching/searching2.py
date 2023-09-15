# j.siedersleben
# fasttrack to professional programming
# lesson 7: searching
# 12.01.2021

from warmingup.types import Iterator

from searching.conjoin import free_fields


# Java-like interface
class SearchProblem(object):
    def __init__(self):
        pass

    def done(self) -> bool:
        raise NotImplementedError

    def getState(self) -> any:
        raise NotImplementedError

    def __iter__(self) -> Iterator:
        raise NotImplementedError

    def do(self, step):
        raise NotImplementedError

    def undo(self, step):
        raise NotImplementedError


# search by generator
def searchByGenerator(problem: SearchProblem) -> Iterator:
    if problem.done():
        yield problem.getState()

    for step in problem:
        problem.do(step)
        yield from searchByGenerator(problem)
        problem.undo(step)


# search by function
def searchByFunction(problem: SearchProblem) -> list:
    if problem.done():
        return [problem.getState()]

    result = []
    for step in problem:
        problem.do(step)
        result += searchByFunction(problem)
        problem.undo(step)
    return result


# search by Java-like class
class SearchByClass(object):
    def __init__(self, problem: SearchProblem):
        self.problem = problem
        self.solutions = []

    def search(self) -> list:
        if self.problem.done():
            self.solutions.append(self.problem.getState())
            return list(self.solutions)

        for step in self.problem:
            self.problem.do(step)
            self.search()
            self.problem.undo(step)


# permutations as a hello-world search problem
class PermutationProblem(SearchProblem):
    def __init__(self, xs):
        super().__init__()
        self.xs = set(xs)
        self.state = []

    def getState(self) -> list:
        return list(self.state)

    def __iter__(self) -> Iterator:
        return iter(self.xs - set(self.state))

    def do(self, step):
        self.state.append(step)

    def undo(self, step):
        self.state.pop()

    def done(self) -> bool:
        return len(self.state) == len(self.xs)


class QueensProblem(SearchProblem):
    def __init__(self, size):
        super().__init__()
        self.size = size  # number of rows
        self.state = []  # state, see nextPositions

    def done(self):
        return len(self.state) == self.size

    def __iter__(self):
        return iter(free_fields(self.state, self.size))

    def getState(self):
        return list(self.state)

    def do(self, step):
        self.state.append(step)

    def undo(self, step):
        self.state.pop()
