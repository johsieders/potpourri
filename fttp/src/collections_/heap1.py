# s. siedersleben
# fasttrack to professional programming
# lesson 5: sorting
# 29.12.2020

class Myheap(object):
    def __init__(self):
        self.h = []

    def __str__(self):
        return str(self.h)

    def __len__(self):
        return len(self.h)

    def myheappush(self, new_element):
        """
        :param new_element: integer, float that is added to the heap
        :return: a heap containing the new element at the correct location within the heap
        """
        child = len(self.h)
        self.h.append(new_element)
        parent_index = (child - 1) // 2
        if parent_index == child:
            return
        while not self.h[parent_index] <= self.h[child]:
            self.h[parent_index], self.h[child] = self.h[child], self.h[parent_index]
            parent_index, child = (parent_index - 1) // 2, parent_index
            if child <= 0:  # in case the top of the heap is reached, there is nothing else to do
                break

    @staticmethod
    def argmin(h, index):
        return min([2 * index + 1, 2 * index + 2], key=lambda i: h[i])

    def myheappop(self):
        n = len(self.h)
        if n == 0:
            raise IndexError
        elif n <= 2:
            return_value = self.h.pop(0)
            return return_value
        elif n == 3:
            return_value = self.h.pop(0)
            self.h = [min(self.h), max(self.h)]
            return return_value
        else:
            return_value = self.h.pop(0)
            self.h = [self.h[-1]] + self.h[:-1]
            parent_index = 0
            while not (self.h[parent_index] <= self.h[2 * parent_index + 1] and
                       self.h[parent_index] <= self.h[2 * parent_index + 2]):
                index_smallest_son = Myheap.argmin(self.h, parent_index)
                self.h[parent_index], self.h[index_smallest_son] = self.h[index_smallest_son], self.h[parent_index]
                parent_index = index_smallest_son

                if 2 * parent_index + 1 not in range(len(self)):  # in case parent index has no further branch -> exit
                    break
                if 2 * parent_index + 2 not in range(len(self)):  # in case parent_index has only one branch
                    self.h[parent_index], self.h[2 * parent_index + 1] = \
                        max(self.h[2 * parent_index + 1], self.h[parent_index]), \
                            min(self.h[2 * parent_index + 1], self.h[parent_index])
                    break
            return return_value


if __name__ == '__main__':
    m = Myheap()
    xs = [21, 1, 8, 10, 50, 2]
    # xs = [4, 3, 2, 10, 11, 15]
    # xs = [4, 3, 2, 1]
    for x in xs:
        m.myheappush(x)
        print(m)
    print(m.myheappop())

    for _ in range(len(m)):
        print(m.myheappop())

    #  print([m.myheappop() for _ in range(len(m))])
