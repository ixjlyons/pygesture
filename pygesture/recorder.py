import os
import random
import shutil

from PyQt4 import QtCore
import numpy as np
import scipy.io.wavfile as siowav

from pygesture import filestruct
from pygesture.simulation import config, vrepsim


class RecordThread(QtCore.QThread):

    update_sig = QtCore.pyqtSignal(np.ndarray)
    finished_sig = QtCore.pyqtSignal(np.ndarray)
    prediction_sig = QtCore.pyqtSignal(int)

    def __init__(self, daq, run_sim=False):
        QtCore.QThread.__init__(self, parent=None)
        self.daq = daq
        self.run_sim = run_sim

        self.continuous = True
        self.triggers_per_record = 0
        self.running = False
        self.simulation = None
        self.pipeline = None

        if self.run_sim:
            vrepsim.set_path(config.path)
            self.simulation = vrepsim.VrepSimulation(config.vrep_port)

    def run(self):
        self.running = True

        if self.continuous:
            self.run_continuous()
        else:
            self.run_fixed()

    def run_continuous(self):
        robot = None
        if self.simulation:
            self.simulation.start()
            robot = vrepsim.Robot(self.simulation.clientId, config.actions)

        self.daq.start()

        while self.running:
            d = self.daq.read()
            if self.pipeline is not None:
                y = self.pipeline.run(d)
                self.prediction_sig.emit(y)

                if robot is not None:
                    robot.do_action("rest")
                    #robot.do_action(st.gesture_dict['l'+str(int(y[0]))][1])

            self.update_sig.emit(d)

        if self.simulation is not None:
            if robot is not None:
                robot.do_action("rest")
            self.simulation.stop()

    def run_fixed(self):
        spr = self.daq.samples_per_read
        data = np.zeros((self.daq.num_channels, spr*self.triggers_per_record))
        self.daq.start()
        for i in range(self.triggers_per_record):
            d = self.daq.read()

            data[:, i*spr:(i+1)*spr] = d
            self.update_sig.emit(d)

        self.daq.stop()
        self.finished_sig.emit(data)

    def set_continuous(self):
        self.continuous = True

    def set_fixed(self, triggers_per_record):
        self.triggers_per_record = triggers_per_record
        self.continuous = False

    def set_pipeline(self, pipeline):
        self.pipeline = pipeline

    def kill(self):
        self.running = False
        self.wait()

    def cleanup(self):
        if self.simulation is not None:
            self.simulation.finish()


def generate_trial_order(labels, n_repeat):
    """
    Generates the sequence of trials for the session. Each label is represented
    a specified number of times, and the order is randomized.

    Parameters
    ----------
    labels : list
        List of trial labels (e.g. 'l0', 'l5', etc.).
    n_repeat : int
        Number of times to repeat each gesture.
    """
    l = labels * n_repeat
    random.shuffle(l)
    return l


class Session:

    def __init__(self, data_root, labels, n_repeat):
        self.gesture_order = generate_trial_order(labels, n_repeat)
        self.current_trial = 0
        self.data_root = data_root

    def set_ids(self, pid, sid):
        self.participant_id = pid
        self.session_id = sid

        try:
            self.init_file_structure()
        except IOError:
            raise

    def init_file_structure(self, force=False):
        session_dir, date_str = \
            filestruct.new_session_dir(self.data_root,
                self.participant_id, self.session_id)
        recording_dir = filestruct.get_recording_dir(session_dir)

        if os.path.isdir(session_dir):
            if force:
                shutil.rmtree(session_dir)
            else:
                raise IOError('Session directory already exists.')
                return

        os.makedirs(session_dir)
        os.makedirs(recording_dir)

        self.date_str = date_str
        self.session_dir = session_dir
        self.recording_dir = recording_dir

    def overwrite_session(self):
        self.init_file_structure(force=True)

    def start_trial(self):
        self.current_trial += 1
        self.current_gesture = self.gesture_order[self.current_trial-1]
        return (self.current_trial, self.current_gesture)

    def write_recording(self, data, fs):
        rec_file = filestruct.get_recording_file(
            self.recording_dir, self.participant_id, self.session_id,
            self.date_str, self.current_trial, self.current_gesture)

        data *= 32768
        data = data.astype(np.int16, copy=False)
        siowav.write(rec_file, fs, data.T)
