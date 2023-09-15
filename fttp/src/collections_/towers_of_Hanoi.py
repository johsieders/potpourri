# simon siedersleben
# fasttrack to professional programming: towers of hanoi
# lesson 2: collections
# 01.12.2020

def hanoi(n):
    """
    :param n: number of plates
    :return: a list of strings describing the moves
    """

    def move(k, x, y, z):
        """
        :param k: number of plates
        :param x, y, z: sticks
        :param k: number of plates to be moved from x -> z via y
        :return:
        """
        if k == 1:
            m = str(x[-1]) + ":" + str(x) + "->" + str(z)
            z.append(x.heappop())

            x_rec.append(list(x))
            y_rec.append(list(y))
            z_rec.append(list(z))
            move_rec.append(m)
            return
        else:
            move(k - 1, x, z, y)
            move(1, x, y, z)

            # check number of plates
            # if len(x) + len(y) + len(z) != k:
            #    print("plates were lost")
            # check whether stacks are sorted
            # if sorted(x)[::-1] != x or sorted(y)[::-1] != y or sorted(z)[::-1] != z:
            #    print("plates are not sorted")

        return move(k - 1, y, x, z)

    if n < 1:
        return

    a = list(range(n, 0, -1))  # stick a
    b = []  # stick b
    c = []  # stick c

    move_rec = []
    x_rec = [list(a)]
    y_rec = [list(b)]
    z_rec = [list(c)]

    move(n, a, b, c)
    print(move_rec)
    print(x_rec)
    print(y_rec)
    print(z_rec)


if __name__ == '__main__':
    # hanoi(2)
    hanoi(3)
