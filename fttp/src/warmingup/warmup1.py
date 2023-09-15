def fibo(n):
    """
    :param n: integer >= 0
    :return: nte Fibonacci-Zahl
    """
    if n < 0:
        raise ValueError
    elif n == 0:
        return 0

    result = [0, 1]
    for _ in range(2, n + 1):
        result.append(result[-2] + result[-1])
    return result[-1]


def fibo1(n):
    """
    :param n: integer >= 0
    :return: nte Fibonacci-Zahl
    """
    if n < 0:
        raise ValueError
    elif n == 0:
        return 0

    a = 0
    b = 1
    for _ in range(2, n + 1):
        a, b = b, a + b
        # c = a + b
        # a = b
        # b = c
    return b


def fibo2(n):
    """
    :param n: integer >= 0
    :return: nte Fibonacci-Zahl
    """
    if n < 0:
        raise ValueError
    elif n == 0:
        return 0
    elif n == 1:
        return 1

    return fibo2(n - 2) + fibo2(n - 1)


def gca(a, b):
    """
    :param a: integer
    :param b: integer
    :return: gca
    """

    if (a == 0) | (b == 0):
        return 1

    if b >= a:
        a, b = b, a

    result = [a, b, a % b]
    while result[-1] > 0:
        result.append(result[-2] % result[-1])
        # print(result)
    return result[-2]


def gca1(a, b):
    """
    :param a: integer
    :param b: integer
    :return: gca
    """

    if (a == 0) | (b == 0):
        return 1
    elif b >= a:
        a, b = b, a

    #  c = a % b
    #  while c != 0:
    while a % b != 0:
        #  a = b
        #  b = c
        #  c = a % b
        a, b = b, a % b
    return b


def gca2(a, b):
    """
    :param a: integer
    :param b: integer
    :return: gca
    """

    if (a == 0) | (b == 0):
        return 1
    elif b >= a:
        a, b = b, a

    if a % b == 0:
        return b

    return gca(b, a % b)


def faculty(n):
    """
    :param n: integer
    :return:  nth-faculty
    """

    if n < 0:
        raise ValueError
    elif n == 0:
        return 1

    result = 1
    for i in range(2, n + 1):
        result = i * result
    return result


def faculty1(n):
    """
    :param n: integer
    :return:  nth-faculty
    """

    if n < 0:
        raise ValueError
    elif n == 0:
        return 1

    return faculty1(n - 1) * n


def exp_coeff(n, x):
    """
    :param n: positive integer
    :param x: real
    :return: nth value of the exponentional function at a = 0
    """

    if n <= 0:
        raise ValueError
    elif n == 1:
        return 1

    result = 1
    for i in range(1, n):
        result = result + x ** i / faculty(i)
    return result


def exp_coeff1(n, x):
    """
    :param n: positive integer
    :param x: real
    :return: nth value of the exponentional function at a = 0
    """

    if n <= 0:
        raise ValueError
    elif n == 1:
        return 1

    return x ** (n - 1) / faculty(n - 1) + exp_coeff1(n - 1, x)


def reverse(xs):
    """
    :param xs: guess what
    :return: a reversed list
    """

    if not xs:
        return []

    xs_reverse = []
    for x in xs[::-1]:
        xs_reverse.append(x)
    return xs_reverse


def reverse1(xs):
    """
    :param xs: guess what
    :return: a reversed list
    """
    return xs[::-1]


def reverse2(xs):
    """
    :param xs: list
    :return: reversed
    """
    if not xs:
        return
    else:
        return [xs[-1]] + reverse(xs[0:-1])


def palindrome(xs):
    """
    :param xs: string
    :return: boolean
    """

    # clean string
    punctuation = ["!", ":", ".", ",", ";", "?"]
    xs_no_punc = "".join([x for x in xs if x not in punctuation])
    print(xs_no_punc)
    xs_int = xs_no_punc.lower().split()

    # reverse string
    xs_int_rev = xs_int[::-1]
    for i, x in enumerate(xs_int_rev):
        xs_int_rev[i] = x[::-1]

    if "".join(xs_int_rev) == "".join(xs_int):
        return True
    else:
        return False


def normstring(s):
    import string
    result = ''
    for c in s:
        if c in string.ascii_letters:
            result += str.lower(c)
    return result


def palindrom1(xs):
    """
    :param xs: string
    :return: boolean
    """

    # clean string
    punctuation = ["!", ":", ".", ",", ";", "?", " "]
    for punc in punctuation:
        xs = xs.replace(punc, "")

    xs_int = xs.lower()
    xs_int_rev = xs_int[::-1]
    if xs_int == xs_int_rev:
        return True
    else:
        return False


def palindrom2(xs):
    """
    :param xs: string
    :return: boolean (True = palindrom)
    """
    if xs == "":
        raise ValueError

    # cleaning string
    punctuation = ["!", ":", ".", ",", ";", "?", " "]
    for punc in punctuation:
        xs = xs.replace(punc, "")
    xs_int = xs.lower()
    print(xs_int)

    if len(xs_int) == 2:
        if xs_int[0] == xs_int[-1]:
            return True
        else:
            return False

    if xs_int[0] == xs_int[-1]:
        return palindrom2(xs_int[1:-1])
    else:
        return False


def romans():
    """
    :return: romans 1-100
    """
    tens = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']
    hundreds = ['', 'X', 'XX', 'XXX', 'XL', 'L', 'LX', 'LXX', 'LXXX', 'XC', 'C']
    result = []
    for i, h in enumerate(hundreds):
        if i <= 2:
            for t in tens[1::]:
                result.append(h + t)
        elif i >= 3:
            for t in tens[0:-1]:
                result.append(h + t)

    return result


def teile(betrag):
    """
    :param betrag: integer (cent)
    :return: integer mit Anzahl der Geldeinheiten
    """

    if type(betrag) != int:
        raise ValueError

    euros = [20000, 10000, 5000, 2000, 1000, 500, 200, 100, 50, 10, 2, 1]
    betrag_euro = []
    result = []
    for euro in euros:
        x = betrag // euro
        result.append(x)
        betrag_euro.append(x * euro)
        betrag = betrag % euro
    return result, betrag_euro, sum(betrag_euro)


def zeugnisnote(proben, kurzproben, stegreifaufgaben):
    """
    :param proben:
    :param kurzproben:
    :param stegreifaufgaben:
    :return: real note
    """

    sum_proben = sum(proben)
    sum_kurzproben = sum(kurzproben)
    sum_steg = sum(stegreifaufgaben)

    note = (sum_proben + sum_kurzproben + sum_steg) / (len(proben) + len(kurzproben) + len(stegreifaufgaben))

    return note


def pascal_triangle(n):
    """
    :param n: an integer >= 0
    :return: coefficients of (a + b) ** n
    """
    if n < 0:
        raise ValueError
    elif n <= 1:
        return [1] * (n + 1)
    else:
        previous_line = [1, 1]
        for i in range(3, n + 2):
            this_line = [1] * i
            for j in range(len(this_line))[1:-1]:
                this_line[j] = previous_line[j - 1] + previous_line[j]
            previous_line = this_line
        return previous_line


def pascal_triangle1(n):
    """
    :param n: an integer >= 0
    :return: coefficients of (a + b) ** n
    """

    def pas(xs, n):
        from operator import add
        return xs if n == 1 \
            else pas([1] + list(map(add, xs[0:-1], xs[1:])) + [1], n - 1)

    if n < 0:
        raise ValueError
    elif n == 0:
        return [1]
    else:
        return pas([1, 1], n)


if __name__ == '__main__':
    # print(gca2(20, 2))
    # print(gca2(0, 8))
    # print(gca2(8, 20))
    # print(faculty1(1))
    # print(exp_coeff(5, 1))
    # print(exp_coeff1(5, 1))
    # print(reverse([0, 1, 2, 3]))
    # print(palindrom2("Ein Neger mit Gazelle zagt im Regen nie!"))
    # print(palindrom2("Ein Neger mit zagt im Regen nie"))
    # print(romans())
    # print(teile(22222))
    # print(zeugnisnote(proben=[2.0, 3.0, 3.0, 2.0, 1.3],
    #                  kurzproben=[3.3, 2.7, 4.3, 2.3],
    #                  stegreifaufgaben=[4.0, 2.0, 2.3, 5.0, 2.0, 2.3]))

    # print(reverse([1, 2, 3]))
    # print(pascal_triangle(0))
    # # print(pascal_triangle1(1))
    # print(pascal_triangle1(2))
    # print(pascal_triangle1(3))

    for n in range(7):
        print(pascal_triangle1(n))
