import sys
import os

#from PySide import QtGui, QtCore
from PyQt4 import QtGui, QtCore

from pygesture import settings as st
from pygesture.ui import signals, results, clfbuilder
from pygesture import filestruct
from pygesture import recorder


class MainWindow(QtGui.QWidget):

    def __init__(self, debug=False):
        super(MainWindow, self).__init__()

        self.running = False
        self.debug = debug

        self.create_record_thread()
        self.create_menu()
        self.create_gesture_view()
        self.create_gesture_prompt()
        self.create_session_form()
        self.create_session_progressbar()
        self.create_event_buttons()
        self.create_intertrial_timer()

        self.main_layout = QtGui.QHBoxLayout()

        self.left_side_layout = QtGui.QVBoxLayout()
        self.left_side_layout.addWidget(self.gesture_view)
        self.left_side_layout.addWidget(self.gesture_prompt)

        self.right_side_layout = QtGui.QVBoxLayout()
        self.right_side_layout.addWidget(self.session_info_box)
        self.right_side_layout.addStretch()
        self.right_side_layout.addWidget(self.session_progressbar)
        self.right_side_layout.addLayout(self.button_box)

        self.main_layout.addLayout(self.left_side_layout)
        self.main_layout.addLayout(self.right_side_layout)
        self.main_layout.setMenuBar(self.menu_bar)

        self.setLayout(self.main_layout)
        self.setWindowTitle('pygesture')

        self.start_button.clicked.connect(self.start_session)
        self.pause_button.clicked.connect(self.pause_session)

    def create_record_thread(self):
        self.record_thread = recorder.RecordThread(usedaq=(not self.debug))
        self.record_thread.finished_sig.connect(self.record_finished)

    def create_menu(self):
        self.menu_bar = QtGui.QMenuBar()

        self.file_menu = QtGui.QMenu('&File', self)
        self.exit_action = self.file_menu.addAction('E&xit')
        self.menu_bar.addMenu(self.file_menu)
        self.exit_action.triggered.connect(self.close)

        self.view_menu = QtGui.QMenu('&View', self)
        self.signal_check_action = self.view_menu.addAction('&Check Signals')
        self.signal_check_action.triggered.connect(self.check_signals)
        self.signal_probe_action = self.view_menu.addAction('&Probe')
        self.signal_probe_action.triggered.connect(self.probe_signal)
        self.process_session_action = self.view_menu.addAction(
            'Process &Session')
        self.process_session_action.triggered.connect(self.process_session)
        self.menu_bar.addMenu(self.view_menu)

    def create_gesture_view(self):
        self.gesture_view = QtGui.QLabel()
        imgpath = os.path.join(os.path.dirname(__file__), 'images')
        self.gesture_images = dict()
        for (key, val) in st.gesture_dict.items():
            filepath = os.path.join(imgpath, val[1] + '.png')
            img = QtGui.QPixmap(filepath).scaled(
                800, 600, QtCore.Qt.KeepAspectRatio)
            self.gesture_images[key] = img
        self.gesture_view.setPixmap(self.gesture_images['l0'])

    def create_gesture_prompt(self):
        self.gesture_prompt = PromptWidget(
            st.SECONDS_PER_RECORD, (st.ONSET_TRANSITION, st.OFFSET_TRANSITION))
        self.prompt_anim = QtCore.QPropertyAnimation(
            self.gesture_prompt, 'value_prop')
        self.prompt_anim.setDuration(1000*st.SECONDS_PER_RECORD)
        self.prompt_anim.setStartValue(0)
        self.prompt_anim.setEndValue(1000*st.SECONDS_PER_RECORD)

    def create_session_form(self):
        self.session_info_box = QtGui.QGroupBox("Session Info")
        layout = QtGui.QFormLayout()
        self.participant_input = QtGui.QLineEdit()
        self.session_input = QtGui.QLineEdit()
        layout.addRow(QtGui.QLabel("Participant:"), self.participant_input)
        layout.addRow(QtGui.QLabel("Session:"), self.session_input)
        self.session_info_box.setLayout(layout)

    def create_session_progressbar(self):
        self.session_progressbar = QtGui.QProgressBar(self)
        self.session_progressbar.setMinimum(0)
        self.session_progressbar.setMaximum(st.NUM_GESTURES*st.NUM_REPEATS)
        self.session_progressbar.setFormat('Trial: %v / %m')
        self.session_progressbar.setValue(0)

    def create_event_buttons(self):
        self.button_box = QtGui.QHBoxLayout()
        self.start_button = QtGui.QPushButton('Start')
        self.pause_button = QtGui.QPushButton('Pause')
        self.button_box.addWidget(self.start_button)
        self.button_box.addWidget(self.pause_button)
        self.pause_button.setEnabled(False)

    def create_intertrial_timer(self):
        self.intertrial_timer = QtCore.QTimer(self)
        self.connect(self.intertrial_timer,
                     QtCore.SIGNAL('timeout()'), self.start_recording)
        self.intertrial_timer.setSingleShot(True)

    def start_session(self):
        self.session = recorder.Session()
        pid = self.participant_input.text()
        sid = self.session_input.text()
        if pid == '' or sid == '':
            message = QtGui.QMessageBox().critical(
                self, "Error", "Input session info before starting.")
            return

        try:
            self.session.set_ids(pid, sid)
        except IOError:
            message = QtGui.QMessageBox().warning(
                self, "Warning",
                "Session directory already exists.\nOverwrite?",
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.Cancel)

            if message == QtGui.QMessageBox.Cancel:
                return
            elif message == QtGui.QMessageBox.Yes:
                self.session.overwrite_session()

        self.running = True
        self.start_button.setEnabled(False)
        self.session_info_box.setEnabled(False)
        self.start_recording()

    def start_recording(self):
        trial, gesture = self.session.start_trial()
        self.session_progressbar.setValue(trial)
        self.gesture_view.setPixmap(self.gesture_images[gesture])
        self.pause_button.setEnabled(False)
        self.record_thread.start()
        self.prompt_anim.start()

    def record_finished(self, data):
        self.session.write_recording(data)

        self.gesture_view.setPixmap(self.gesture_images['l0'])
        self.pause_button.setEnabled(True)

        if self.session.current_trial == st.NUM_TRIALS:
            self.finish_session()
            return

        if self.running:
            self.intertrial_timer.start(1000*st.INTERTRIAL_TIMEOUT)

    def pause_session(self):
        if self.running:
            if self.intertrial_timer.isActive():
                self.intertrial_timer.stop()
            self.running = False
            self.pause_button.setText('Resume')
        else:
            self.running = True
            self.start_recording()
            self.pause_button.setText('Pause')

    def finish_session(self):
        self.running = False
        self.start_button.setEnabled(True)
        self.session_info_box.setEnabled(True)

    def check_signals(self):
        self.signal_window = signals.SignalCheckWindow(debug=self.debug)
        self.record_thread.set_continuous(True)
        self.record_thread.update_sig.connect(self.signal_window.update_plot)
        self.record_thread.start()
        self.signal_window.exec_()
        self.record_thread.kill()
        self.record_thread.update_sig.disconnect(self.signal_window.update_plot)

    def probe_signal(self):
        self.probe_window = signals.SignalProbeWindow(debug=self.debug)
        self.record_thread.set_continuous(True)
        self.record_thread.set_single_channel_mode(True, st.PROBE_CHANNEL)
        self.record_thread.update_sig.connect(self.probe_window.update_plot)
        self.record_thread.start()
        self.probe_window.exec_()
        self.record_thread.kill()
        self.record_thread.set_single_channel_mode(False)
        self.record_thread.update_sig.disconnect(self.probe_window.update_plot)

    def process_session(self):
        pid = self.participant_input.text()

        # make sure participant has completed all sessions
        sid_list = filestruct.get_session_list(pid)
        for sid in st.arm_session_list + st.leg_session_list:
            if sid not in sid_list:
                QtGui.QMessageBox().warning(
                    self, "Warning",
                    "Not all sessions found for this participant",
                    QtGui.QMessageBox.Ok)
                return

        dialog = results.SessionResultsDialog(pid)
        dialog.exec_()

    def train_classifier(self):
        dialog = clfbuilder.ClassifierBuilderDialog()
        if dialog.exec_():
            (pid, sid_list) = dialog.get_training_ids()
            self.clf = clfbuilder.train_classifier(pid, sid_list)

    def closeEvent(self, event):
        self.record_thread.kill()


class PromptWidget(QtGui.QWidget):

    HEIGHT = 40
    REST_COLOR = QtGui.QColor(90, 90, 90)
    CONTRACT_COLOR = QtGui.QColor(150, 80, 80, 150)

    def __init__(self, length, transitions):
        super(PromptWidget, self).__init__()
        self.setFixedHeight(PromptWidget.HEIGHT)
        self.value = 0
        self.tick_labels = [str(i) for i in range(1, length)]
        self.maximum = length*1000
        self.length = length
        self.trans1 = transitions[0]*1000
        self.trans2 = transitions[1]*1000
        self.transitions = transitions

        self.tick_font = QtGui.QFont('Serif', 7, QtGui.QFont.Light)
        self.prompt_font = QtGui.QFont('Serif', 10, QtGui.QFont.Light)

    def setProgress(self, value):
        self.value = value
        self.repaint()

    def getProgress(self):
        return self.value

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.draw(qp)
        qp.end()

    def draw(self, qp):

        w = self.size().width()
        h = self.size().height()

        tick_step = int(round(w / self.length))

        till = int(((w / float(self.maximum)) * self.value))
        full1 = int(((w / float(self.maximum)) * self.trans1))
        full2 = int(((w / float(self.maximum)) * self.trans2))

        qp.setPen(PromptWidget.REST_COLOR)
        qp.setBrush(PromptWidget.REST_COLOR)
        qp.drawRect(0, 0, till, h)

        qp.setPen(PromptWidget.CONTRACT_COLOR)
        qp.setBrush(PromptWidget.CONTRACT_COLOR)
        qp.drawRect(full1, 0, full2-full1, h)

        pen = QtGui.QPen(QtGui.QColor(20, 20, 20), 1, QtCore.Qt.SolidLine)

        qp.setPen(pen)
        qp.setBrush(QtCore.Qt.NoBrush)
        qp.drawRect(0, 0, w-1, h-1)

        qp.setFont(self.prompt_font)
        for t, l in zip(self.transitions, ['contract', 'rest']):
            x = int(((w / float(self.maximum)) * (t*1000.)))
            metrics = qp.fontMetrics()
            fw = metrics.width(l)
            qp.drawText(x-fw/2, h/2, l)

        qp.setFont(self.tick_font)
        j = 0
        for i in range(tick_step, self.length*tick_step, tick_step):
            qp.drawLine(i, h-5, i, h)
            metrics = qp.fontMetrics()
            fw = metrics.width(self.tick_labels[j])
            qp.drawText(i-fw/2, h-7, self.tick_labels[j])
            j += 1

    value_prop = QtCore.Property(float, getProgress, setProgress)


import argparse
def main():
    parser = argparse.ArgumentParser(description="Gesture recording system.")
    parser.add_argument('-d', '--debug', action='store_true',
        help="Run in debug mode (random input instead of DAQ hardware).")
    args = parser.parse_args()

    app = QtGui.QApplication([])
    mw = MainWindow(args.debug)
    mw.show()
    app.exec_()
    app.deleteLater()
    sys.exit()
