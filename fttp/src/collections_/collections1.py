def histogram0(xs):
    """
    :param xs: any list
    :return: dictionary key; elements of xs value = num of occurances of each x in xs
    """

    result = {}

    for x in set(xs):
        result[x] = xs.count(x)

    return result


def histogram1(xs):
    """
    :param xs: any list
    :return: dictionary key; elements of xs value = num of occurances of each x in xs
    """

    result = {}

    for x in xs:
        if x not in result:
            result[x] = 1
        else:
            result[x] += 1

    return result


def indexA(book):
    """
    :param book: dictionary of pages each page containing the items to be indexed
    :return: dictionary key: words occuring in book; value: list of page numbers featuring word
    """

    result = {}

    for i, page in book.items():
        for word in page:
            if word not in result:
                result[word] = [i]
            else:
                result[word].append(i)

    return result


def normnumber(s):
    """
    :param s: a string
    :return: keeps ascii letters only and converts s to lower case
    """
    import string
    result = ''
    for c in s:
        if c in string.digits:
            result += str.lower(c)
    return result


def cross_sum0(x):
    """
    :param x: any float
    :return: cross sum of x treating the decimals like normal numbers
    """
    xs = str(x)
    xs_norm = normnumber(xs)
    result = 0
    for c in xs_norm:
        result += int(c)
    return result


def cross_sum1(x):
    """
    :param x: any positive integer
    :return: cross sum of positive integer
    << perfekt >>
    """
    return x if x < 10 \
        else x % 10 + cross_sum1(x // 10)


def cross_sum2(x):
    """
    :param x: any positive float
    :return: cross sum of x
    """
    while x % 1 != 0:
        x = x * 10

    def int_cross_sum(x_inner):
        return x_inner if x_inner < 10 \
            else x_inner % 10 + cross_sum1(x_inner // 10)

    return int_cross_sum(x)


def is_sorted0(xs):
    """
    :param xs: list with floats and/or integers
    :return: True if xs is sorted, false otherwise
    << perfekt >>
    """
    if len(xs) <= 1:
        return True

    for i, x in enumerate(xs[0:-1]):
        if xs[i] > xs[i + 1]:
            return False
    return True


def is_sorted1(xs):
    """
    :param xs: list with floats and/or integers
    :return: True if xs is sorted, false otherwise
    << perfekt >>
    """
    if len(xs) <= 1:
        return True

    return False if xs[0] > xs[1] else is_sorted1(xs[1:])


def makePhoneIndex(contacts):
    """
    :param contacts: list with tuples
    :return: dictionary result; index phone numbers; values: corresponding list indexes
    """
    index = {}

    for i, contact in enumerate(contacts):
        if contact[1] not in index:
            index[contact[1]] = [i]
        else:
            index[contact[1]].append(i)

    return index


def makeIndex(table, func):
    """
    :param table: a list containing tuples
    :param func: a hash function
    :return: index based on the  hash function func
    """
    index = {}

    for i, row in enumerate(table):
        key = func(row)
        if key not in index:
            index[key] = [i]
        else:
            index[key].append(i)

    return index


def func_phone(contact):
    """
    :param contact: tuple
    :return: second entry of tuple
    """
    return contact[1]


def merge1(xs, ys):
    """
    :param xs: list with integers of length n, sorted, smallest int first
    :param ys: list with integers of length n, sorted smallest int first
    :return: a new sorted list including all elements of xs and ys
    """
    result = []

    x = xs.heappop(0) if xs else None
    y = ys.heappop(0) if ys else None

    while x and y:
        if x <= y:
            result.append(x)
            x = xs.heappop(0) if xs else None
        else:
            result.append(y)
            y = ys.heappop(0) if ys else None

    if x:
        result.append(x)
    if y:
        result.append(y)

    if xs:
        result += xs
    if ys:
        result += ys

    return result


def merge2(xs, ys):
    """
    :param xs: list with integers of length n, sorted, smallest int first
    :param ys: list with integers of length n, sorted smallest int first
    :return: a new sorted list including all elements of xs and ys
    comment: this is the recursive solution
    """
    if not xs:
        return ys
    elif not ys:
        return xs
    else:
        if xs[0] <= ys[0]:
            return [xs[0]] + merge2(xs[1::], ys)
        else:
            return [ys[0]] + merge2(xs, ys[1::])


###############################
## self-made hash dictionary ##
###############################

def makeDict():
    """
    :return: two functions get_key(key), set_key(key, value):
    - get_key(key): returns the value of a key
        get_key(key) works in the following manner:
            1. check whether the hash_value of key already exists in a list of slots [(hash_value, slot)]
            2. if key exist, keep looking for the value in the corresponding list slot = [(key, value)]
    - set_key(key, value): sets the value of a key
        set_key(key, value) works in the following manner
            1. check whether the hash_value of the given string exist
            2. if not create a new entry in slots
            3. if yes, append a new entry in the corresponding slot
    """
    slots = []

    def get(key):
        h0 = hash(key)
        for slot in slots:
            if slot[0] == h0:
                for s in slot[1]:
                    if key == s[0]:
                        return s[1]
        raise ValueError

    def set(key, value):
        h0 = hash(key)
        exist = False
        for slot in slots:
            if slot[0] == h0:
                slot[1].append((key, value))
                exist = True
        if not exist:
            slots.append((h0, [(key, value)]))

        return

    return get, set


if __name__ == '__main__':
    g, s = makeDict()
    # g(1)
    s(2, "3")
    print(g(2))
