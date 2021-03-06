import os
import pkg_resources

from pygesture import filestruct
from pygesture import wav
from pygesture import experiment

from pygesture.ui.qt import QtGui, QtCore, QtWidgets
from pygesture.ui.templates.train_widget_template import Ui_TrainWidget


class TrainWidget(QtWidgets.QWidget):

    session_started = QtCore.pyqtSignal()
    session_paused = QtCore.pyqtSignal()
    session_resumed = QtCore.pyqtSignal()
    session_finished = QtCore.pyqtSignal()

    def __init__(self, config, record_thread, base_session, parent=None):
        super(TrainWidget, self).__init__(parent)
        self.cfg = config
        self.record_thread = record_thread
        self.base_session = base_session

        self.ui = Ui_TrainWidget()
        self.ui.setupUi(self)

        self.running = False

        self.init_session()
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
        tpr = int(self.cfg.trial_duration /
                  (self.cfg.daq.samples_per_read / (self.cfg.daq.rate/1000)))
        self.cfg.daq.set_channel_range(
            (min(self.cfg.channels), max(self.cfg.channels)))
        self.record_thread.set_fixed(triggers_per_record=tpr)
        self.record_thread.ready_sig.connect(self.on_recorder_ready)
        self.record_thread.finished_sig.connect(self.record_finished)
        self.record_thread.error_sig.connect(self.on_record_error)

    def dispose_record_thread(self):
        try:
            self.record_thread.finished_sig.disconnect(self.record_finished)
            self.record_thread.ready_sig.disconnect(self.on_recorder_ready)
            self.record_thread.error_sig.disconnect(self.on_record_error)
        except TypeError:
            pass
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

    def update_gesture_view(self, imgkey=0):
        self.ui.gestureView.setPixmap(self.gesture_images[imgkey])

    def init_gesture_prompt(self):
        self.ui.promptWidget.ticks = int(self.cfg.trial_duration/1000)
        self.ui.promptWidget.transitions = self.cfg.prompt_times
        self.ui.promptWidget.setMaximum(self.cfg.trial_duration)
        self.prompt_anim = QtCore.QPropertyAnimation(
            self.ui.promptWidget, b'value')
        self.prompt_anim.setDuration(self.cfg.trial_duration)
        self.prompt_anim.setStartValue(0)
        self.prompt_anim.setEndValue(self.cfg.trial_duration)

    def init_session_progressbar(self):
        self.ui.sessionProgressBar.setMinimum(0)
        self.ui.sessionProgressBar.setMaximum(
            self.cfg.num_repeats*len(self.cfg.gestures))
        self.ui.sessionProgressBar.setValue(0)

    def init_buttons(self):
        self.ui.startButton.clicked.connect(self.on_start_clicked)
        self.ui.pauseButton.clicked.connect(self.on_pause_clicked)
        self.ui.redoButton.clicked.connect(self.on_redo_clicked)

    def init_intertrial_timer(self):
        self.intertrial_timer = QtCore.QTimer(self)
        self.intertrial_timer.setSingleShot(True)
        self.intertrial_timer.timeout.connect(self.start_recording)

    def init_session(self):
        self.session = Session(
            self.base_session,
            [g.label for g in self.cfg.gestures],
            self.cfg.num_repeats)

        self.lefty = True if self.base_session.hand == 'left' else False

    def on_start_clicked(self):
        self.start_session()

    def on_pause_clicked(self):
        if self.running:
            self.pause_session()
        else:
            self.resume_session()

    def on_redo_clicked(self):
        if self.running:
            self.pause_session()
        self.session.redo_trial()
        self.resume_session()

    def start_session(self):
        self.running = True
        self.ui.startButton.setEnabled(False)
        self.ui.pauseButton.setEnabled(True)
        self.start_recording()
        self.session_started.emit()

    def start_recording(self):
        self.record_thread.start()

    def on_recorder_ready(self):
        trial, gesture = self.session.start_trial()
        self.prompt_anim.start()
        self.update_gesture_view(imgkey=gesture)
        self.ui.sessionProgressBar.setValue(trial)
        self.ui.redoButton.setEnabled(False)

    def on_record_error(self):
        self.on_pause_clicked()
        QtWidgets.QMessageBox().critical(
            self, "Error",
            "DAQ failure.",
            QtWidgets.QMessageBox.Ok)

    def record_finished(self, data):
        self.session.write_recording(data, self.cfg.daq.rate)
        self.session.finish_trial()

        self.update_gesture_view()

        if self.session.finished:
            self.finish_session()
            return

        if self.running:
            self.intertrial_timer.start(1000*self.cfg.inter_trial_timeout)

        self.ui.redoButton.setEnabled(True)

    def pause_session(self):
        if self.intertrial_timer.isActive():
            self.intertrial_timer.stop()
        if self.record_thread.running:
            self.record_thread.kill()
        self.prompt_anim.stop()
        self.ui.promptWidget.reset()
        self.update_gesture_view()
        self.running = False
        self.ui.pauseButton.setText('Resume')
        self.session_paused.emit()

    def resume_session(self):
        self.running = True
        self.start_recording()
        self.ui.pauseButton.setText('Pause')
        self.session_resumed.emit()

    def finish_session(self):
        self.running = False
        self.session_finished.emit()


class Session(object):

    def __init__(self, session, labels, n_repeat):
        self.parent_session = session

        self.gesture_order = experiment.generate_trials(
            labels, n_repeat=n_repeat)
        self.num_trials = len(self.gesture_order)
        self.current_trial = 1
        self.finished = False

        self.init_file_structure()

    def init_file_structure(self):
        self.recording_dir = filestruct.get_recording_dir(
            self.parent_session.session_dir)
        os.makedirs(self.recording_dir)

    def start_trial(self):
        self.current_gesture = self.gesture_order[self.current_trial-1]
        return (self.current_trial, self.current_gesture)

    def redo_trial(self):
        self.current_trial -= 1
        self.update_finished()

    def finish_trial(self):
        self.current_trial += 1
        self.update_finished()

    def update_finished(self):
        self.finished = self.current_trial > self.num_trials

    def write_recording(self, data, fs):
        rec_file = filestruct.get_recording_file(
            self.recording_dir,
            self.parent_session.pid,
            self.parent_session.sid,
            self.parent_session.datestr,
            self.current_trial,
            self.current_gesture)

        wav.write(rec_file, fs, data.T)
