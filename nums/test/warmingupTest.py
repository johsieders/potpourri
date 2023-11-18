# testing warmingup
# 13/11/2020

import unittest

from nums.src.warmingup import *


class WarmingupTest(unittest.TestCase):
    def testPower2(self):
        for n in [2 ** k for k in range(2, 100)]:
            self.assertFalse(powerOf2(n - 1))
            self.assertTrue(powerOf2(n))
            self.assertFalse(powerOf2(n + 1))

    def testLog2(self):
        for n in range(1, 10):
            print(n, log2(n))

    def testFibo(self):
        f = fibo(3)
        self.assertEqual(2, f)

    def testReverse0(self):
        xss = [[], [0], [0, 1], [0, 1, 2], [0, 1, 2, 3]]
        for xs in xss:
            ys = reverse0(xs)
            zs = reverse0(ys)
            self.assertListEqual(xs, zs)

    def testReverse1(self):
        xss = [[], [0], [0, 1], [0, 1, 2], [0, 1, 2, 3]]
        for xs in xss:
            ys = list(xs)
            reverse1(xs)
            reverse1(xs)
            self.assertListEqual(xs, ys)

    def auxPalindrome(self, isPalindrome):
        b = isPalindrome("")
        self.assertTrue(b)
        b = isPalindrome("x")
        self.assertTrue(b)
        b = isPalindrome("xx")
        self.assertTrue(b)
        b = isPalindrome("xy")
        self.assertFalse(b)

        s = "Reittier"
        b = isPalindrome(s)
        self.assertTrue(b)

        s = "Reliefpfeiler"
        b = isPalindrome(s)
        self.assertTrue(b)

        s = "Ein Neger mit Gazelle zagt im Regen nie"
        b = isPalindrome(s)
        self.assertTrue(b)

        s = "Madam, I'm Adam"
        b = isPalindrome(s)
        self.assertTrue(b)

        s = "Risotto, Sir?"
        b = isPalindrome(s)
        self.assertTrue(b)

        s = "Eine treue Familie bei Lima feuerte nie"
        b = isPalindrome(s)
        self.assertTrue(b)

        s = "Liese, tu Gutes, eil!"
        b = isPalindrome(s)
        self.assertTrue(b)

        s = "O Genie, der Herr ehre dein Ego!"
        b = isPalindrome(s)
        self.assertTrue(b)

        s = "Grub Nero nie in Orenburg?"
        b = isPalindrome(s)
        self.assertTrue(b)

        s = "Mad Zeus, no live devil, lived evil on Suez dam"
        b = isPalindrome(s)
        self.assertTrue(b)

        s = "Straw? No, too stupid a fad. I put soot on warts."
        b = isPalindrome(s)
        self.assertTrue(b)

        s = "Lewd I did live, & evil did I dwel?"
        b = isPalindrome(s)
        self.assertTrue(b)

    def testPalindrome(self):
        for p in [palindrome1, palindrome, palindrome2]:
            self.auxPalindrome(p)

    def testRomans(self):
        romanNumbers = romans()
        self.assertEqual('', romanNumbers[0])
        self.assertEqual('I', romanNumbers[1])
        self.assertEqual('II', romanNumbers[2])
        self.assertEqual('V', romanNumbers[5])
        self.assertEqual('MMMMCMXCIX', romanNumbers[4999])

    def testTeileBetrag(self):
        for betrag in [10000, 30000, 50005]:
            result, sum = teile(betrag)
            self.assertEqual(betrag, sum)

    def testZeugnisnoten(self):
        proben = [[], [2]]
        kurzproben = [[], [2]]
        stegreifaufgaben = [[1], [2]]
        ergebnis = [1., 2.]

        for i in range(len(proben)):
            gesamtnote = zeugnisnote(proben[i],
                                     kurzproben[i],
                                     stegreifaufgaben[i])
            self.assertAlmostEqual(gesamtnote, ergebnis[i])

    def testPascal(self):
        for n in range(7):
            print(pascal(n))
