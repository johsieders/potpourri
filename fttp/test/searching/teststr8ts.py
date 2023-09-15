## checkInvariants Str8ts
## js 3.4.2010

from unittest import TestCase, TextTestRunner, makeSuite

from datastr8ts import void, t1, t2, t3
from search import searchByFunction, searchByGenerator
from str8ts import Str8tsProblem

newline = '\n'


class TestStr8ts(TestCase):
    def testvg(self):
        r = searchByGenerator(Str8tsProblem(void))
        print
        newline, r.next()

    def test1f(self):
        r = searchByFunction(Str8tsProblem(t1))
        print
        newline, r[0]

    def test1g(self):
        r = searchByGenerator(Str8tsProblem(t1))
        print
        newline, r.next()

    ##    def test1c(self):
    ##        r = SearchByClass(Str8tsProblem(t1)).search()
    ##        print r[0]

    def test2f(self):
        r = searchByFunction(Str8tsProblem(t2))
        print
        newline, r[0]

    def test2g(self):
        r = searchByGenerator(Str8tsProblem(t2))
        print
        newline, r.next()

    def test3f(self):
        r = searchByFunction(Str8tsProblem(t3))
        print
        newline, r[0]

    def test3g(self):
        r = searchByGenerator(Str8tsProblem(t3))
        print
        newline, r.next()


def suite():
    return makeSuite(TestStr8ts)


if __name__ == '__main__':
    runner = TextTestRunner()
    runner.run(suite())
