import numpy as np
from numpy.testing import assert_equal, assert_array_equal

from pygesture import pipeline

np.random.seed(12345)

rand_data_1d = np.random.rand(100, 1)
rand_data_2d = np.random.rand(100, 5)

class TestConditioner(object):

    def test_1d(self):
        data = rand_data_1d
        conditioner = pipeline.Conditioner(3, (10, 450), 1000)
        out = conditioner.process(data)

        assert_array_equal(data.shape, out.shape)

    def test_2d_nodownsample(self):
        data = rand_data_2d
        conditioner = pipeline.Conditioner(3, (10, 450), 1000)
        out = conditioner.process(data)

        assert_array_equal(data.shape, out.shape)

    def test_2d_downsample(self):
        data = rand_data_2d
        conditioner = pipeline.Conditioner(3, (10, 450), 1000, 500)
        out = conditioner.process(data)

        assert_equal(int(data.shape[0]/2), out.shape[0])

class TestWindower(object):

    def test_no_overlap(self):
        data = rand_data_2d
        windower = pipeline.Windower(10, 0)

        for i in range(data.shape[0]//10):
            new_data = windower.process(data[i*10:(i+1)*10, :])

        assert_array_equal(new_data, data[-10:, :])

    def test_overlap(self):
        data = rand_data_2d
        windower = pipeline.Windower(13, 3)

        for i in range(data.shape[0]//10):
            new_data = windower.process(data[i*10:(i+1)*10, :])

        assert_array_equal(new_data, data[-13:, :])
