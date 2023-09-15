# s.siedersleben
# fasttrack to professional programming
# random question found in the internet
# 16.12.2020

def max_profit(xs):
    '''
    :param xs:
    :return:
    '''
    max_diff = 0
    buy = 0
    sell = 0
    for i, x in enumerate(xs):
        for j in xs[i::]:
            if x - j < max_diff:
                max_diff = x - j
                buy = x
                sell = j
    return (max_diff, buy, sell)


def max_profit1(stock_price):
    '''
    :param xs:
    :return:
    '''
    max_diff = 0
    hist = []
    for current_p in stock_price:
        hist.append(current_p)
        max_diff = min(max_diff, min(hist) - current_p)
    return max_diff


if __name__ == "__main__":
    print(max_profit(xs=[10, 7, 8, 9]))
    print(max_profit(xs=[1, 2, 3, 4, 5]))
    print(max_profit(xs=[5, 4, 3, 1]))
    print(max_profit1([10, 7, 8, 9]))
    print(max_profit1([1, 2, 3, 4, 5]))
    print(max_profit1([5, 4, 3, 1]))
