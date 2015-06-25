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

    def __init__(self, rootdir, pid, sid, processor):
        self.sid = sid
        self.pid = pid
        self.processor = processor

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

        feat_fid = open(self.featfile, 'ab')

        for f in self.recording_file_list:
            try:
                rec = Recording(f, self.processor)
            except KeyError:
                continue
            proc_data, features = rec.process()

            outfile = os.path.join(self.procdir, rec.filename)
            fs_proc = self.processor.conditioner.f_down
            wav.write(outfile, fs_proc, proc_data)

            np.savetxt(feat_fid, features, delimiter=',', fmt='%.5e')


class Recording:

    def __init__(self, wavfile, processor, loc='leg'):
        self.conditioner = processor.conditioner
        self.feature_extractor = processor.feature_extractor
        self.windower = processor.windower

        self.n_features = self.feature_extractor.n_features

        self.fs_raw, self.raw_data = wav.read(wavfile)
        path, self.filename = os.path.split(wavfile)
        self.location = loc
        self.parse_details(self.filename)

        self.rest_ind = range(
            processor.rest_bounds[0], processor.rest_bounds[1],
            self.windower.length-self.windower.overlap)
        self.gest_ind = range(
            processor.gesture_bounds[0], processor.gesture_bounds[1],
            self.windower.length-self.windower.overlap)

    def parse_details(self, filename):
        self.trial_number = filestruct.parse_trial_number(filename)
        self.label = filestruct.parse_label(filename)

    def process(self):
        cd = self.conditioner.process(self.raw_data)

        num_gestures = len(self.rest_ind) + len(self.gest_ind)
        fd = np.zeros((num_gestures, self.n_features+1))
        for i, n in enumerate(self.rest_ind):
            label = 0
            x = cd[n:n+self.windower.length, :]
            fd[i, 0] = label
            fd[i, 1:] = self.feature_extractor.process(x)

        rl = len(self.rest_ind)
        for i, n in enumerate(self.gest_ind):
            x = cd[n:n+self.windower.length, :]
            fd[rl+i, 0] = self.label
            fd[rl+i, 1:] = self.feature_extractor.process(x)

        self.conditioned_data = cd
        self.feature_data = fd

        return (cd, fd)

    def get_dict(self):
        data_dict = {
            'label': self.label,
            'trial_number': self.trial_number,
            'data': self.feature_data.tolist()}

        return data_dict
