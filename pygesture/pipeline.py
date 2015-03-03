from scipy import signal
import numpy as np


class Pipeline(object):
    def __init__(self, block_list):
        self.block_list = block_list

    def process(self, data):
        out = data
        for block in self.block_list:
            out = block.process(out) 

        return out


class PipelineBlock(object):
    """
    A generic processing block in the pipeline.
    
    The pipeline is implemented as
    a tree structure, which is completely determined by this class,
    representing a node in the tree. This base class takes care of propogating
    its processed data to its children, so subclasses just need to implement
    the `process()` method, which should take in data and return data. They
    *should* also implement `__repr__`, as this is useful for generating
    visualizations of the pipeline.
    """

    def __init__(self):
        self.children = []
        self.hooks = []

    def add_child(self, node):
        self.children.append(node)

    def add_hook(self, hook):
        self.hooks.append(hook)

    def process(self, data):
        out = data  # usually some function
        self.propogate(out)

    def propogate(self, data):
        for hook in self.hooks:
            hook(data)

        for child in self.children:
            child.process(data)

    def __repr__(self):
        return "%s.%s()" % (
            self.__class__.__module__,
            self.__class__.__name__
        )


class Conditioner(PipelineBlock):
    """
    A data conditioner which performs three operations on the input:
        1. DC bias removal
        2. bandpass filtering
        3. downsampling

    The bias removal is done by subtracting the mean from the signal, as this
    block is assumed to operate on batch data. The bandpass filter is
    implemented as a Butterworth filter with order and cutoff frequencies
    specified, and the downsampling

    Parameters
    ----------
    n : int
        Filter order.
    fc : tuple or list of ints (len=2) 
        Cutoff frequencies for the filter, specified in Hz.
    fs : int
        Signal sampling rate.
    fd : int, default=None
        Downsampled signal sample rate. Must evenly divide into fs. If not
        specified, the sampling rate is unchanged.
    """

    def __init__(self, order, f_cut, f_samp, f_down=None):
        super(Conditioner, self).__init__()
        self.n = order
        self.fc = f_cut 
        self.fs = f_samp 

        if f_down is None:
            f_down = self.fs

        self.m = int(self.fs/f_down)

        self._build_filter()
        self.zi = None

    def _build_filter(self):
        wc = [f / (self.fs/2.0) for f in self.fc]
        self.b, self.a = signal.butter(self.n, wc, 'bandpass')

    def process(self, data):
        if self.zi is None:
            zi = signal.lfilter_zi(self.b, self.a)
            self.zi = np.tile(zi, (data.shape[1], 1)).T

        data_centered = data - np.mean(data, axis=0)
        data_filtered, self.zi = signal.lfilter(
            self.b, self.a, data_centered, axis=0, zi=self.zi)
        data_downsampled = data_filtered[::self.m, :]
        return data_downsampled

    def __repr__(self):
        return "%s.%s(n=%s, fc=%s, fs=%s, m=%s)" % (
            self.__class__.__module__,
            self.__class__.__name__,
            self.n,
            self.fc,
            self.fs
        )


class Classifier(PipelineBlock):

    def __init__(self, clf):
        super(Classifier, self).__init__()
        self.clf = clf

    def fit(self, data):
        self.clf.fit(data)

    def process(self, data):
        return self.clf.predict(data)
