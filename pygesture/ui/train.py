import sys
import os
import argparse

from PyQt4 import QtGui, QtCore

from pygesture import config
from pygesture.ui import signals, results
from pygesture import daq
from pygesture import filestruct
from pygesture import recorder


class MainWindow(QtGui.QWidget):

    def __init__(self, config):
        super(MainWindow, self).__init__()
        self.cfg = config

        self.running = False

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
                "Couldn't find the specified DAQ. Falling back to emulator.",
                QtGui.QMessageBox.Ok)

        tpr = self.cfg.trial_duration * \
            int(self.daq.rate / self.daq.samples_per_read)
        self.record_thread = recorder.RecordThread(self.daq)
        self.record_thread.set_fixed(triggers_per_record=tpr)
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
        for (key, val) in self.cfg.arm_gestures.items():
            filepath = os.path.join(imgpath, val[1] + '.png')
            img = QtGui.QPixmap(filepath).scaled(
                800, 600, QtCore.Qt.KeepAspectRatio)
            self.gesture_images[key] = img
        self.gesture_view.setPixmap(self.gesture_images[0])

    def create_gesture_prompt(self):
        self.gesture_prompt = PromptWidget(
            self.cfg.trial_duration, (self.cfg.prompt_times))
        self.prompt_anim = QtCore.QPropertyAnimation(
            self.gesture_prompt, 'value_prop')
        self.prompt_anim.setDuration(1000*self.cfg.trial_duration)
        self.prompt_anim.setStartValue(0)
        self.prompt_anim.setEndValue(1000*self.cfg.trial_duration)

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
        self.session_progressbar.setMaximum(
            self.cfg.num_repeats*len(list(self.cfg.arm_gestures)))
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
        self.session = recorder.Session(
            self.cfg.data_path, list(self.cfg.arm_gestures),
            self.cfg.num_repeats)
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
        self.session.write_recording(data, self.daq.rate)

        self.gesture_view.setPixmap(self.gesture_images[0])
        self.pause_button.setEnabled(True)

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
        self.signal_window = signals.SignalCheckWindow(len(self.cfg.channels))
        self.record_thread.set_continuous()
        self.record_thread.update_sig.connect(self.signal_window.update_plot)
        self.record_thread.start()
        self.signal_window.exec_()
        self.record_thread.kill()
        self.record_thread.set_fixed()
        self.record_thread.update_sig.disconnect(
            self.signal_window.update_plot)

    def probe_signal(self):
        self.probe_window = signals.SignalProbeWindow()
        self.record_thread.set_continuous()
        self.daq.set_channel_range(
            (self.cfg.probe_channel, self.cfg.probe_channel))
        self.record_thread.update_sig.connect(self.probe_window.update_plot)
        self.record_thread.start()
        self.probe_window.exec_()
        self.record_thread.kill()
        self.record_thread.set_fixed()
        self.daq.set_channel_range(
            (min(self.cfg.channels), max(self.cfg.channels)))
        self.record_thread.update_sig.disconnect(self.probe_window.update_plot)

    def process_session(self):
        pid = self.participant_input.text()

        # make sure participant has completed all sessions
        sid_list = filestruct.get_session_list(self.cfg.data_path, pid)
        for sid in self.cfg.results_sid_arm + self.cfg.results_sid_leg:
            if sid not in sid_list:
                QtGui.QMessageBox().warning(
                    self, "Warning",
                    "Not all sessions found for this participant",
                    QtGui.QMessageBox.Ok)
                return

        dialog = results.SessionResultsDialog(pid, self.cfg)
        dialog.exec_()

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


def main():
    parser = argparse.ArgumentParser(description="Gesture recording system.")
    parser.add_argument(
        '-c', '--config',
        dest='config',
        default='config.py',
        help="Config file. Default is `config.py` (current directory).")
    args = parser.parse_args()

    cfg = config.Config(args.config)

    app = QtGui.QApplication([])
    mw = MainWindow(cfg)
    mw.show()
    app.exec_()
    app.deleteLater()
    sys.exit()