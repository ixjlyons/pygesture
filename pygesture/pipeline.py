from scipy import signal
import numpy as np


class Pipeline(object):
    """
    Container for processing a set of PipelineBlock objects arranged in a
    block diagram structure.

    To create a pipeline, the following two rules are needed: a list of blocks
    are processed in series, and a tuple of blocks are processed in parallel.

    For example, the following feeds incoming data first to block `a`, and the
    output of block `a` is passed to both blocks `b` and `c`. The output of
    blocks `b` and `c` are then both passed to block `d`.

    >>> from pygesture import pipeline
    >>> a = pipeline.PipelineBlock()
    >>> b = pipeline.PipelineBlock()
    >>> c = pipeline.PipelineBlock()
    >>> d = pipeline.PipelineBlock()
    >>> p = pipeline.Pipeline([a, (b, c), d])

    Blocks that are arranged to take multiple inputs (such as block `d` in the
    above example) should expect to take the corresponding number of inputs in
    the order they are given. It is up to the user to make sure that the
    arrangement of blocks makes sense.

    Parameters
    ----------
    blocks : nested lists/tuples of objects derived from PiplineBlock
        The blocks in the pipline, with lists processed in series and tuples
        processed in parallel.
    """

    def __init__(self, blocks):
        self.blocks = blocks

    def add_block(self, block):
        """
        Adds a block to the end of the pipeline in series.
        """
        self.blocks.append(block)

    def process(self, data):
        out = _process_block(self.blocks, data)
        return out


def _process_block(block, data):
    if type(block) is list:
        out = _process_list(block, data)
    elif type(block) is tuple:
        out = _process_tuple(block, data)
    else:
        out = block.process(data)

    return out


def _process_list(block, data):
    out = data
    for b in block:
        out = _process_block(b, out)

    return out


def _process_tuple(block, data):
    out = []
    for b in block:
        out.append(_process_block(b, data))

    return out


class PipelineBlock(object):
    """
    A generic processing block in the pipeline.

    The pipeline is implemented as a network of series and parallel blocks. Any
    extension of this class just needs to implement the `process` method, which
    takes a single argument (data). It is up to the designer of the pipeline to
    ensure compatibility between simple series connections and convergent
    connections (i.e. output of multiple blocks converges to a single block).
    In any case, the documentation for a `PiplineBlock` implementation should
    very clearly state what the expected input and output should be.
    """

    def process(self, data):
        out = data  # usually some function
        return out

    def __repr__(self):
        return "%s.%s()" % (
            self.__class__.__module__,
            self.__class__.__name__
        )


class Windower(PipelineBlock):
    """
    Takes new input data and combines with past data to maintain a sliding
    window with overlap. It is assumed that the input to this block has length
    (length-overlap).

    Parameters
    ----------
    length : int
        Total number of samples to output on each iteration.
    overlap : int, default=0
        Number of samples from previous input to keep in the current window.
    """

    def __init__(self, length, overlap=0):
        super(Windower, self).__init__()
        self.length = length
        self.overlap = overlap

        self._out = None

    def process(self, data):
        if self._out is None:
            self._preallocate(data.shape[1])

        if self.overlap == 0:
            return data

        self._out[:self.overlap, :] = self._out[-self.overlap:, :]
        self._out[self.overlap:, :] = data

        return self._out.copy()

    def _preallocate(self, cols):
        self._out = np.zeros((self.length, cols))

    def __repr__(self):
        return "%s.%s(length=%s, overlap=%s)" % (
            self.__class__.__module__,
            self.__class__.__name__,
            self.length,
            self.overlap
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

    def fit(self, X, y):
        self.clf.fit(X, y)

    def process(self, data):
        return self.clf.predict(data)[0]
