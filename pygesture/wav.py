import numpy as np
import scipy.io.wavfile as siowav


def write(filename, rate, data):
    """
    Writes recording data to file in WAV format. It is basically a convenience
    wrapper around `scipy.io.wavfile.write` for handling normalized float data.

    Paramters
    ---------
    filename : str
        Path + file name to the file to write to.
    rate : int
        Sample rate in Hz.
    data : ndarray
        Data to write. For multi-channel recordings, the shape should be
        (num_samples, num_channels).
    """
    data *= 32768
    data = data.astype(np.int16, copy=False)
    siowav.write(filename, rate, data)


def read(filename):
    """
    Reads recording data from a WAV file. It is basically a convenience wrapper
    around `scipy.io.wavfile.read` for getting float data.

    Parameters
    ----------
    filename : str
        Path + file name to the file to read from.

    Returns
    -------
    rate : int
        Sample rate.
    data : ndarray
        Float data (-1 to 1) from the file. Shape is (num_samples,
        num_channels).
    """
    rate, data = siowav.read(filename)
    data = data / 32768.0
    return rate, data


class ContinuousWriter(object):
    """
    Writes data to a WAV file chunk by chunk.

    Parameters
    ----------
    """

    def __init__(self, filename, fs):
        self.filename = filename
        self.fs = fs

        self.fid = open(self.filename, 'ab')

    def write(self, data):
        write(self.fid, self.fs, data)

    def close(self):
        self.fid.close()
