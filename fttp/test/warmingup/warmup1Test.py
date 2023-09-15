import unittest

from warmingup.warmup1 import pascal_triangle, pascal_triangle1


class TestWarmUp1(unittest.TestCase):
    def test_pascal_triangle(self):
        # self.assertRaises(pascal_triangle(-1), ValueError)
        self.assertEqual(pascal_triangle(0), [1])
        self.assertEqual(pascal_triangle(1), [1, 1])
        self.assertEqual(pascal_triangle(2), [1, 2, 1])
        self.assertEqual(pascal_triangle(3), [1, 3, 3, 1])

    def test_pascal_triangle1(self):
        # self.assertRaises(pascal_triangle(-1), ValueError)
        self.assertEqual(pascal_triangle1(0), [1])
        self.assertEqual(pascal_triangle1(1), [1, 1])
        self.assertEqual(pascal_triangle1(2), [1, 2, 1])
        self.assertEqual(pascal_triangle(3), [1, 3, 3, 1])


if __name__ == '__main__':
    unittest.main()
