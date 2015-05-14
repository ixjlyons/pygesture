import pkg_resources

from pygesture import recorder

from PyQt4 import QtGui, QtCore

from pygesture.ui.train_widget_template import Ui_TrainWidget


class TrainWidget(QtGui.QWidget):

    def __init__(self, config, record_thread, parent=None):
        super(TrainWidget, self).__init__(parent)
        self.cfg = config
        self.record_thread = record_thread

        self.ui = Ui_TrainWidget()
        self.ui.setupUi(self)

        self.running = False

        self.init_record_thread()
        self.init_gesture_view()
        self.init_gesture_prompt()
        self.init_session_progressbar()
        self.init_buttons()
        self.init_intertrial_timer()

    def init_record_thread(self):
        tpr = self.cfg.trial_duration * \
            int(self.cfg.daq.rate / self.cfg.daq.samples_per_read)
        self.record_thread.set_fixed(triggers_per_record=tpr)
        self.record_thread.finished_sig.connect(self.record_finished)

    def init_gesture_view(self):
        self.gesture_images = dict()
        for (key, val) in self.cfg.arm_gestures.items():
            imgpath = pkg_resources.resource_filename(
                __name__, 'images/'+val[1]+'.png')
            img = QtGui.QPixmap(imgpath)
            self.gesture_images[key] = img

        self.ui.gestureView.resize_signal.connect(self.update_gesture_view)

    def update_gesture_view(self, event=None, imgkey=0):
        w = self.ui.gestureView.width()
        h = self.ui.gestureView.height()

        self.ui.gestureView.setPixmap(self.gesture_images[imgkey].scaled(
            w, h, QtCore.Qt.KeepAspectRatio))

    def init_gesture_prompt(self):
        self.ui.promptWidget.ticks = self.cfg.trial_duration
        self.ui.promptWidget.transitions = self.cfg.prompt_times
        self.prompt_anim = QtCore.QPropertyAnimation(
            self.ui.promptWidget, 'value_prop')
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

    def start_session(self):
        self.session = recorder.Session(
            self.cfg.data_path, list(self.cfg.arm_gestures),
            self.cfg.num_repeats)
        pid = self.ui.participantLineEdit.text()
        sid = self.ui.sessionLineEdit.text()
        if pid == '' or sid == '':
            message = QtGui.QMessageBox().critical(
                self, "Error", "Input session info before starting.")
            return

        try:
            self.session.set_ids(pid, sid)
        except IOError:
            message = QtGui.QMessageBox().warning(
                self,
                "Warning",
                "Session directory already exists.\nOverwrite?",
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.Cancel)

            if message == QtGui.QMessageBox.Cancel:
                return
            elif message == QtGui.QMessageBox.Yes:
                self.session.overwrite_session()

        self.running = True
        self.ui.startButton.setEnabled(False)
        self.ui.sessionInfoBox.setEnabled(False)
        self.start_recording()

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
        else:
            self.running = True
            self.start_recording()
            self.ui.pauseButton.setText('Pause')

    def finish_session(self):
        self.running = False
        self.ui.startButton.setEnabled(True)
        self.ui.sessionInfoBox.setEnabled(True)
