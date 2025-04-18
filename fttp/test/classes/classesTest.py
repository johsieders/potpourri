# testing classes_
# 20/11/2020
# This exercise shows three ways how to make
# static data and methods available


import unittest

from classes_.romans import *
# from sorting.sorting2 import *


class classesTest(unittest.TestCase):

    def testRomans(self):
        tofrom = (Roman.toRoman, Roman.fromRoman), \
            (RomanFunc.toRoman, RomanFunc.fromRoman), \
            (toRoman1, fromRoman1)

        for toRoman, fromRoman in tofrom:
            self.assertEqual('I', toRoman(1))
            self.assertEqual('CI', toRoman(101))

            self.assertEqual(1, fromRoman('I'))
            self.assertEqual(100, fromRoman('C'))



class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

