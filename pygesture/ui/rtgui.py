import sys
import os
import pkg_resources

from pygesture import filestruct
from pygesture import processing
from pygesture import settings as st
from pygesture import recorder

import numpy as np
from sklearn.lda import LDA
from sklearn.svm import SVC

from PyQt4 import QtGui, QtCore

from pygesture.ui.rtgui_template import *
from pygesture.ui.calibrationdialog_template import *


class RealTimeGUI(QtGui.QMainWindow):

    def __init__(self, *args):
        super(RealTimeGUI, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.running = False
        self.prediction = 0
        self.calibration = np.zeros((1, st.NUM_CHANNELS))

        while True:
            try: 
                self.recorder = recorder.RecordThread(run_sim=True)
                break
            except ValueError:
                ret = QtGui.QMessageBox().critical(
                    self, "Error",
                    "Could not connect to DAQ.",
                    QtGui.QMessageBox.Retry|QtGui.QMessageBox.Abort)
                if ret == QtGui.QMessageBox.Abort:
                    raise ValueError("Could not connect to DAQ.")

        self.init_recorder()
        self.init_pid_list()
        self.init_gesture_view()

        self.ui.startButton.clicked.connect(self.toggle_running_callback)
        self.ui.actionCalibrate.triggered.connect(self.calibrate)

        self.setWindowTitle('pygesture-rt')

    def init_recorder(self):
        self.recorder.set_continuous(True)
        self.recorder.prediction_sig.connect(self.prediction_callback)

    def init_pid_list(self):
        pid_list = filestruct.get_participant_list()
        pid_list = [pid for pid in pid_list if pid.startswith('p')]
        self.pid_list = pid_list

        self.ui.pidComboBox.addItems(self.pid_list)
        self.ui.pidComboBox.currentIndexChanged.connect(self.set_pid)

        self.set_pid(0)

    def init_gesture_view(self):
        self.gesture_images = dict()
        for (key, val) in st.gesture_dict.items():
            imgpath = pkg_resources.resource_filename(
                __name__, 'images/'+val[1]+'.png')
            img = QtGui.QPixmap(imgpath)
            self.gesture_images[key] = img

        self.ui.gestureDisplayLabel.resize_signal.connect(
            self.update_gesture_view)

    def update_gesture_view(self, event=None):
        w = self.ui.gestureDisplayLabel.width()
        h = self.ui.gestureDisplayLabel.height()

        if self.running:
            imgkey = 'l' + str(self.prediction)
        else:
            imgkey = 'l0'

        self.ui.gestureDisplayLabel.setPixmap(
            self.gesture_images[imgkey].scaled(
                w, h, QtCore.Qt.KeepAspectRatio))

    def set_pid(self, index):
        self.pid = self.pid_list[index]
        self.ui.trainingList.clear()
        self.sid_list = filestruct.get_session_list(self.pid)
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
            st.DATA_ROOT, self.pid, train_list)
        training_data = processing.read_feature_file_list(file_list)

        clf_type = self.ui.classifierComboBox.currentText()
        if clf_type == 'LDA':
            clf = LDA()
        elif clf_type == 'SVM':
            clf = SVC(C=50, kernel='linear')
        else:
            clf = LDA()

        pl = processing.Pipeline(clf, training_data, self.calibration)

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

    def prediction_callback(self, prediction):
        self.prediction = prediction
        self.update_gesture_view()

    def calibrate(self):
        caldialog = CalibrateDialog(self.recorder)
        caldialog.save_signal.connect(self.set_calibration)
        caldialog.exec_()
        self.init_recorder()

    def set_calibration(self, calibration):
        self.calibration = calibration


class CalibrateDialog(QtGui.QDialog):

    save_signal = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, recorder, parent=None):
        super(CalibrateDialog, self).__init__()
        self.ui = Ui_CalibrationDialog()
        self.ui.setupUi(self)

        self.progress = 0

        self.recorder = recorder
        self.recorder.set_continuous(False)
        self.recorder.finished_sig.connect(self.record_finished_callback)
        self.recorder.update_sig.connect(self.record_update_callback)
        self.calibration_data = np.zeros((1, st.NUM_CHANNELS))

        self.ui.startButton.clicked.connect(self.start_calibration)
        self.ui.buttonBox.accepted.connect(self.save_callback)

    def start_calibration(self):
        self.ui.buttonBox.setEnabled(False)
        self.ui.startButton.setEnabled(False)
        self.recorder.start()

    def record_update_callback(self):
        self.progress += 1/float(st.TRIGGERS_PER_RECORD)*100
        self.ui.progressBar.setValue(self.progress)

    def record_finished_callback(self, data):
        self.ui.progressBar.setValue(100)
        self.ui.buttonBox.setEnabled(True)
        self.ui.startButton.setEnabled(True)

        self.calibration_data = np.mean(data, 1)

    def save_callback(self):
        self.save_signal.emit(self.calibration_data)

    def closeEvent(self, event):
        recorder.cleanup()
        QMainWindow.closeEvent(self, event)


def main():
    app = QtGui.QApplication([])
    try:
        mw = RealTimeGUI()
    except ValueError:
        sys.exit(-1)

    mw.show()
    app.exec_()
    app.deleteLater()
    sys.exit(0)
    
