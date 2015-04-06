import argparse
import sys
import pkg_resources

from pygesture import config
from pygesture import filestruct
from pygesture import processing
from pygesture import pipeline
from pygesture import daq
from pygesture import recorder
from pygesture import features
from pygesture.simulation import vrepsim

import numpy as np
from sklearn.lda import LDA
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from PyQt4 import QtGui, QtCore

from pygesture.ui.test_template import Ui_MainWindow


class RealTimeGUI(QtGui.QMainWindow):

    def __init__(self, config, parent=None):
        super(RealTimeGUI, self).__init__(parent)
        self.cfg = config

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.running = False
        self.prediction = 0
        self.calibration = np.zeros((1, len(self.cfg.channels)))

        self.init_recorder()
        self.init_simulation()
        self.init_pid_list()
        self.init_gesture_view()
        self.init_boosts_dock()

        self.ui.startButton.clicked.connect(self.toggle_running_callback)

    def init_recorder(self):
        try:
            self.daq = self.cfg.daq
            self.daq.initialize()
        except ValueError:
            # fall back on "fake" DAQ
            self.daq = daq.Daq(
                self.daq.rate, self.daq.input_range, self.daq.channel_range,
                self.daq.samples_per_read)

            QtGui.QMessageBox().warning(
                self,
                "Warning",
                "Falling back to emulated DAQ.",
                QtGui.QMessageBox.Ok)

        self.recorder = recorder.RecordThread(self.daq)
        self.recorder.prediction_sig.connect(self.prediction_callback)

    def init_simulation(self):
        self.robot = None
        vrepsim.set_path(self.cfg.vrep_path)
        try:
            self.simulation = vrepsim.VrepSimulation(self.cfg.vrep_port)
        except:
            QtGui.QMessageBox().warning(
                self,
                "Warning",
                "Running without v-rep simulation.",
                QtGui.QMessageBox.Ok)

    def init_pid_list(self):
        pid_list = filestruct.get_participant_list(self.cfg.data_path)
        pid_list = [pid for pid in pid_list if pid.startswith('p')]
        self.pid_list = pid_list

        self.ui.pidComboBox.addItems(self.pid_list)
        self.ui.pidComboBox.currentIndexChanged.connect(self.set_pid)

        self.set_pid(0)

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

        self.ui.boostsWidget.set_mapping(labels, limits=(0, 5), init=1)
        self.ui.boostsWidget.updated.connect(self.boosts_callback)

    def boosts_callback(self, boosts):
        self.cfg.controller.boosts = boosts

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

    def set_pid(self, index):
        self.pid = self.pid_list[index]
        self.ui.trainingList.clear()
        self.sid_list = filestruct.get_session_list(
            self.cfg.data_path, self.pid)
        for sid in self.sid_list:
            item = QtGui.QListWidgetItem(sid, self.ui.trainingList)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Unchecked)

    def toggle_running_callback(self):
        if not self.running:
            self.start_running()
        else:
            self.stop_running()

    def start_running(self):
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

        if self.simulation is not None:
            self.simulation.start()
            self.robot = vrepsim.IRB140Arm(self.simulation.clientId)

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

        self.recorder.set_pipeline(pl)
        self.recorder.start()

        self.ui.startButton.setText('Pause')
        self.running = True

    def stop_running(self):
        self.recorder.kill()
        self.ui.sessionInfoBox.setEnabled(True)
        self.ui.startButton.setText('Start')
        self.running = False
        self.prediction = 0
        self.update_gesture_view()
        if self.robot is not None:
            self.robot.stop()
            self.simulation.stop()

    def prediction_callback(self, prediction):
        self.prediction = prediction[1]
        if self.robot is not None:
            commands = self.cfg.controller.process(prediction)
            self.robot.command(commands)
        self.update_gesture_view()


def main():
    parser = argparse.ArgumentParser(
        description="EMG gesture recognition with real-time feedback.")
    parser.add_argument(
        '-c', '--config',
        dest='config',
        default='config.py',
        help="Config file. Default is `config.py` (current directory).")
    args = parser.parse_args()

    cfg = config.Config(args.config)

    app = QtGui.QApplication([])
    mw = RealTimeGUI(cfg)
    mw.show()
    app.exec_()
    app.deleteLater()
    sys.exit(0)
