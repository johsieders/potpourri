## checkInvariants Z over p
## js 12.08.2004

from unittest import makeSuite, TestCase, TextTestRunner


class TestFp(TestCase):
    def testAri(self):
        F7 = makeFp(7)
        a = F7(5)
        b = F7(6)

        self.assertEqual(4, a + 6)
        self.assertEqual(4, 6 + a)
        self.assertEqual(4, a + b)

        self.assertEqual(6, a - 6)
        self.assertEqual(1, 6 - a)
        self.assertEqual(6, a - b)

        self.assertEqual(2, a * 6)
        self.assertEqual(2, 6 * a)
        self.assertEqual(2, a * b)

        self.assertEqual(2, a / 6)
        self.assertEqual(4, 6 / a)
        self.assertEqual(2, a / b)

        self.assertEqual(1, a ** 0)
        self.assertEqual(5, a ** 1)
        self.assertEqual(4, a ** 2)


def suite():
    return makeSuite(TestFp)


if __name__ == '__main__':
    runner = TextTestRunner()
    runner.run(suite())
