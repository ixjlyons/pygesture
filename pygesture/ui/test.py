import argparse
import sys
import pkg_resources

from pygesture import config
from pygesture import filestruct
from pygesture import processing
from pygesture import pipeline
from pygesture import daq
from pygesture import features
from pygesture.simulation import vrepsim

import numpy as np
from sklearn.lda import LDA
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from PyQt4 import QtGui, QtCore

from pygesture.ui.test_widget import Ui_TestWidget


class TestWidget(QtGui.QWidget):

    def __init__(self, config, record_thread, parent=None):
        super(TestWidget, self).__init__(parent)
        self.cfg = config
        self.record_thread = record_thread

        self.ui = Ui_TestWidget()
        self.ui.setupUi(self)

        self.running = False
        self.simulation = None
        self.robot = None
        self.prediction = 0
        self.calibration = np.zeros((1, len(self.cfg.channels)))

        self.init_record_thread()
        self.init_gesture_view()

        self.ui.trainButton.clicked.connect(self.build_pipeline)
        self.ui.connectButton.clicked.connect(self.toggle_connect_callback)
        self.ui.startButton.clicked.connect(self.toggle_running_callback)
        self.ui.startButton.setEnabled(False)

    def showEvent(self, event):
        if self.simulation is None:
            self.init_simulation()

    def init_simulation(self):
        vrepsim.set_path(self.cfg.vrep_path)
        self.sim_connect_thread = SimulationConnectThread(self.cfg.vrep_port)
        self.sim_connect_thread.finished.connect(
            self.simulation_connected_callback)
        self.sim_connect_thread.start()

    def simulation_connected_callback(self, simulation):
        self.simulation = simulation

        if simulation is None:
            self.ui.connectButton.setEnabled(False)
            QtGui.QMessageBox().warning(
                self,
                "Warning",
                "Couldn't connect to v-rep.",
                QtGui.QMessageBox.Ok)

    def init_record_thread(self):
        self.record_thread.set_continuous()
        self.record_thread.prediction_sig.connect(self.prediction_callback)

    def init_gesture_view(self):
        self.gesture_images = dict()
        for (key, val) in self.cfg.arm_gestures.items():
            imgpath = pkg_resources.resource_filename(
                __name__, 'images/'+val[1]+'.png')
            img = QtGui.QPixmap(imgpath)
            self.gesture_images[key] = img

        self.ui.gestureDisplayLabel.resize_signal.connect(
            self.update_gesture_view)

    def init_boosts_dock(self):
        self.ui.boostsDock.hide()
        # sorry for the hackage, need a list of (label, 'abbrv') tuples sorted
        # by label to easily change the controller {label: boost} dict
        d = self.cfg.arm_gestures
        labels = [(l, d[l][0]) for l in sorted(d)]

        self.ui.boostsWidget.set_mapping(labels, limits=(0, 1000), init=1)
        self.ui.boostsWidget.updated.connect(self.boosts_callback)

    def boosts_callback(self, boosts):
        self.cfg.controller.boosts = boosts

    def probe_callback(self):
        self._show_signal_window("probe")

    def check_signals_callback(self):
        self._show_signal_window("check signals")

    def _show_signal_window(self, title):
        if title == "probe":
            signal_window = signals.SignalDialog(1)
            self.daq.set_channel_range(
                (self.cfg.probe_channel, self.cfg.probe_channel))
        else:
            signal_window = signals.SignalDialog(len(self.cfg.channels))

        signal_window.setWindowTitle(title)
        self.record_thread.set_continuous()
        self.record_thread.update_sig.connect(signal_window.update_plot)
        self.record_thread.start()
        signal_window.exec_()
        self.record_thread.kill()
        self.daq.set_channel_range(
            (min(self.cfg.channels), max(self.cfg.channels)))
        self.record_thread.update_sig.disconnect(signal_window.update_plot)

    def update_gesture_view(self, event=None):
        w = self.ui.gestureDisplayLabel.width()
        h = self.ui.gestureDisplayLabel.height()

        if self.running:
            imgkey = self.prediction
        else:
            imgkey = 0

        self.ui.gestureDisplayLabel.setPixmap(
            self.gesture_images[imgkey].scaled(
                w, h, QtCore.Qt.KeepAspectRatio))

    def set_pid(self, pid):
        self.pid = pid
        self.ui.trainingList.clear()
        self.sid_list = filestruct.get_session_list(
            self.cfg.data_path, self.pid)
        for sid in self.sid_list:
            item = QtGui.QListWidgetItem(sid, self.ui.trainingList)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Unchecked)

    def toggle_connect_callback(self):
        starting = self.ui.connectButton.isChecked()

        if starting:
            self.simulation.start()
            self.robot = vrepsim.IRB140Arm(self.simulation.clientId)
        else:
            self.robot.stop()
            self.simulation.stop()
            self.robot = None

        self.ui.startButton.setEnabled(starting)

    def toggle_running_callback(self):
        starting = (not self.running)

        if starting:
            self.start_running()
        else:
            self.stop_running()

        self.ui.connectButton.setEnabled((not starting))

    def build_pipeline(self):
        train_list = []
        for i in range(self.ui.trainingList.count()):
            item = self.ui.trainingList.item(i)
            if item.checkState():
                train_list.append(item.text())

        if not train_list:
            QtGui.QMessageBox().critical(
                self, "Error",
                "No sessions selected for training.",
                QtGui.QMessageBox.Ok)
            return

        self.ui.sessionInfoBox.setEnabled(False)

        file_list = filestruct.get_feature_file_list(
            self.cfg.data_path, self.pid, train_list)
        training_data = processing.read_feature_file_list(
            file_list, labels=list(self.cfg.arm_gestures))

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
        for label, names in self.cfg.arm_gestures.items():
            mav_avg = np.mean(X[y == label, :], axis=1)
            # -np.partition(-data, N) gets N largest elements of data
            boosts[label] = 1 / np.mean(-np.partition(-mav_avg, 10)[:10])
        #self.ui.boostsWidget.set_values(boosts)

        clf_type = self.ui.classifierComboBox.currentText()
        if clf_type == 'LDA':
            clf = LDA()
        elif clf_type == 'SVM':
            clf = SVC(C=50, kernel='linear')
        else:
            clf = LDA()

        preproc = StandardScaler()
        skpipeline = Pipeline([('preproc', preproc), ('clf', clf)])

        classifier = pipeline.Classifier(skpipeline)
        classifier.fit(*training_data)

        pl = pipeline.Pipeline(
            [
                self.cfg.conditioner,
                self.cfg.windower,
                (
                    features.FeatureExtractor(
                        [features.MAV()],
                        len(self.cfg.channels)),
                    [
                        self.cfg.feature_extractor,
                        classifier
                    ],
                )
            ]
        )

        self.record_thread.set_pipeline(pl)

    def start_running(self):
        self.record_thread.start()

        self.ui.startButton.setText('Pause')
        self.running = True

    def stop_running(self):
        self.robot.stop()
        self.record_thread.kill()
        self.ui.sessionInfoBox.setEnabled(True)
        self.ui.startButton.setText('Start')
        self.running = False
        self.prediction = 0
        self.update_gesture_view()

    def prediction_callback(self, prediction):
        if not self.running:
            return

        self.prediction = prediction[1]
        if self.robot is not None:
            commands = self.cfg.controller.process(prediction)
            self.robot.command(commands)
        self.update_gesture_view()


class SimulationConnectThread(QtCore.QThread):

    finished = QtCore.pyqtSignal(object)

    def __init__(self, port):
        super(SimulationConnectThread, self).__init__()
        self.port = port

    def run(self):
        try:
            sim = vrepsim.VrepSimulation(self.port)
        except:
            sim = None

        self.finished.emit(sim)

