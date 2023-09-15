import unittest

from collections_.collections1 import cross_sum0, cross_sum1, cross_sum2, is_sorted0, is_sorted1, \
    makeIndex, merge2, makeDict


class collection1Test(unittest.TestCase):
    def test_cross_sum0(self):
        self.assertEqual(cross_sum0(0), 0)
        self.assertEqual(cross_sum0(12), 3)
        self.assertEqual(cross_sum0(12.2), 5)

    def test_cross_sum1(self):
        self.assertEqual(cross_sum1(0), 0)
        self.assertEqual(cross_sum1(2), 2)
        self.assertEqual(cross_sum1(12), 3)

    def test_cross_sum2(self):
        self.assertEqual(cross_sum2(0), 0)
        self.assertEqual(cross_sum2(2.2), 4)

    def test_sorted0(self):
        self.assertEqual(is_sorted0([]), True)
        self.assertEqual(is_sorted0([1]), True)
        self.assertEqual(is_sorted0([1, 2, 3]), True)
        self.assertEqual(is_sorted0([1, 3, 2]), False)

    def test_sorted1(self):
        self.assertEqual(is_sorted1([]), True)
        self.assertEqual(is_sorted1([1]), True)
        self.assertEqual(is_sorted1([1, 2, 3]), True)
        self.assertEqual(is_sorted1([1, 3, 2]), False)

    def test_makeIndex(self):
        contacts = [("Hans", 1234), ("Peter", 4321), ("Fritz", 2134)]
        expected_result = {1234: [0], 4321: [1], 2134: [2]}
        self.assertEquals(makeIndex({}, lambda contact: contact[1]), {})
        self.assertEquals(makeIndex(contacts, lambda contact: contact[1]), expected_result)

    def test_merge2(selfs):
        xs = [1, 2, 3]
        ys = [3, 4]
        selfs.assertEqual(merge2(xs, ys), [1, 2, 3, 3, 4])

    def testHash(self):
        g, s = makeDict()

        caught = False
        try:
            g(1)
        except ValueError:
            caught = True
        self.assertTrue(caught)

        n = 1000

        for i in range(n):
            s(i, str(5 * i))

        for i in range(n):
            s(i, str(10 * i))

        for i in range(n):
            self.assertEqual(str(10 * i), g(i))


if __name__ == '__main__':
    unittest.main()
