import unittest

from functions.functions1 import anagram0, anagram1, power0, compose, curry


class function1Test(unittest.TestCase):
    def test_anagram(self):
        xs = ['otto', 'anna', 'ttoo', 'oott', 'nnaa']
        xs_out = ['anna', 'nnaa', 'otto', 'ttoo', 'oott']
        xs_out1 = ['otto', 'ttoo', 'oott', 'nnaa', 'anna']
        self.assertEqual(anagram0(xs), xs_out)
        self.assertEqual(anagram1(xs), xs_out)

    def test_power0(self):
        self.assertEqual(power0(0, 0), 1)
        self.assertEqual(power0(0, 2), 0)
        self.assertEqual(power0(1, 1), 1)
        self.assertEqual(power0(2, 1), 2)
        self.assertEqual(power0(2, 2), 4)

    def test_compose(self):
        def my_add(x):
            return x + 1

        def my_minus(x):
            return x - 1

        t = compose(my_add, my_minus)
        self.assertEqual(t(1), 1)

    def test_curry(self):
        def my_add(x, y):
            return x + y

        t = curry(my_add, 1)
        self.assertEqual(t(1), 2)


if __name__ == '__main__':
    unittest.main()
