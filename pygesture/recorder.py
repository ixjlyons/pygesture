import os
import random
import shutil

from PyQt4 import QtCore
import numpy as np
import scipy.io.wavfile as siowav

from pygesture import settings as st
from pygesture import mccdaq
from pygesture import filestruct
from pygesture.simulation import config, vrepsim


class RecordThread(QtCore.QThread):

    update_sig = QtCore.pyqtSignal(np.ndarray)
    finished_sig = QtCore.pyqtSignal(np.ndarray)
    prediction_sig = QtCore.pyqtSignal(int)

    def __init__(self, usedaq=True, run_sim=False):
        QtCore.QThread.__init__(self, parent=None)
        self.usedaq = usedaq
        self.run_sim = run_sim
        self.continuous = False
        self.single_channel_mode = False
        self.running = False
        self.daq = None
        self.simulation = None
        self.pipeline = None

        if self.usedaq and self.daq is None:
            self.daq = mccdaq.MccDaq(st.SAMPLE_RATE, st.INPUT_RANGE,
                                     st.CHANNEL_RANGE, st.SAMPLES_PER_READ)

        if self.run_sim:
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

        if self.usedaq:
            self.daq.start()

        while self.running:
            if self.usedaq:
                d = self.daq.read()
                if self.pipeline is not None:
                    y = self.pipeline.run(d)
                    self.prediction_sig.emit(y)

                    if robot is not None:
                        robot.do_action("rest")
                        robot.do_action(st.gesture_dict['l'+str(int(y[0]))][1])

            else:
                nch = st.NUM_CHANNELS
                if self.single_channel_mode:
                    nch = 1
                d = 0.2*(np.random.rand(nch, st.SAMPLES_PER_READ) - 0.5)
                self.msleep(1000*st.SAMPLES_PER_READ/st.SAMPLE_RATE)

            self.update_sig.emit(d)

        if self.simulation is not None:
            if robot is not None:
                robot.do_action("rest")
            self.simulation.stop()

    def run_fixed(self):
        data = np.zeros((st.NUM_CHANNELS,
                         st.SAMPLES_PER_READ*st.TRIGGERS_PER_RECORD))
        if self.usedaq:
            self.daq.start()
        for i in range(st.TRIGGERS_PER_RECORD):
            if self.usedaq:
                d = self.daq.read()
            else:
                nch = st.NUM_CHANNELS
                if self.single_channel_mode:
                    nch = 1
                d = 0.2*(np.random.rand(nch, st.SAMPLES_PER_READ) - 0.5)
                self.msleep(1000*st.SAMPLES_PER_READ/st.SAMPLE_RATE)

            data[:, i*st.SAMPLES_PER_READ:(i+1)*st.SAMPLES_PER_READ] = d
            self.update_sig.emit(d)

        if self.usedaq:
            self.daq.stop()
        self.finished_sig.emit(data)

    def set_single_channel_mode(self, single_channel, ch=0):
        self.single_channel_mode = single_channel
        if single_channel:
            if self.usedaq:
                self.daq.set_channel_range((ch, ch))
        else:
            if self.usedaq:
                self.daq.set_channel_range(st.CHANNEL_RANGE)

    def set_continuous(self, continuous):
        self.continuous = continuous

    def set_pipeline(self, pipeline):
        self.pipeline = pipeline

    def kill(self):
        self.running = False
        self.wait()

    def cleanup(self):
        if self.simulation is not None:
            self.simulation.finish()


class Session:

    def __init__(self):
        self.generate_gesture_order()
        self.current_trial = 0

    def generate_gesture_order(self):
        self.gesture_indices = []
        for i in range(1, st.NUM_GESTURES+1):
            self.gesture_indices.extend([i]*st.NUM_REPEATS)

        random.shuffle(self.gesture_indices)

    def set_ids(self, pid, sid):
        self.participant_id = pid
        self.session_id = sid

        try:
            self.init_file_structure()
        except IOError:
            raise

    def init_file_structure(self, force=False):
        session_dir, date_str = \
            filestruct.new_session_dir(self.participant_id, self.session_id)
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
        self.current_gesture = 'l' + \
            str(self.gesture_indices[self.current_trial-1])
        return (self.current_trial, self.current_gesture)

    def write_recording(self, data):
        rec_file = filestruct.get_recording_file(
            self.recording_dir, self.participant_id, self.session_id,
            self.date_str, self.current_trial, self.current_gesture)

        data *= 32768
        data = data.astype(np.int16, copy=False)
        siowav.write(rec_file, st.SAMPLE_RATE, data.T)
