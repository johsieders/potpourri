# from https://docs.fast.ai/tutorial.datablock


# from fastai.data.load import *
# from fastcore.foundation import *
# from fastcore.test_ import *
#
# import string

import unittest


class Sandbox(unittest.TestCase):

    def testDataLoader(self):
        self.assertEqual(1, 1)
        print('hello')

        # ds = L(enumerate(string.ascii_lowercase))
        # dl = DataLoader(ds, batch_size=2, shuffle=False)
        # print(list(dl))
        #
        # test_eq(0, 0)
