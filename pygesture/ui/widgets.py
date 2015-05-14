import numpy as np

from sklearn.lda import LDA
from sklearn import cross_validation

from PyQt4 import QtGui, QtCore
import pyqtgraph as pg
import pyqtgraph.opengl as gl

from pygesture import filestruct
from pygesture import processing

from pygesture.ui.signal_widget_template import Ui_SignalWidget
from pygesture.ui.new_session_template import Ui_NewSessionDialog
from pygesture.ui.recording_viewer_template import Ui_RecordingViewerWidget
from pygesture.ui.process_widget_template import Ui_ProcessWidget


class GestureView(QtGui.QLabel):
    """
    A trivial extension of QLabel so we can connect to resizeEvent.
    """

    resize_signal = QtCore.pyqtSignal(QtGui.QResizeEvent)

    def __init__(self, parent=None):
        QtGui.QLabel.__init__(self, parent)

    def resizeEvent(self, event=None):
        self.resize_signal.emit(event)


class PromptWidget(QtGui.QWidget):

    HEIGHT = 40
    REST_COLOR = QtGui.QColor(90, 90, 90)
    CONTRACT_COLOR = QtGui.QColor(150, 80, 80, 150)

    def __init__(self, parent=None):
        super(PromptWidget, self).__init__()
        self.setFixedHeight(PromptWidget.HEIGHT)
        self.value = 0
        self._ticks = 1
        self.update_tick_labels()
        self._transitions = (0, 1)

        self.tick_font = QtGui.QFont('Serif', 7, QtGui.QFont.Light)
        self.prompt_font = QtGui.QFont('Serif', 10, QtGui.QFont.Light)

    @property
    def ticks(self):
        return self._ticks

    @ticks.setter
    def ticks(self, value):
        self._ticks = value
        self.update_tick_labels()
        self.repaint()

    @property
    def transitions(self):
        return self._transitions

    @transitions.setter
    def transitions(self, value):
        self._transitions = value
        self.repaint()

    def setProgress(self, value):
        self.value = value
        self.repaint()

    def getProgress(self):
        return self.value

    def update_tick_labels(self):
        self.tick_labels = [str(i) for i in range(1, int(self._ticks))]

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.draw(qp)
        qp.end()

    def draw(self, qp):

        w = self.size().width()
        h = self.size().height()

        tick_step = int(round(w / self._ticks))

        till = int(((w / float(self._ticks*1000)) * self.value))
        f1 = int(((w / float(self._ticks*1000)) * self._transitions[0]*1000))
        f2 = int(((w / float(self._ticks*1000)) * self._transitions[1]*1000))

        qp.setPen(PromptWidget.REST_COLOR)
        qp.setBrush(PromptWidget.REST_COLOR)
        qp.drawRect(0, 0, till, h)

        qp.setPen(PromptWidget.CONTRACT_COLOR)
        qp.setBrush(PromptWidget.CONTRACT_COLOR)
        qp.drawRect(f1, 0, f2-f1, h)

        pen = QtGui.QPen(QtGui.QColor(20, 20, 20), 1, QtCore.Qt.SolidLine)

        qp.setPen(pen)
        qp.setBrush(QtCore.Qt.NoBrush)
        qp.drawRect(0, 0, w-1, h-1)

        qp.setFont(self.prompt_font)
        for t, l in zip(self._transitions, ['contract', 'rest']):
            x = int(((w / float(self._ticks*1000)) * (t*1000.)))
            metrics = qp.fontMetrics()
            fw = metrics.width(l)
            qp.drawText(x-fw/2, h/2, l)

        qp.setFont(self.tick_font)
        j = 0
        for i in range(tick_step, self._ticks*tick_step, tick_step):
            qp.drawLine(i, h-5, i, h)
            metrics = qp.fontMetrics()
            fw = metrics.width(self.tick_labels[j])
            qp.drawText(i-fw/2, h-7, self.tick_labels[j])
            j += 1

    value_prop = QtCore.pyqtProperty(float, getProgress, setProgress)


class BoostsWidget(QtGui.QWidget):

    updated = QtCore.pyqtSignal(dict)

    def __init__(self, parent=None):
        super(BoostsWidget, self).__init__(parent)

        self.spinboxes = dict()
        self.values = dict()
        self.form = QtGui.QFormLayout()
        self.setLayout(self.form)

    def set_mapping(self, labels, limits=(0, 1), init=0.5, step=0.1):
        # labels is a list of tuples [(int, str), (int, str)...]
        for num, text in labels:
            spinbox = QtGui.QDoubleSpinBox()
            spinbox.setRange(*limits)
            spinbox.setValue(init)
            spinbox.setSingleStep(step)
            spinbox.valueChanged.connect(self.spinbox_callback)

            self.spinboxes[num] = spinbox
            self.values[num] = init

            self.form.addRow(text, spinbox)

    def spinbox_callback(self, value):
        for label, box in self.spinboxes.items():
            self.values[label] = box.value()

        self.updated.emit(self.values)

    def set_values(self, values):
        for label, box in self.spinboxes.items():
            box.setValue(values[label])


class NewSessionDialog(QtGui.QDialog):

    def __init__(self, parent=None):
        super(NewSessionDialog, self).__init__(parent)

        self.ui = Ui_NewSessionDialog()
        self.ui.setupUi(self)

    def get_data(self):
        data = {
            'pid': str(self.ui.participantLineEdit.text()),
            'sid': str(self.ui.sessionLineEdit.text())
        }
        return data


class SignalWidget(QtGui.QWidget):

    def __init__(self, config, record_thread, parent=None):
        super(SignalWidget, self).__init__(parent)

        self.cfg = config
        self.record_thread = record_thread

        self.samp_per_read = 1
        self.plot_items = []
        self.plot_data_items = []

        self.ui = Ui_SignalWidget()
        self.ui.setupUi(self)

        self.init_plot()
        self.init_button_group()

    def showEvent(self, event):
        self.record_thread.set_continuous()
        self.record_thread.update_sig.connect(self.update_plot)
        self.set_mode_callback()

    def hideEvent(self, event):
        try:
            self.record_thread.update_sig.disconnect(self.update_plot)
        except TypeError:
            # thrown if the signal isn't connected yet
            pass

        self.record_thread.kill()

    def init_plot(self):
        self.ui.plotWidget.setBackground(None)

    def init_button_group(self):
        self.ui.probeButton.clicked.connect(self.set_mode_callback)
        self.ui.signalButton.clicked.connect(self.set_mode_callback)
        self.set_mode_callback()

    def set_mode_callback(self):
        if self.record_thread.running:
            self.record_thread.kill()
        probe_mode = self.ui.probeButton.isChecked()
        if probe_mode:
            self.n_channels = 1
            self.cfg.daq.set_channel_range(
                (self.cfg.probe_channel, self.cfg.probe_channel))
        else:
            self.n_channels = len(self.cfg.channels)
            self.cfg.daq.set_channel_range(
                (min(self.cfg.channels), max(self.cfg.channels)))

        self.update_num_channels()
        self.record_thread.start()

    def update_num_channels(self):
        self.ui.plotWidget.clear()

        self.plot_items = []
        self.plot_data_items = []
        for i in range(self.n_channels):
            plot_item = self.ui.plotWidget.addPlot(row=i, col=0)
            plot_data_item = plot_item.plot(
                pen=(i, self.n_channels), antialias=True)

            plot_item.showAxis('bottom', False)
            plot_item.showGrid(y=True, alpha=0.5)
            plot_item.setMouseEnabled(x=False)

            if self.n_channels > 1:
                ch = self.cfg.channels[i]
                label = "%s/%s" % (
                    self.cfg.arm_sensors[ch][0], self.cfg.leg_sensors[ch][0])
                plot_item.setLabels(left=label)

            if i > 0:
                plot_item.setYLink(self.plot_items[0])

            self.plot_items.append(plot_item)
            self.plot_data_items.append(plot_data_item)

    def update_plot(self, data):
        n_channels, spr = data.shape
        if self.n_channels != n_channels:
            return

        if spr != self.samp_per_read:
            self.samp_per_read = spr

        for i in range(self.n_channels):
            self.plot_data_items[i].setData(data[i, :])


class RecordingViewerWidget(QtGui.QWidget):

    def __init__(self, config, parent=None):
        super(RecordingViewerWidget, self).__init__(parent)

        self.cfg = config

        self.ui = Ui_RecordingViewerWidget()
        self.ui.setupUi(self)

        self.init_plot()
        self.init_buttons()

        self.ui.sessionList.currentTextChanged.connect(
            self.sid_selection_callback)

    def init_plot(self):
        self.ui.plotWidget.setBackground(None)

    def init_buttons(self):
        self.ui.nextButton.clicked.connect(self.next_plot_callback)
        self.ui.previousButton.clicked.connect(self.prev_plot_callback)

    def set_pid(self, pid):
        self.pid = pid
        self.ui.sessionList.clear()
        self.sid_list = filestruct.get_session_list(
            self.cfg.data_path, self.pid)

        for sid in self.sid_list:
            QtGui.QListWidgetItem(sid, self.ui.sessionList)

    def sid_selection_callback(self, sid):
        sid = str(sid)
        session = processing.Session(self.cfg.data_path, self.pid, sid, None)
        self.data_list = []
        for f in session.recording_file_list:
            rec = processing.Recording(f, self.cfg.post_processor)
            n_samples, n_channels = rec.raw_data.shape
            rate = rec.fs_raw
            t = np.arange(0, n_samples/rate, 1/float(rate))
            data = rec.raw_data
            self.data_list.append(
                (t, data, rec.trial_number, rec.label))

        self.trial_index = 0
        self.update_num_channels(self.data_list[0][1].shape[1])
        self.set_data(self.data_list[0])

    def next_plot_callback(self):
        self.trial_index += 1
        if self.trial_index == len(self.data_list):
            self.trial_index = 0

        self.set_data(self.data_list[self.trial_index])

    def prev_plot_callback(self):
        self.trial_index -= 1
        if self.trial_index < 0:
            self.trial_index = len(self.data_list) - 1

        self.set_data(self.data_list[self.trial_index])

    def update_num_channels(self, num_channels):
        self.ui.plotWidget.clear()

        self.plot_items = []
        self.plot_data_items = []
        for i in range(num_channels):
            plot_item = self.ui.plotWidget.addPlot(row=i, col=0)
            plot_data_item = plot_item.plot(
                pen=(i, num_channels), antialias=True)

            plot_item.showAxis('bottom', False)
            plot_item.showGrid(y=True, alpha=0.5)
            plot_item.setYRange(-1, 1)
            plot_item.setMouseEnabled(x=False)

            if i > 0:
                plot_item.setYLink(self.plot_items[0])

            self.plot_items.append(plot_item)
            self.plot_data_items.append(plot_data_item)

    def set_data(self, data):
        t, signals, trial, label = data
        self.ui.titleLabel.setText("Trial %d, Label %s" % (trial, label))
        for i, item in enumerate(self.plot_data_items):
            item.setData(t, signals[:, i])


class ProcessWidget(QtGui.QWidget):

    def __init__(self, config, parent=None):
        super(ProcessWidget, self).__init__(parent)

        self.cfg = config
        self.plot_items = []

        self.ui = Ui_ProcessWidget()
        self.ui.setupUi(self)

        self.init_plot()
        self.init_layout()

        self.ui.processButton.clicked.connect(self.process_button_callback)
        self.ui.sessionList.currentTextChanged.connect(
            self.sid_selection_callback)

    def init_plot(self):
        self.plotWidget = gl.GLViewWidget()
        g = gl.GLGridItem()
        self.plotWidget.addItem(g)

    def init_layout(self):
        self.ui.verticalLayout.addWidget(self.plotWidget)

    def set_pid(self, pid):
        self.pid = pid
        self.ui.sessionList.clear()
        self.sid_list = filestruct.get_session_list(
            self.cfg.data_path, self.pid)

        for sid in self.sid_list:
            QtGui.QListWidgetItem(sid, self.ui.sessionList)

    def sid_selection_callback(self, sid):
        self.sid = str(sid)
        self.ui.processButton.setEnabled(True)
        try:
            f = filestruct.find_feature_file(
                self.cfg.data_path, self.pid, self.sid)
            data = processing.read_feature_file_list([f])
            self.plot_data(*data)
        except:
            # couldn't find feature file
            self.clear_plot()
            return

    def process_button_callback(self):
        session = processing.Session(
            self.cfg.data_path, self.pid, self.sid, self.cfg.post_processor)
        self.processor_thread = SessionProcessorThread(session)
        self.processor_thread.finished.connect(self.process_finished_callback)
        self.ui.progressBar.setRange(0, 0)
        self.ui.processButton.setEnabled(False)
        self.original_button_text = self.ui.processButton.text()
        self.ui.processButton.setText("Processing...")
        self.processor_thread.start()

    def process_finished_callback(self):
        self.ui.progressBar.setRange(0, 1)
        self.ui.progressBar.setValue(1)
        self.ui.processButton.setEnabled(True)
        self.ui.processButton.setText(self.original_button_text)
        self.sid_selection_callback(self.sid)

    def plot_data(self, X, y):
        self.clear_plot()

        # get the simple cross validation score
        clf = LDA()
        scores = cross_validation.cross_val_score(clf, X, y, cv=5)
        score = np.mean(scores)
        self.ui.titleLabel.setText("Accuracy: %.2f" % score)

        # project the data to 3D for visualization
        clf = LDA(n_components=3)
        X_proj = clf.fit(X, y).transform(X)

        labels = sorted(np.unique(y))
        for i in labels:
            plot = gl.GLScatterPlotItem(
                pos=X_proj[y == i], color=pg.glColor(pg.intColor(i)))
            self.plotWidget.addItem(plot)
            self.plot_items.append(plot)

    def clear_plot(self):
        for item in self.plot_items:
            self.plotWidget.removeItem(item)
        self.plot_items = []
        self.ui.titleLabel.setText("Process to View Data")


class SessionProcessorThread(QtCore.QThread):

    finished = QtCore.pyqtSignal()

    def __init__(self, session):
        super(SessionProcessorThread, self).__init__()
        self.session = session

    def run(self):
        self.session.process()

        self.finished.emit()
