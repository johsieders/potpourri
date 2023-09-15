# j.siedersleben
# fasttrack to professional programming
# lesson 2: collections
# 17.11.2020

# Anmerkung: collections gibt es schon irgendwo, daher collections_

from warmingup.warmingup2 import romans


def merge(xs, ys: list):
    """
    :param xs: a non descending list
    :param ys: a non descending list
    :return: merge of xs and ys
    Standard solution. A bit tricky.
    """
    result = []
    # invariants:
    # x, y first elements of xs, ys, None if there is no first element
    x = xs.pop(0) if xs else None
    y = ys.pop(0) if ys else None

    while x and y:  # same as x is not None and y is not None
        if x <= y:  # get next element of xs for next loop
            result.append(x)
            x = xs.pop(0) if xs else None
        else:  # get next element of ys for next loop
            result.append(y)
            y = ys.pop(0) if ys else None

    # x or y may be left behind (but not both)
    if x:
        result.append(x)
    if y:
        result.append(y)

    # one of the remaining xs, ys is empty
    # the one which is not (if any) is appended to result
    if xs:  # same as len(xs) > 0
        result += xs
    if ys:
        result += ys

    return result


def merge1(xs, ys: list):
    """
    :param xs: a non descending list
    :param ys: a non descending list
    :return: merge of xs and ys
    elegant but slow
    This the definition of merge, and it happens to run!
    """
    if not xs:
        return list(ys)
    elif not ys:
        return list(xs)
    elif xs[0] <= ys[0]:
        return xs[:1] + merge1(xs[1:], ys)
    else:
        return ys[:1] + merge1(xs, ys[1:])


def checksum(n):
    """
    :param n: an integer
    :return: checksum of n
    """
    result = 0

    while n != 0:
        n, r = divmod(n, 10)
        result += r

    return result


def histogram0(xs):
    """
    :param xs: a list
    :return: histogram0 of xs: a map indicating how often each x occurs in xs
    """
    result = {}
    for x in xs:
        if x not in result.keys():
            result[x] = 1
        else:
            result[x] += 1
    return result


def histogram1(xs):
    """
    :param xs: a list
    :return: histogram0 of xs: a map indicating how often each x occurs in xs
    """
    result = {}
    for x in xs:
        if x not in result.keys():
            result[x] = xs.count(x)
    return result


def histogram2(xs):
    """
    :param xs: a list
    :return: histogram0 of xs: a map indicating how often each x occurs in xs
    """
    return dict([(x, xs.count(x)) for x in xs])


def histogram3(xs):
    """
    :param xs: a list
    :return: histogram0 of xs: a map indicating how often each x occurs in xs
    """
    return dict([(x, xs.count(x)) for x in set(xs)])


#############################
##      Roman Numbers      ##
#############################

def romanTrafos():
    """
    :return: functions toRoman, fromRoman
    toRomanList and fromRomanMap are computed once.
    They are contained in the closure of toRoman and fromRoman
    """
    toRomanList = romans()
    fromRomanMap = dict((toRomanList[n], n) for n in range(5000))

    def toRoman(n):
        return toRomanList[n]

    def fromRoman(r):
        return fromRomanMap[r]

    return toRoman, fromRoman


#######################
##      index A      ##
#######################

def indexA(book):
    """
    book[i]      = list of indexable words on page i
    result[word] = list of pages containing word
    """
    result = {}
    for i, page in enumerate(book):
        for word in set(page):
            if word not in result.keys():
                result[word] = []
            result[word].append(i)
    return result


#######################
##      index B      ##
#######################

def indexB1(book, keywords):
    """
    book[i]  = set of all words on page i
    keywords = set of all indexable words
    result[word] = list of pages containing word
    standard solution
    """
    result = {}
    for i, page in enumerate(book):
        for word in set(page) & set(keywords):
            if word not in result.keys():
                result[word] = []
            result[word].append(i)
    return result


def indexB2(book, keywords):
    """
    book[i]  = set of all words on page i
    keywords = set of all indexable words
    result[word] = list of pages containing word
    elegant but slower
    idea: replace each page with the intersection of page and keywords
    """
    book = [set(page) & set(keywords) for page in book]
    return indexB1(book, keywords)


#############################
##      search index       ##
#############################

def makeIndex(rows, v):
    """
    :param rows: list of rows; each row being a tuple of fields or whatever
    :param v: row -> value (value to be indexed)
    :return: a dictionary; key = field, value = IDs of rows with v(row) = value
    """
    index = {}

    for i, row in enumerate(rows):
        value = v(row)
        if value not in index.keys():
            index[value] = []
        index[value].append(i)

    return index


def makeIndices(rows, vs):
    """
    :param rows: list of rows; each row being a tuple of fields or whatever
    :param vs: functions v: row -> value (value to be indexed)
    :return: a list of dictionaries; key = field, value = IDs of rows with v(row) = value
    """
    indices = []
    for _ in range(len(vs)):
        indices.append({})

    for i, row in enumerate(rows):
        for j, v in enumerate(vs):
            value = v(row)
            if value not in indices[j].keys():
                indices[j][value] = []
            indices[j][value].append(i)

    return indices


def isDescending(xs):
    return True if len(xs) <= 1 \
        else xs[0] > xs[1] and isDescending(xs[1:])


###############################
##      Towers of Hanoi      ##
###############################


def hanoi_naked(n: int) -> None:
    """
    Towers of Hanoi. Exponential time (n = 22 -> 12s)
    :param n: number of disks on first tower > 0
    :return: None
    There is nothing left to remove
    """

    a, b, c = list(range(n, 0, -1)), [], []

    def move(k, x, y, z):
        """
        This function moves k disks from stack x to stack z
        using y as clipboard
        :param k: number of disks to be moved
        :param x: from stack
        :param y: clipboard
        :param z: to stack
        :return: None
        """
        if k == 1:
            z.append(x.heappop())
        else:
            move(k - 1, x, z, y)
            move(1, x, y, z)
            move(k - 1, y, x, z)

    move(n, a, b, c)


def hanoi(n):
    """
    Towers of Hanoi. Exponential time (n = 22 -> 12s)
    :param n: number of disks on first tower > 0
    :return: protocol of all moves
    This is hanoi_naked with protocol
    """

    # checking a precondition
    if n < 1:
        raise ValueError

    a, b, c = list(range(n, 0, -1)), [], []
    protocol = [(list(a), list(b), list(c))]

    def move(k, x, y, z):
        if k == 1:
            z.append(x.pop())
            protocol.append((list(a), list(b), list(c)))
        else:
            move(k - 1, x, z, y)
            move(1, x, y, z)
            move(k - 1, y, x, z)

    move(n, a, b, c)
    return protocol
