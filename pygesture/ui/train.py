import os
import pkg_resources
import random

import numpy as np
import scipy.io.wavfile as siowav

from pygesture import filestruct

from PyQt4 import QtGui, QtCore
from pygesture.ui.train_widget_template import Ui_TrainWidget


class TrainWidget(QtGui.QWidget):

    session_started = QtCore.pyqtSignal()
    session_paused = QtCore.pyqtSignal()
    session_resumed = QtCore.pyqtSignal()
    session_finished = QtCore.pyqtSignal()

    def __init__(self, config, record_thread, parent=None):
        super(TrainWidget, self).__init__(parent)
        self.cfg = config
        self.record_thread = record_thread

        self.ui = Ui_TrainWidget()
        self.ui.setupUi(self)

        self.running = False

        self.init_gesture_view()
        self.init_gesture_prompt()
        self.init_session_progressbar()
        self.init_buttons()
        self.init_intertrial_timer()

    def showEvent(self, event):
        self.init_record_thread()

    def hideEvent(self, event):
        self.dispose_record_thread()

    def init_record_thread(self):
        tpr = self.cfg.trial_duration * \
            int(self.cfg.daq.rate / self.cfg.daq.samples_per_read)
        self.cfg.daq.set_channel_range(
            (min(self.cfg.channels), max(self.cfg.channels)))
        self.record_thread.set_fixed(triggers_per_record=tpr)
        self.record_thread.finished_sig.connect(self.record_finished)

    def dispose_record_thread(self):
        try:
            self.record_thread.finished_sig.disconnect(self.record_finished)
        except TypeError:
            pass
        self.record_thread.kill()

    def init_gesture_view(self):
        self.gesture_images = dict()
        for (key, val) in self.cfg.arm_gestures.items():
            imgpath = pkg_resources.resource_filename(
                __name__, 'images/'+val[1]+'.png')
            img = QtGui.QPixmap(imgpath)
            self.gesture_images[key] = img

        self.update_gesture_view()

    def update_gesture_view(self, imgkey=0):
        self.ui.gestureView.setPixmap(self.gesture_images[imgkey])

    def init_gesture_prompt(self):
        self.ui.promptWidget.ticks = self.cfg.trial_duration
        self.ui.promptWidget.transitions = self.cfg.prompt_times
        self.ui.promptWidget.setMaximum(1000*self.cfg.trial_duration)
        self.prompt_anim = QtCore.QPropertyAnimation(
            self.ui.promptWidget, 'value')
        self.prompt_anim.setDuration(1000*self.cfg.trial_duration)
        self.prompt_anim.setStartValue(0)
        self.prompt_anim.setEndValue(1000*self.cfg.trial_duration)

    def init_session_progressbar(self):
        self.ui.sessionProgressBar.setMinimum(0)
        self.ui.sessionProgressBar.setMaximum(
            self.cfg.num_repeats*len(list(self.cfg.arm_gestures)))
        self.ui.sessionProgressBar.setValue(0)

    def init_buttons(self):
        self.ui.startButton.clicked.connect(self.start_session)
        self.ui.pauseButton.clicked.connect(self.pause_session)

    def init_intertrial_timer(self):
        self.intertrial_timer = QtCore.QTimer(self)
        self.intertrial_timer.setSingleShot(True)
        self.intertrial_timer.timeout.connect(self.start_recording)

    def set_session(self, session):
        self.base_session = session
        self.session = Session(
            session, list(self.cfg.arm_gestures), self.cfg.num_repeats)

    def start_session(self):
        self.running = True
        self.ui.startButton.setEnabled(False)
        self.start_recording()
        self.session_started.emit()

    def start_recording(self):
        trial, gesture = self.session.start_trial()
        self.ui.sessionProgressBar.setValue(trial)
        self.update_gesture_view(imgkey=gesture)
        self.ui.pauseButton.setEnabled(False)
        self.record_thread.start()
        self.prompt_anim.start()

    def record_finished(self, data):
        self.session.write_recording(data, self.cfg.daq.rate)

        self.update_gesture_view()
        self.ui.pauseButton.setEnabled(True)

        if self.session.current_trial == self.session.num_trials:
            self.finish_session()
            return

        if self.running:
            self.intertrial_timer.start(1000*self.cfg.inter_trial_timeout)

    def pause_session(self):
        if self.running:
            if self.intertrial_timer.isActive():
                self.intertrial_timer.stop()
            self.running = False
            self.ui.pauseButton.setText('Resume')
            self.session_paused.emit()
        else:
            self.running = True
            self.start_recording()
            self.ui.pauseButton.setText('Pause')
            self.session_resumed.emit()

    def finish_session(self):
        self.running = False
        self.ui.startButton.setEnabled(True)
        self.session_finished.emit()


def generate_trial_order(labels, n_repeat):
    """
    Generates the sequence of trials for the session. Each label is represented
    a specified number of times, and the order is randomized.

    Parameters
    ----------
    labels : list
        List of trial labels.
    n_repeat : int
        Number of times to repeat each gesture.

    Returns
    -------
    new_labels : list
        List of randomized trials.
    """
    new_labels = labels * n_repeat
    random.shuffle(new_labels)
    return new_labels


class Session(object):

    def __init__(self, session, labels, n_repeat):
        self.parent_session = session

        self.gesture_order = generate_trial_order(labels, n_repeat)
        self.num_trials = len(self.gesture_order)
        self.current_trial = 0

        self.init_file_structure()

    def init_file_structure(self):
        self.recording_dir = filestruct.get_recording_dir(
            self.parent_session.session_dir)
        os.makedirs(self.recording_dir)

    def start_trial(self):
        self.current_trial += 1
        self.current_gesture = self.gesture_order[self.current_trial-1]
        return (self.current_trial, self.current_gesture)

    def write_recording(self, data, fs):
        rec_file = filestruct.get_recording_file(
            self.recording_dir,
            self.parent_session.pid,
            self.parent_session.sid,
            self.parent_session.datestr,
            self.current_trial,
            self.current_gesture)

        data *= 32768
        data = data.astype(np.int16, copy=False)
        siowav.write(rec_file, fs, data.T)
