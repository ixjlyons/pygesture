"""
Handles processing (filtering, downsampling) of raw recording files and
calculation of features. The locations of the output files is determined
by the `filestruct` module, but the format of the feature file is specified
here within the `Session` class.
"""

# TODO: document Recording class
# TODO: document Session class
# TODO: better documentation of ndarray sizes

import os
from multiprocessing import Pool
import pickle

import numpy as np
import scipy.io.wavfile as siowav
from scipy import signal

from pygesture import filestruct
from pygesture import settings as st


def batch_process(rootdir, pid, sid_list='all', pool=1):
    """
    Processes the given participants' sessions. If sid_list is not provided,
    all sessions are processed.

    Parameters
    ----------
    rootdir : str
        The path to the root of the data file structure.
    pid : str
        The participant ID for which to process the files (e.g. 'p0').
    sid_list : list of strings, optional
        List of session IDs to process (e.g. ['arm1', 'arm2']). The default is
        'all', which means the function will search for all of the given
        participant's sessions and process them.
    pool : int, default 1
        The number of processes to start for processing. Default is 1, which
        means the function will not use the multiprocessing module.
    """
    if sid_list == 'all':
        sid_list = filestruct.get_session_list(pid)

    if pool > 1:
        pool = Pool(processes=pool)
        pool.map(process_session, [(rootdir, pid, sid) for sid in sid_list])
        pool.close()
    else:
        for sid in sid_list:
            process_session((rootdir, pid, sid))


def process_session(session_info):
    """
    Internally used for processing a single session. The input should be a
    tuple with (rootdir, pid, sid).
    """
    rootdir, pid, sid = session_info
    sess = Session(rootdir, pid, sid)
    sess.process()


def mav(x):
    """
    Calculates the mean absolute value of a signal.

    Parameters
    ----------
    x : ndarray
        The signal (can be multidimensional, in which case the MAV is
        calculated along columns)

    Returns
    -------
    y : ndarray
        The mean absolute value of each channel of the input.
    """
    y = np.mean(np.absolute(x), 0)
    return y


def wl(x):
    """
    Calculates the waveform length of a signal. Waveform length is just the
    sum of the absolute value of all deltas (between adjacent taps) of a
    signal.

    Parameters
    ----------
    x : ndarray
        The raw signal(s) to calculate WL for. If multidimensional, WL is
        calculated along columns.

    Returns
    -------
    y : ndarray
        The waveform length of each channel of the input.
    """
    x2 = np.vstack((x[0, :], x[:-1, :]))
    y = np.sum(np.absolute(x - x2), 0)
    return y


def zc(x, thresh):
    """
    Calculates the number of zero crossings in a signal, subject to a threshold
    for discarding noisy fluctuations above and below zero.

    Parameters
    ----------
    x : ndarray
        The raw signal(s) to calculate ZC for. If multidimensional, ZC is
        calculated along columns.
    thresh : float
        The threshold for discriminating true zero crossings from those caused
        by noise.

    Returns
    -------
    y : ndarray
        The number of zero crossings in each channel of the input.
    """
    xrows, xcols = x.shape
    y = np.zeros(xcols)
    for i in range(xcols):
        for j in range(1, xrows):
            if ((x[j, i] > 0 and x[j-1, i] < 0) or
                    (x[j, i] < 0 and x[j-1, i] > 0)):
                if np.absolute(x[j, i] - x[j-1, i]) > thresh:
                    y[i] += 1
    return y


def ssc(x, thresh):
    """
    Calculates the number of slope sign changes in a signal, subject to a
    threshold for discarding noisy fluctuations.

    Parameters
    ----------
    x : ndarray
        The raw signal(s) to calculate SSC for. If multidimensional, SSC is
        calculated along columns.
    thresh : float
        The threshold for discriminating true slope sign changes from those
        caused by noise.

    Returns
    -------
    y : ndarray
        The number of slope sign changes in each channel of the input.
    """
    xrows, xcols = x.shape
    y = np.zeros(xcols)
    for i in range(xcols):
        for j in range(1, xrows-1):
            if ((x[j, i] > x[j-1, i] and x[j, i] > x[j+1, i]) or
                    (x[j, i] < x[j-1, i] and x[j, i] < x[j+1, i])):
                if (np.absolute(x[j, i] - x[j-1, i]) > thresh or
                        np.absolute(x[j, i] - x[j+1, i]) > thresh):
                    y[i] += 1
    return y


def get_features(x):
    """
    Calculates the four time-domain features (MAV, WL, ZC, and SSC) and stacks
    the result in a matrix.

    Parameters
    ----------
    x : ndarray
        The raw signal(s) to calculate features for. Features will be calculate
        for each channel.

    Returns
    -------
    y : ndarray
        The features, stacked such that each group of columns represents the
        feature for all channels.
    """
    return np.hstack((mav(x), wl(x), zc(x, 0.001), ssc(x, 0.001)))


def condition(x, fs):
    """
    Conditions the signals according to experimental protocol. The processing
    steps are band pass filtering, mean-zeroing, and downsampling from the give
    sampling frequency.

    Parameters
    ----------
    x : ndarray
        The raw data to condition.
    fs : int
        The input sampling frequency in Hz.

    Returns
    -------
    y : ndarray
        The conditioned data, the same size as x.
    """
    wc = [f / (fs / 2.) for f in st.FC]
    b, a = signal.butter(st.FILTER_ORDER, wc, 'bandpass')
    x = x - np.mean(x, 0)
    x = signal.lfilter(b, a, x, 0)
    x = x[::fs/st.FS_PROC, :]
    return x


def read_feature_file_list(file_list):
    """
    Reads all of the feature files specified and concatenates all of their data
    into a (vector, label) tuple.
    """
    data = np.concatenate([np.genfromtxt(f, delimiter=',') for f in file_list])
    X = data[:, 1:]
    y = data[:, 0]
    return (X, y)


def get_session_data(pid, sid_list):
    """
    Convenience function to retrieve the data for the specified particpiant and
    session ID list in a (vector, label) tuple.
    """
    file_list = filestruct.get_feature_file_list(pid, sid_list)
    (X, y) = read_feature_file_list(file_list)
    return (X, y)


class Pipeline:

    def __init__(self, classifier, training_data, calibration_data):
        self.conditioner = Conditioner(calibration_data)
        self.classifier = classifier
        self.classifier.fit(*training_data)

    def run(self, x):
        x_cond = self.conditioner.condition(x.T)
        features = get_features(x_cond)
        y = self.classifier.predict(features)
        return y


class Conditioner:

    def __init__(self, calibration_data):
        self.fs = st.SAMPLE_RATE
        wc = [f / (self.fs/2.0) for f in st.FC]
        self.b, self.a = signal.butter(st.FILTER_ORDER, wc, 'bandpass')
        zi = signal.lfilter_zi(self.b, self.a)
        self.zi = np.tile(zi, (st.NUM_CHANNELS, 1)).T
        self.x_mean = calibration_data

    def condition(self, x):
        x_centered = x - self.x_mean
        print(np.mean(x_centered, 0))
        x_filtered, self.zi = signal.lfilter(self.b, self.a, x_centered,
            axis=0, zi=self.zi)
        x_downsampled = x_filtered[::self.fs/st.FS_PROC, :]
        return x_downsampled


class Session:

    def __init__(self, rootdir, pid, sid):
        self.sid = sid
        self.pid = pid

        self.sessdir = filestruct.find_session_dir(rootdir, pid, sid)
        self.datestr = filestruct.parse_date_string(self.sessdir)
        self.featfile = filestruct.new_feature_file(
            self.sessdir, pid, sid, self.datestr)
        self.rawdir = filestruct.get_recording_dir(self.sessdir)
        self.procdir = filestruct.get_processed_dir(self.sessdir)

        if not os.path.exists(self.procdir):
            os.mkdir(self.procdir)

        self.recording_file_list = \
            filestruct.get_recording_file_list(self.rawdir)

    def process(self):
        if os.path.isfile(self.featfile):
            os.remove(self.featfile)

        feat_fid = open(self.featfile, 'a')

        dict_list = []
        for f in self.recording_file_list:
            try:
                rec = Recording(f)
            except KeyError:
                continue
            proc_data, features = rec.process()

            outfile = os.path.join(self.procdir, rec.filename)
            self.write_proc_file(outfile, proc_data)

            np.savetxt(feat_fid, features, delimiter=',', fmt='%.5e')
            dict_list.append(rec.get_dict())

        pickle_fid = open(self.featfile[:-4]+'.p', 'ab')
        pickle.dump(dict_list,  pickle_fid)

    def write_proc_file(self, filepath, data):
        data *= 32768
        data = data.astype(np.int16, copy=False)
        siowav.write(filepath, 2000, data)


class Recording:

    def __init__(self, wavfile, loc='leg'):
        fs_raw, data = siowav.read(wavfile)
        self.fs_raw = fs_raw
        self.raw_data = data / 32768.0
        path, self.filename = os.path.split(wavfile)
        self.location = loc
        self.parse_details(self.filename)

        self.rest_ind = range(st.REST_START_SAMP, st.REST_END_SAMP,
                              st.WINDOW_SHIFT_SAMP)
        self.gest_ind = range(st.GESTURE_START_SAMP, st.GESTURE_END_SAMP,
                              st.WINDOW_SHIFT_SAMP)
        self.num_features = get_features(self.raw_data[1:4, :]).size

    def parse_details(self, filename):
        trial_number = filestruct.parse_trial_number(filename)
        label_id = filestruct.parse_label(filename)

        if self.location == 'arm':
            label = st.arm_label_dict[label_id]
        else:
            label = st.leg_label_dict[label_id]

        self.label_id = label_id
        self.trial_number = trial_number
        self.label_short, self.label_long = label

    def process(self):
        conditioner = Conditioner(self.raw_data)
        cd = condition(self.raw_data, self.fs_raw)

        num_gestures = len(self.rest_ind) + len(self.gest_ind)
        fd = np.zeros((num_gestures, self.num_features+1))
        for i, n in enumerate(self.rest_ind):
            label = 0
            x = cd[n:n+st.WINDOW_LENGTH_SAMP, :]
            fd[i, 0] = label
            fd[i, 1:] = get_features(x)

        rl = len(self.rest_ind)
        for i, n in enumerate(self.gest_ind):
            label = int(self.label_id[1:])
            x = cd[n:n+st.WINDOW_LENGTH_SAMP, :]
            fd[rl+i, 0] = label
            fd[rl+i, 1:] = get_features(x)

        self.conditioned_data = cd
        self.feature_data = fd

        return (cd, fd)

    def get_dict(self):
        data_dict = {
            'label_id': self.label_id,
            'trial_number': self.trial_number,
            'data': self.feature_data.tolist()}

        return data_dict
