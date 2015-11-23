import os
import time
import json
import pkg_resources

import numpy as np

from pygesture import filestruct
from pygesture import processing
from pygesture import features
from pygesture import wav
from pygesture import control
from pygesture import pipeline

from pygesture.cursor import cursor2d

from pygesture.ui.qt import QtGui, QtCore, QtWidgets
from pygesture.ui.templates.cursor_widget_template import Ui_CursorWidget


# time to wait before starting the recorder
trial_start_delay = 2000


class CursorWidget(QtWidgets.QWidget):

    session_started = QtCore.pyqtSignal()
    session_paused = QtCore.pyqtSignal()
    session_resumed = QtCore.pyqtSignal()
    session_finished = QtCore.pyqtSignal()

    def __init__(self, config, record_thread, base_session, parent=None):
        super(CursorWidget, self).__init__(parent)
        self.cfg = config
        self.test = getattr(config, 'test', False)
        self.record_thread = record_thread
        self.base_session = base_session

        self.ui = Ui_CursorWidget()
        self.ui.setupUi(self)

        self.session_running = False
        self.trial_running = False
        self.trial_initializing = False
        self.simulation = None
        self.robot = None
        self.prediction = 0

        self.init_base_session()
        self.init_cursor_view()
        self.init_session_progressbar()
        self.init_session_type_combo()
        self.init_timers()

        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def showEvent(self, event):
        self.init_record_thread()

    def hideEvent(self, event):
        self.dispose_record_thread()

    def init_base_session(self):
        pass

    def init_session_type_combo(self):
        pass

    def init_session_progressbar(self):
        pass

    def init_record_thread(self):
        self.record_thread.set_continuous()
        self.cfg.daq.set_channel_range(
            (min(self.cfg.channels), max(self.cfg.channels)))
        self.record_thread.ready_sig.connect(self.on_recorder_ready)
        self.record_thread.prediction_sig.connect(self.prediction_callback)
        self.record_thread.update_sig.connect(self.record_callback)

    def dispose_record_thread(self):
        self.record_thread.prediction_sig.disconnect(self.prediction_callback)
        self.record_thread.ready_sig.disconnect(self.on_recorder_ready)
        self.record_thread.pipeline = None
        self.record_thread.kill()

    def init_cursor_view(self):
        self.cursor_view = self.ui.cursorView
        self.cursor = cursor2d.CircleItem(self.cursor_view.map_size(0.1),
                                          color='#291859')
        self.target = cursor2d.CircleItem(self.cursor_view.map_size(0.3),
                                          color='#285491')
        self.cursor_view.scene().addItem(self.cursor)
        self.cursor_view.scene().addItem(self.target)

        self.target.set_norm_pos(0.5, -0.4)

    def init_timers(self):
        # timer which delays start of a trial (after trial initialization)
        self.trial_start_timer = QtCore.QTimer(self)
        self.trial_start_timer.setInterval(trial_start_delay)
        self.trial_start_timer.setSingleShot(True)
        self.trial_start_timer.timeout.connect(self.start_trial)

        # manually keep track of trial timing
        self.seconds_per_read = \
            self.cfg.daq.samples_per_read / self.cfg.daq.rate
        self.reads_per_trial = 0  # will be set on trial start

        # timer to wait between trials
        self.intertrial_timer = QtCore.QTimer(self)
        self.intertrial_timer.setInterval(self.cfg.inter_trial_timeout*1000)
        self.intertrial_timer.setSingleShot(True)
        self.intertrial_timer.timeout.connect(self.initialize_trial)

        # timer to check for target dwell
        self.dwell_timer = QtCore.QTimer(self)
        self.dwell_timer.setSingleShot(True)
        self.dwell_timer.timeout.connect(self.dwell_timeout)

    def start_session(self):
        self.session_started.emit()
        self.initialize_trial()

    def initialize_trial(self):
        self.trial_initializing = True
        #self.record_thread.set_pipeline(self.pipeline)

    def start_trial(self):
        self.trial_initializing = False
        self.trial_running = True
        self.record_thread.start()

    def on_recorder_ready(self):
        self.current_read_count = 0

    def pause_trial(self):
        self.dwell_timer.stop()
        self.intertrial_timer.stop()
        self.trial_start_timer.stop()

        self.record_thread.kill()
        self.trial_running = False

    def finish_trial(self, success=False):
        self.pause_trial()
        self.prediction = 0
        self.update_cursor_view()

        self.logger.success = success
        self.session.write_trial(
            self.trial_number,
            self.logger.get_data(),
            self.cfg.daq.rate)

        if self.trial_number == len(self.tac_session.trials):
            self.finish_session()
        else:
            self.trial_number += 1
            self.intertrial_timer.start()

    def finish_session(self):
        self.session_finished.emit()
        self.session_running = False

        self.ui.sessionInfoBox.setEnabled(True)
        self.ui.pauseButton.setEnabled(False)

    def on_target_enter(self):
        self.dwell_timer.stop()
        self.dwell_timer.start()

    def dwell_timeout(self):
        self.finish_trial(success=True)

    def on_target_leave(self):
        self.dwell_timer.stop()

    def prediction_callback(self, data):
        """Called by the `RecordThread` when it produces a new output."""
        mav, label = data

        if not self.trial_running:
            return

        if not self.test:
            self.prediction = label
        else:
            # negative input because user reverses target movements
            data = ([-0.5], self.prediction)

        commands = self.controller.process(data)

        self.update_cursor_view()

        self.current_read_count += 1
        if self.current_read_count > self.reads_per_trial:
            self.finish_trial()

    def record_callback(self, data):
        """Called by the `RecordThread` when it gets new recording data."""
        print('hey')

    def keyPressEvent(self, event):
        if self.test and self.trial_running:
            key = event.key()
            if key == QtCore.Qt.Key_Up:
                self.prediction = 0
            elif key == QtCore.Qt.Key_Down:
                self.prediction = 1
            else:
                super().keyPressEvent(event)
        else:
            super().keyPressEvent(event)

    def update_cursor_view(self):
        pass

    def build_pipeline(self):
        """
        Builds the processing pipeline. Most of the pipeline is specified by
        the config, but we need to gather training data, build a classifier
        with that data, and insert the classifier into the pipeline.
        """
        pass
