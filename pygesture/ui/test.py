"""
Real-time gesture recognition and control test setup.

Testing protocol:
    - a classifier is trained
    - a target achievement control (TAC) test session type is selected
    - the session is started:
        - a timer is started which delays the start of a trial (2 second)
        - the simulation is started
        - the target robot moves into position
        - the trial begins and the user attempts to move the robot to target
        - the trial ends if timeout is triggered or the robot sits within the
          target posture (with specified angular tolerance) for a specified
          dwell time
        - the simulation is stopped
        - an inter-trial timer is started, triggering the next trial
    - at the end of a session, UI is re-enabled and a new session can be
      created
"""

import os
import time
import json
import pkg_resources

import numpy as np

from pygesture import filestruct
from pygesture import features
from pygesture import wav
from pygesture import control
from pygesture import pipeline
from pygesture.analysis import processing
from pygesture.simulation import vrepsim

from pygesture.ui.qt import QtGui, QtCore, QtWidgets
from pygesture.ui.templates.test_widget_template import Ui_TestWidget


# time to wait before starting the recorder
trial_start_delay = 1000


class TestWidget(QtWidgets.QWidget):

    session_started = QtCore.pyqtSignal()
    session_paused = QtCore.pyqtSignal()
    session_resumed = QtCore.pyqtSignal()
    session_finished = QtCore.pyqtSignal()

    def __init__(self, config, record_thread, base_session, parent=None):
        super(TestWidget, self).__init__(parent)
        self.cfg = config
        self.test = getattr(config, 'test', False)
        self.record_thread = record_thread
        self.base_session = base_session

        self.ui = Ui_TestWidget()
        self.ui.setupUi(self)

        self.session_running = False
        self.trial_running = False
        self.trial_initializing = False
        self.simulation = None
        self.robot = None
        self.prediction = 0

        self.init_base_session()
        self.init_gesture_view()
        self.init_session_progressbar()
        self.init_session_type_combo()
        self.init_timers()

        self.ui.trainButton.clicked.connect(self.on_train_clicked)
        self.ui.startButton.clicked.connect(self.on_start_clicked)
        self.ui.pauseButton.clicked.connect(self.on_pause_clicked)

        self.ui.controlsBox.setEnabled(False)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def showEvent(self, event):
        if self.simulation is None and self.isEnabled():
            self.init_simulation()

        self.init_record_thread()

    def hideEvent(self, event):
        self.dispose_record_thread()
        if self.simulation is not None:
            self.simulation.stop()

    def init_base_session(self):
        if self.simulation is None and self.isVisible():
            self.init_simulation()

        self.pid = self.base_session.pid
        self.ui.trainingList.clear()
        self.sid_list = filestruct.get_session_list(
            self.cfg.data_path, self.pid, search="train")
        for sid in self.sid_list:
            item = QtWidgets.QListWidgetItem(sid, self.ui.trainingList)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Unchecked)

        self.lefty = True if self.base_session.hand == 'left' else False

    def init_session_type_combo(self):
        for k, v in sorted(self.cfg.tac_sessions.items()):
            self.ui.sessionTypeComboBox.addItem(k)

        self.ui.sessionTypeComboBox.activated[str].connect(
            self.on_session_type_selection)
        self.on_session_type_selection(
            self.ui.sessionTypeComboBox.currentText())

    def init_session_progressbar(self):
        self.ui.sessionProgressBar.setMinimum(0)
        self.ui.sessionProgressBar.setMaximum(1)
        self.ui.sessionProgressBar.setValue(0)

    def init_simulation(self):
        self.sim_connect_thread = SimulationConnectThread()
        self.sim_connect_thread.finished.connect(
            self.on_simulation_connected)
        self.sim_connect_thread.start()

    def init_record_thread(self):
        self.record_thread.set_continuous()
        self.cfg.daq.set_channel_range(
            (min(self.cfg.channels), max(self.cfg.channels)))
        self.record_thread.ready_sig.connect(self.on_recorder_ready)
        self.record_thread.prediction_sig.connect(self.prediction_callback)
        self.record_thread.update_sig.connect(self.record_callback)
        self.record_thread.error_sig.connect(self.on_record_error)

    def dispose_record_thread(self):
        self.record_thread.prediction_sig.disconnect(self.prediction_callback)
        self.record_thread.ready_sig.disconnect(self.on_recorder_ready)
        self.record_thread.error_sig.disconnect(self.on_record_error)
        self.record_thread.pipeline = None
        self.record_thread.kill()

    def init_gesture_view(self):
        self.gesture_images = dict()
        for gesture in self.cfg.gestures:
            imgpath = pkg_resources.resource_filename(
                __name__, 'images/'+gesture.description+'.png')
            img = QtGui.QPixmap(imgpath)

            if self.lefty and 'no-contraction' not in imgpath:
                # flip horizontally
                t = QtGui.QTransform(-1, 0, 0, 1, 0, 0)
                img = img.transformed(t)

            self.gesture_images[gesture.label] = img

        self.update_gesture_view()

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

    def on_simulation_connected(self, simulation):
        self.simulation = simulation

        if simulation is None:
            QtWidgets.QMessageBox().warning(
                self,
                "Warning",
                "Couldn't connect to v-rep.",
                QtWidgets.QMessageBox.Ok)

    def on_session_type_selection(self, text):
        self.tac_session = self.cfg.tac_sessions[text]
        self.ui.sessionProgressBar.setMaximum(len(self.tac_session.trials))

    def on_train_clicked(self):
        self.build_pipeline()
        self.ui.controlsBox.setEnabled(True)
        self.ui.startButton.setEnabled(True)

    def on_start_clicked(self):
        self.start_session()

    def on_pause_clicked(self):
        if self.ui.pauseButton.text() == "Pause":
            self.pause_trial()
            self.ui.pauseButton.setText("Resume")
        else:
            self.initialize_trial()
            self.ui.pauseButton.setText("Pause")

    def start_session(self):
        self.session_started.emit()

        self.tac_session.reshuffle()
        self.session = Session(self.base_session, self.tac_session)

        self.ui.sessionInfoBox.setEnabled(False)
        self.ui.startButton.setEnabled(False)
        self.ui.pauseButton.setEnabled(True)

        self.trial_number = 1
        self.dwell_timer.setInterval(self.tac_session.dwell*1000)
        self.reads_per_trial = int(
            self.tac_session.timeout / self.seconds_per_read)
        self.initialize_trial()
        self.session_running = True

    def initialize_trial(self):
        """
        Starts the simulation, initializes the robots in the simulation, starts
        a timer for the trial to start, and positions the target robot.
        """
        self.trial_initializing = True
        self.ui.sessionProgressBar.setValue(self.trial_number)

        self.record_thread.set_pipeline(self.pipeline)

        self.logger = Logger(
            self.tac_session, self.trial_number-1,
            self.training_sessions, self.boosts)

        if self.simulation is not None:
            self.simulation.start()
            self.acquired_signal = vrepsim.IntegerSignal(
                self.simulation.clientId, 'target_acquired')
            self.state_signal = vrepsim.IntegerSignal(
                self.simulation.clientId, 'trial_state')
            self.tol_signal = vrepsim.FloatSignal(
                self.simulation.clientId, 'tolerance')
            self.robot = vrepsim.MPL(self.simulation.clientId)

        self.trial_start_timer.start()

        if self.simulation is not None:
            gestures = self.tac_session.trials[self.trial_number-1]
            target = {g.action: self.tac_session.dist for g in gestures}
            self.tol_signal.write(self.tac_session.tol)
            self.state_signal.write(2)
            self.robot.set_visible(False)
            self.robot.position_controlled = True
            self.robot.command(target)

    def start_trial(self):
        """
        Starts the trial -- recording, prediction, robot control, etc. all
        starts here, not in `initialize_trial`.
        """
        self.trial_initializing = False
        self.trial_running = True
        self.record_thread.start()

    def on_recorder_ready(self):
        self.current_read_count = 0
        if self.simulation is not None:
            self.state_signal.write(3)
            self.robot.position_controlled = False
            self.robot.set_visible(True)

    def pause_trial(self):
        self.dwell_timer.stop()
        self.intertrial_timer.stop()
        self.trial_start_timer.stop()

        if self.simulation is not None:
            self.robot.stop()
            self.simulation.stop()

        self.record_thread.kill()
        self.trial_running = False

    def finish_trial(self, success=False):
        self.pause_trial()
        self.prediction = 0
        self.update_gesture_view()

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

        if self.simulation is not None:
            commands = self.controller.process(data)
            self.robot.command(commands)

            acq = self.acquired_signal.read()
            if acq is not None:
                if acq == 1:
                    self.on_target_enter()
                else:
                    self.on_target_leave()

            self.logger.log(self.prediction, commands, self.robot.pose, acq)

        self.update_gesture_view()

        self.current_read_count += 1
        if self.current_read_count > self.reads_per_trial:
            self.finish_trial()

    def record_callback(self, data):
        """Called by the `RecordThread` when it gets new recording data."""
        self.logger.record(data)

    def on_record_error(self):
        self.on_pause_clicked()
        QtWidgets.QMessageBox().critical(
            self, "Error",
            "DAQ failure.",
            QtWidgets.QMessageBox.Ok)

    def keyPressEvent(self, event):
        if self.test and self.trial_running:
            label = self.tac_session.trials[self.trial_number-1][0].label
            if event.key() == QtCore.Qt.Key_PageUp:
                self.prediction = label
            elif event.key() == QtCore.Qt.Key_PageDown:
                self.prediction = 0
            else:
                super().keyPressEvent(event)
        else:
            super().keyPressEvent(event)

    def update_gesture_view(self):
        if self.trial_running:
            imgkey = self.prediction
        else:
            imgkey = 0

        self.ui.gestureDisplayLabel.setPixmap(self.gesture_images[imgkey])

    def build_pipeline(self):
        """
        Builds the processing pipeline. Most of the pipeline is specified by
        the config, but we need to gather training data, build a classifier
        with that data, and insert the classifier into the pipeline.
        """
        train_list = []
        for i in range(self.ui.trainingList.count()):
            item = self.ui.trainingList.item(i)
            if item.checkState():
                train_list.append(str(item.text()))
        self.training_sessions = train_list

        if not train_list:
            QtWidgets.QMessageBox().critical(
                self, "Error",
                "No sessions selected for training.",
                QtWidgets.QMessageBox.Ok)
            return

        # get only the labels for the selected TAC session
        # need to loop over available gestures to catch those with no dof
        labels = []
        mapping = {}
        for gesture in self.cfg.gestures:
            if gesture.dof is None:
                labels.append(gesture.label)
                mapping[gesture.label] = gesture.action
            else:
                if gesture in self.tac_session.gestures:
                    labels.append(gesture.label)
                    mapping[gesture.label] = gesture.action

        file_list = filestruct.get_feature_file_list(
            self.cfg.data_path, self.pid, train_list)
        training_data = processing.read_feature_file_list(
            file_list, labels=labels)

        # get average MAV for each gesture label to auto-set boosts
        # warning: super hacky
        j = 0
        start = 0
        for i, feature in enumerate(self.cfg.feature_extractor.features):
            if 'MAV' in str(feature):
                start = j
                break
            else:
                j += feature.dim_per_channel*len(self.cfg.channels)
        X, y = training_data
        X = X[:, start:len(self.cfg.channels)]
        boosts = dict()
        for label in labels:
            mav_avg = np.mean(X[y == label, :], axis=1)
            # -np.partition(-data, N) gets N largest elements of data
            boosts[label] = 1 / np.mean(-np.partition(-mav_avg, 10)[:10])
        self.boosts = boosts

        # re-create the controller to make sure it has the correct mapping
        self.controller = control.DBVRController(
            mapping=mapping,
            ramp_length=self.cfg.controller.ramp_length,
            boosts=1 if self.test else boosts)

        self.cfg.learner.fit(*training_data)

        self.pipeline = pipeline.Pipeline([
            self.cfg.conditioner,
            self.cfg.windower,
            (
                features.FeatureExtractor(
                    [features.MAV()], len(self.cfg.channels)),
                [
                    self.cfg.feature_extractor,
                    self.cfg.learner
                ],
            )
        ])

        self.record_thread.set_pipeline(self.pipeline)


class Session(object):

    def __init__(self, base_session, tac_session):
        self.base_session = base_session
        self.tac_session = tac_session

        self.init_file_structure()

    def init_file_structure(self):
        self.recording_dir = filestruct.get_recording_dir(
            self.base_session.session_dir)
        os.makedirs(self.recording_dir)

        self.log_dir = filestruct.get_log_dir(
            self.base_session.session_dir)
        os.makedirs(self.log_dir)

    def write_trial(self, trial_number, data, fs):
        rec, log = data

        rec_file = filestruct.get_recording_file(
            self.recording_dir,
            self.base_session.pid,
            self.base_session.sid,
            self.base_session.datestr,
            trial_number)

        wav.write(rec_file, fs, rec.T)

        log_file = filestruct.get_log_file(
            self.log_dir,
            self.base_session.pid,
            self.base_session.sid,
            self.base_session.datestr,
            trial_number)

        with open(log_file, 'w') as f:
            f.write(log)


class Logger(object):

    def __init__(self, tac_session, trial_index, training_sessions, boosts):
        self.started = False
        self.success = False

        self.tac_session = tac_session
        self.trial_index = trial_index
        self.training_sessions = training_sessions
        self.boosts = boosts

        self.active_classes = [g.action for g in tac_session.gestures]
        self.target = {
            'dist': tac_session.dist,
            'pose': [g.action for g in tac_session.trials[trial_index]]
        }

        self.trial_data = {
            'timestamp': [],
            'prediction': [],
            'command': [],
            'target_entered': [],
            'pose': {}
        }
        self.rec_data = []

    def log(self, prediction, command, pose, acq):
        if not self.started:
            self.start_timestamp = time.time()

            for k, v in pose.items():
                self.trial_data['pose'][k] = []

            self.started = True

        ts = time.time() - self.start_timestamp

        self.trial_data['timestamp'].append(ts)
        self.trial_data['prediction'].append(prediction)

        if acq:
            self.trial_data['target_entered'].append(ts)

        self.trial_data['command'].append(command)

        for k, v in pose.items():
            self.trial_data['pose'][k].append(v)

    def record(self, data):
        self.rec_data.append(data)

    def get_data(self):
        rec = np.concatenate(self.rec_data, axis=1)

        d = dict(
            training_sessions=self.training_sessions,
            boosts=self.boosts,
            active_classes=self.active_classes,
            trial_data=self.trial_data,
            target=self.target,
            success=self.success
        )
        log = json.dumps(d, indent=4)

        return (rec, log)


class SimulationConnectThread(QtCore.QThread):

    finished = QtCore.pyqtSignal(object)

    def __init__(self):
        super(SimulationConnectThread, self).__init__()

    def run(self):
        try:
            sim = vrepsim.VrepSimulation()
        except:
            sim = None

        self.finished.emit(sim)
