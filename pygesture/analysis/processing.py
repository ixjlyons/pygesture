import os
from multiprocessing import Pool

import numpy as np

from pygesture import filestruct
from pygesture import wav


class Processor(object):
    """
    Speficies how to process recording files, including conditioning and
    feature extraction from relevant segments of the files. It is basically a
    workaround so all of this information can be passed conveniently from the
    config to the Recording class, which does all of the work.

    Parameters
    ----------
    conditioner : pipeline.Conditioner object
        Conditions the data (usually filters and downsamples).
    windower : pipeline.Windower object
        Holds data for overlapping windows.
    feature_extractor : features.FeatureExtractor object
        Extracts features from waveform data.
    rest_bounds : 2-tuple of ints
        Specifies (start, end) sample indices for the rest class.
    gesture_bounds : 2-tuple of ints
        Specifies (start, end) smaple indices for the gesture class.
    """

    def __init__(self, conditioner, windower, feature_extractor, rest_bounds,
                 gesture_bounds):
        self.conditioner = conditioner
        self.windower = windower
        self.feature_extractor = feature_extractor
        self.rest_bounds = rest_bounds
        self.gesture_bounds = gesture_bounds


def batch_process(rootdir, pid, processor, sid_list='all', pool=1):
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
        sid_list = filestruct.get_session_list(rootdir, pid)

    if pool > 1:
        pool = Pool(processes=pool)
        pool.map(_process_session, [
            (rootdir, pid, sid, processor) for sid in sid_list])
        pool.close()
    else:
        for sid in sid_list:
            _process_session((
                rootdir, pid, sid, processor))


def _process_session(args):
    """
    Internally used for processing a single session. The input should be a
    tuple matching the input args of the Session constructor.
    """
    sess = Session(*args)
    sess.process()


def read_feature_file_list(file_list, labels='all'):
    """
    Reads all of the feature files specified and concatenates all of their data
    into a (vector, label) tuple.

    Parameters
    ----------
    file_list : list (str)
        List of paths to feature files.
    labels : list (int)
        List of labels to include in the data. Default is 'all', meaning all
        labels in the files are included.
    """
    data = np.concatenate([np.genfromtxt(f, delimiter=',') for f in file_list])
    X = data[:, 1:]
    y = data[:, 0]

    if labels == 'all':
        return (X, y)

    else:
        mask = np.zeros(y.shape, dtype=bool)
        for label in labels:
            mask |= (y == label)

        return (X[mask], y[mask])


def get_session_data(rootdir, pid, sid_list):
    """
    Convenience function to retrieve the data for the specified particpiant and
    session ID list in a (vector, label) tuple.
    """
    file_list = filestruct.get_feature_file_list(rootdir, pid, sid_list)
    (X, y) = read_feature_file_list(file_list)
    return (X, y)


class Session:
    """
    Processor of a group of recordings that were taken consecutively.

    Parameters
    ----------
    rootdir : str
        Root directory of the data (see pygesture.filestruct).
    pid : str
        ID of the participant who generated the data.
    sid : str
        ID of the session.
    processor : pygesture.analysis.processing.Processor
        Processor used to transform the raw data to conditioned data and
        feature data.

    Attributes
    ----------
    sessdir : str
        Path to the session directory.
    rawdir : str
        Path to the directory containing the raw recording files.
    procdir : str
        Path to the directory to place the conditioned recording files.
    featfile : str
        Path to the feature file to be generated.
    """
    def __init__(self, rootdir, pid, sid, processor):
        self.sid = sid
        self.pid = pid
        self.processor = processor

        self.sessdir = filestruct.find_session_dir(rootdir, pid, sid)
        self.rawdir = filestruct.get_recording_dir(self.sessdir)
        self.procdir = filestruct.get_processed_dir(self.sessdir)

        self.featfile = filestruct.new_feature_file(
            self.sessdir,
            self.pid,
            self.sid,
            filestruct.parse_date_string(self.sessdir))

        if not os.path.exists(self.procdir):
            os.mkdir(self.procdir)

    def process(self, saveproc=True):
        """
        Iterates over all recordings in the session, processes them (see
        Recording's process method), writes the conditioned data to procdir,
        and writes the features to a CSV file.
        """
        if os.path.isfile(self.featfile):
            os.remove(self.featfile)

        with open(self.featfile, 'ab') as fid:
            for f in filestruct.get_recording_file_list(self.rawdir):
                try:
                    rec = Recording(f, self.processor)
                except KeyError:
                    continue

                proc_data, features = rec.process()

                procfile = os.path.join(self.procdir, rec.filename)
                fs_proc = self.processor.conditioner.f_down
                wav.write(procfile, fs_proc, proc_data)

                np.savetxt(fid, features, delimiter=',', fmt='%.5e')


class Recording:
    """
    Representation of a single multi-channel raw recording.

    Parameters
    ----------
    wavfile : str
        Full path to the raw recording (WAV file).
    processor : pygesture.analysis.processing.Processor
        Processor used to transform the raw data to conditioned data and
        feature data.

    Attributes
    ----------
    fs_raw : int
        Sampling rate (Hz) of the raw recording as read from the WAV file.
    filename : str
        Name of the WAV file (name only, no path).
    raw_data : array, shape (n_samples, n_channels)
        Raw data as read from the WAV file.
    trial_number : int
        Trial number of the recording (pertains to the session it was recorded
        in).
    label : int
        Label of the recording as a whole, relevant to recordings in which a
        gesture is held throughout.
    conditioned_data : array, shape (n_samples_conditioned, n_channels)
        Raw data that has been transformed by the conditioner (of the input
        processor)
    feature_data : array, shape (n_windows, n_features+1)
        Feature data with the label of the recording in the first column. If
        rest bounds are given in the processor, the first rows of the feature
        data will be rest data, and the remaining portion will be from the
        gesture bounds given in the processor.
    """
    def __init__(self, wavfile, processor):
        self.wavfile = wavfile
        self.processor = processor

        self._conditioner = self.processor.conditioner
        self._feature_extractor = self.processor.feature_extractor
        self._windower = self.processor.windower

        self._read_file()

    def _read_file(self):
        self.fs_raw, self.raw_data = wav.read(self.wavfile)
        path, self.filename = os.path.split(self.wavfile)

        self.trial_number = filestruct.parse_trial_number(self.filename)
        self.label = filestruct.parse_label(self.filename)

    def process(self):
        """
        Processes the raw recording data in two steps. The first step is to
        condition the data (usually something like normalization, filtering,
        etc.), specified by the conditioner belonging to this recording's
        processor object. The second step is to calculate features from the
        conditioned data. The conditioned data is windowed according to the
        processor's windower (window length, overlap) and for each window, the
        processor's feature extractor is applied. The conditioned data and the
        feature data are returned.

        Returns
        -------
        conditioned_data : array, shape (n_samples_conditioned, n_channels)
            The conditioned data.
        feature_data : array, shape (n_windows, n_features+1)
            The feature data. Each row is an instance. The first column is
            the gesture label. The rest of the columns are feature types.
        """
        self._conditioner.clear()
        cd = self._conditioner.process(self.raw_data)

        rb = self.processor.rest_bounds
        if rb is not None:
            rest_data = cd[rb[0]:rb[1]]
            rest_ind = list(
                windowind(rest_data.shape[0], self._windower.length,
                          overlap=self._windower.overlap))
            n_rest = len(rest_ind)
        else:
            rest_ind = []
            n_rest = 0

        gb = self.processor.gesture_bounds
        gest_data = cd[gb[0]:gb[1]]
        gest_ind = list(
            windowind(gest_data.shape[0], self._windower.length,
                      overlap=self._windower.overlap))
        n_gest = len(gest_ind)

        n_rows = n_rest + n_gest
        fd = np.zeros((n_rows, self._feature_extractor.n_features+1))
        for i, ind in enumerate(rest_ind):
            fd[i, 0] = 0
            fd[i, 1:] = self._feature_extractor.process(
                rest_data[ind[0]:ind[1]])
        for i, ind in enumerate(gest_ind):
            fd[n_rest+i, 0] = self.label
            fd[n_rest+i, 1:] = self._feature_extractor.process(
                gest_data[ind[0]:ind[1]])

        self.conditioned_data = cd
        self.feature_data = fd

        return self.conditioned_data, self.feature_data


def window(x, length, overlap=0, axis=0):
    """
    Generates a sequence of windows of the input data, each with a specified
    length and optional overlap with the previous window. Only windows of the
    specified length are retrieved (if windows don't fit evenly into the data).
    """
    n = x.shape[axis]
    for f, t in windowind(n, length, overlap=overlap):
        if axis == 0:
            yield x[f:t, :]
        else:
            yield x[:, f:t]


def windowind(n, length, overlap=0):
    """
    Generates a sequence of pairs of indices corresponding to consecutive
    windows of an array of length n. Returns a tuple (low_ind, high_ind) which
    can be used to window an array like `win = data[low_ind, high_ind]`.
    """
    ind = range(0, n, length-overlap)
    for i in ind:
        if i + length < n:
            yield i, i+length
