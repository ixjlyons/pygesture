import numpy as np
from numpy.testing import assert_equal, assert_array_equal

from pygesture import pipeline

np.random.seed(12345)

rand_data_1d = np.random.rand(100, 1)
rand_data_2d = np.random.rand(100, 5)


class _AddOneBlock(pipeline.PipelineBlock):

    def process(self, data):
        return data + 1


class _TwoInputBlock(pipeline.PipelineBlock):

    def process(self, data):
        print(data)
        x, y = data
        return x + y


class TestPipeline(object):

    def setUp(self):
        self.data = 10
        self.a = _AddOneBlock()
        self.b = _AddOneBlock()

    def test_series_simple(self):
        p = pipeline.Pipeline([self.a, self.b])
        out = p.process(self.data)
        assert out == self.data + 2

    def test_parallel_simple(self):
        p = pipeline.Pipeline((self.a, self.b))
        out = p.process(self.data)
        assert out == [self.data+1, self.data+1]

    def test_series_to_parallel(self):
        c = _AddOneBlock()
        p = pipeline.Pipeline([self.a, (self.b, c)])
        out = p.process(self.data)
        assert out == [self.data+2, self.data+2]

    def test_parallel_to_series(self):
        c = _TwoInputBlock()
        p = pipeline.Pipeline([(self.a, self.b), c])
        out = p.process(self.data)
        assert out == self.data+1 + self.data+1

    def test_complex(self):
        c = _AddOneBlock()
        d = _AddOneBlock()
        e = _TwoInputBlock()
        p = pipeline.Pipeline([self.a, (self.b, [c, d]), e])
        out = p.process(self.data)
        assert out == self.data+2 + self.data+3


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
