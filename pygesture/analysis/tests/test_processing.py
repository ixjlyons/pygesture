import numpy as np

from pygesture.analysis import processing


class TestWindow(object):

    def setUp(self):
        self.data1dcol = np.array([[1], [2], [3], [4], [5], [6], [7], [8]])
        self.data2dcol = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
        self.data2drow = np.array([[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12]])

    def test_1d_nooverlap(self):
        for win in processing.window(self.data1dcol, 2):
            assert win.shape == (2, 1)

    def test_uneven(self):
        for win in processing.window(self.data1dcol, 5):
            print(win.shape)
            assert win.shape == (5, 1)

    def test_2d_nooverlap(self):
        for win in processing.window(self.data2dcol, 2):
            assert win.shape == (2, self.data2dcol.shape[1])

    def test_2d_nooverlap_axis1(self):
        for win in processing.window(self.data2drow, 3, axis=1):
            print(win.shape)
            assert win.shape == (2, 3)

    def test_1d_overlap(self):
        for i, win in enumerate(
                processing.window(self.data1dcol, 2, overlap=1)):
            if i > 0:
                assert prev[-1] == win[0]
            prev = win

    def test_zero_vec(self):
        for i in processing.window(np.array([]), 2):
            pass

