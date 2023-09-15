import unittest

import torch
from fastai.data.core import DataLoaders
# from torch.utils.data import DataLoader
from fastai.data.load import DataLoader
from fastai.learner import Learner
from fastai.losses import MSELossFlat
from fastai.metrics import accuracy
from fastai.optimizer import SGD
from torch import float32, tensor, nn


# from fastai.data.load import *
# from fastcore.foundation import *
# from fastcore.test_ import *
# from fastai.text.all import *
# from fastai.tabular.all import *
# from fastai.data.external import *
# from fastai.losses import *


class MyTestCase(unittest.TestCase):
    def test_something(self):
        X = tensor((0, 0, 0, 1, 1, 0, 1, 1), requires_grad=True, dtype=float32).reshape(4, 2)
        Y = tensor((0, 0, 0, 1), dtype=torch.float32).reshape(4, 1)
        F_train = list(zip(X, Y))

        dl = DataLoader(F_train, batch_size=4)
        dls = DataLoaders(dl, dl)

        G = nn.Sequential(nn.Linear(2, 1), nn.Sigmoid())
        learner = Learner(dls, G, opt_func=SGD, loss_func=MSELossFlat(), metrics=accuracy)

        # G = nn.Linear(2, 1)
        # learner = Learner(dls, G, opt_func=SGD, loss_func=BCEWithLogitsLossFlat(), metrics=accuracy)

        learner.fit_one_cycle(1)
        learner.lr_find(end_lr=100)
        learner.recorder.plot()
