# https://docs.fast.ai/tutorial.text

from fastai.text.all import *
from fastcore import *

if __name__ == '__main__':
    xs = []

    test_eq(1, 2)

    xs = L.range(1, 2, 3).shuffle()

    path = untar_data(URLs.IMDB)
    path.ls()

    (path / 'train').ls()

    dls = TextDataLoaders.from_folder(untar_data(URLs.IMDB), valid='test_')

    dls.show_batch()

    learn = text_classifier_learner(dls, AWD_LSTM, drop_mult=0.5, metrics=accuracy)

    learn.fine_tune(4, 1e-2)
    learn.fine_tune(4, 1e-2)
    learn.show_results()

    learn.predict("I really liked that movie!")
