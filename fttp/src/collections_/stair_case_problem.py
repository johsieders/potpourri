# s.siedersleben
# fasttrack to professional programming
# lesson 2: collections
# 10.12.2020

def stair_case(n):
    """
    :param n: number of stairs
    :return: number of possibilities under the assumption that you can only take 1 or 2 steps once a time
    """
    if n < 0:
        raise ValueError

    if n == 0:
        return 1
    elif n == 1:
        return 1
    else:
        return stair_case(n - 1) + stair_case(n - 2)


if __name__ == '__main__':
    pos = stair_case(4, 1)
    print(pos)
