# j.siedersleben
# fasttrack to professional programming
# lesson 4: classes_
# 13.12.2020


from collections.abc import MutableSequence


# The first example shows how subclasses extend a method of their superclass.
# There are three classes_: A(object), B(A) and C(A).

class A(object):
    def __init__(self, text):
        """
        A constructor
        :param text: any text
        """
        self.text = text

    def print1(self):
        print(self.text + ': I am A')


class B(A):
    def __init__(self, text):
        """
        A constructor calling the constructor of the superclass
        :param text:
        """
        super().__init__(text)

    def print1(self):
        """
        A method extending the method of the superclass
        :return: None
        """
        super().print1()
        print(self.text + ': I am B')


class C(A):
    def __init__(self, text):
        """
        A constructor calling the constructor of the superclass
        :param text:
        """
        super().__init__(text)

    def print1(self):
        """
        A method extending the method of the superclass
        :return: None
        """
        super().print1()
        print(self.text + ': I am C')


# The second example shows how subclasses provide a method which is abstract in the superclass
# There are three classes_: D(object), F(D) and E(D).

class D(object):
    def __init__(self, text):
        """
        A constructor
        :param text: any text
        """
        self.text = text

    def print1(self):
        print(self.text + ': I am D1')
        self.print2()

    def print2(self):
        """
        an abstract method to be supplied by subclass
        :return:
        """
        raise NotImplementedError


class E(D):
    def __init__(self, text):
        """
        A constructor calling the constructor of the superclass
        :param text:
        """
        super().__init__(text)

    def print2(self):
        """
        A method extending the method of the superclass
        :return: None
        """
        print(self.text + ': I am E2')


class F(D):
    def __init__(self, text):
        """
        A constructor calling the constructor of the superclass
        :param text:
        """
        super().__init__(text)

    def print2(self):
        """
       Supplying a method which is abstract in the superclass
        :return: None
        """
        print(self.text + ': I am F2')


###################################################################
## The third example shows how subclasses implement an interface ##
## (= a class with no implemented methods)                       ##
## There are three classes_: I(object), G(I) and H(I).            ##
###################################################################

class I(object):

    def print1(self):
        """
        an abstract method to be supplied by subclass
        :return:
        """
        raise NotImplementedError

    def print2(self):
        """
        an abstract method to be supplied by subclass
        :return:
        """
        raise NotImplementedError


class G(I):
    def __init__(self, text):
        """
        A constructor calling the constructor of the superclass
        :param text:
        """
        super().__init__()
        self.text = text

    def print1(self):
        """
        A method implementing an abstract method of the superclass
        :return: None
        """
        print(self.text + ': I am G1')

    def print2(self):
        """
         A method implementing an abstract method of the superclass
        :return: None
        """
        print(self.text + ': I am G2')


class H(I):
    def __init__(self, text):
        """
        A constructor calling the constructor of the superclass
        :param text:
        """
        super().__init__()
        self.text = text

    def print1(self):
        """
       Supplying a method which is abstract in the superclass
        :return: None
        """
        print(self.text + ': I am H1')

    def print2(self):
        """
       Supplying a method which is abstract in the superclass
        :return: None
        """
        print(self.text + ': I am H2')


def process(xs: MutableSequence[any]):
    for x in xs:
        x.print1()
    print()


#################################################################################
## This example shows how classes_ work.                                        ##
## A class defines a namespace.                                                ##
## Classes can be nested to any level (as you would expect for a namespace)    ##
##                                                                             ##
## Functions declared at class level are called methods.                       ##
## Variables defined at class level are called static variables.               ##
## They exist only once.                                                       ##
## Variables defined inside the constructor and qualified by self              ##
## (e.g. self.w) are called instance variables. They exist once per instance.  ##
##                                                                             ##
## Whatever is inside the class can be accessed via the class, e.g. X.z        ##
##                                                                             ##
## Methods accesssed via the class behave like any other function.             ##
## Methods accessed by an instance have the first argument replaced by         ##
## this instance which is called self. They accept one argument less.          ##
##                                                                             ##
## Methods defined inside a class and preceded with @staticmethod              ##
## leave the first argument alone.                                             ##
##                                                                             ##
## Classes can be amended at any time                                          ##
#################################################################################

def hello(a, b):
    print(a, b)


def bye(a):
    print(a)


def seeyou(a):
    print(a)


class X:
    z = 0

    m1 = hello  # class level; takes two arguments

    m2 = bye  # class level

    def __init__(self, w):
        self.w = w

    def __str__(self):
        return str(self.w)

    @staticmethod
    def m3(a, b):
        print(10 * a, 10 * b)


if __name__ == '__main__':
    x = X(4)  # an instance of X

    print(X.z)  # z accessed via X  --> 0
    print(x.z)  # z accessed via x  --> 0
    X.m1(1, 2)  # m1 called via X with two explicit arguments --> 1, 2
    X.m2(3)  # m2 called via X with one explicit argument  --> 3
    x.m1(5)  # m1 called via X with one explicit argument  --> 4, 5
    x.m2()  # m1 called via X with no explicit argument --> 4
    X.m3(1, 2)  # m3 called via X with two explicit arguments --> 10, 20
    x.m3(2, 3)  # m3 called via X with two explicit arguments --> 20, 30

    # X can be amended any time
    X.y = 42
    X.m4 = seeyou

    print(X.y)  # y accessed via X --> 42
    X.m4(9)  # m4 called via X with one explicit argument  --> 9
    x.m4()  # m4 called via x with no explicit argument  --> 4

    # no checkInvariants driver; there is nothing to assert

    # a = A('servus')
    # b = B('hello')
    # c = C('hallo')
    #
    # process([a, b, c])
    #
    # d = D('servus')
    # e = E('hello')
    # f = F('hallo')
    #
    # # don't call d.print1()
    # process([e, f])
    #
    # #  i = I()   not useful
    # g = G('hello')
    # h = H('hallo')
    #
    # process([g, h])
