## checkInvariants dhwdim
## js 8.5.05

from unittest import makeSuite, TestCase, TextTestRunner

from dwhdim import *

produkt = ['Produkt',  ## name of dimension
           'Sparte     Gruppe      Produkt',  ## levels of dimension

           'Food       Obst        Apfel',  ## list of elements by levels
           '                       Birne',
           '           Gemuese     Kohl',
           '                       Lauch',
           'Non-Food   Werkzeug    Hammer',
           '                       Bohrer']


class TestProdukt(TestCase):
    def testSlices(self):
        self.sd = DWHSimpleDimension(produkt)
        self.sd.getSlice()
        self.sd.getSlice('Food')
        self.sd.getSlice('Food', 'Obst')
        self.sd.getSlice('Food', 'Obst', 'Apfel')
        self.sd.getSlice('Food', 'Gemuese', 'Kohl')
        self.sd.getSlice('Non-Food')
        self.sd.getSlice('Non-Food', 'Werkzeug', 'Hammer')
        self.sd.getSlice('Non-Food', 'Werkzeug')


def suite():
    return makeSuite(TestOne)


if __name__ == '__main__':
    runner = TextTestRunner()
    runner.run(suite())
