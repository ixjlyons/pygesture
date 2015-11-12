import numpy as np

from sklearn import cross_validation

from pygesture import filestruct
from pygesture import pipeline
from pygesture.analysis import processing

from pygesture.ui.qt import QtCore, QtWidgets
from .templates.signal_widget_template import Ui_SignalWidget
from .templates.recording_viewer_template import Ui_RecordingViewerWidget
from .templates.process_widget_template import Ui_ProcessWidget

import pyqtgraph as pg
try:
    import pyqtgraph.opengl as gl
    USE_GL = True
except:
    USE_GL = False
    pass


class SignalWidget(QtWidgets.QWidget):
    """
    A composite widget for displaying real-time signals.

    Single and multi-channel data is supported. A single signal is shown in
    "probe mode." A radio group allows switching between single and
    multi-channel modes. The widget is self-encompassing in that it doesn't
    need external input aside from a `pygesture.ui.recorder.RecordThread` for
    receiving data.
    """

    def __init__(self, config, record_thread, parent=None):
        super(SignalWidget, self).__init__(parent)

        self.cfg = config
        self.record_thread = record_thread

        self.samp_per_read = 1
        self.hist = 20
        self.plot_items = []
        self.plot_data_items = []

        self.ui = Ui_SignalWidget()
        self.ui.setupUi(self)

        self.pipeline = pipeline.Pipeline(self.cfg.conditioner)

        self.init_plot()
        self.init_button_group()

    def showEvent(self, event):
        self.init_record_thread()
        self.set_mode_callback()

    def hideEvent(self, event):
        self.dispose_record_thread()

    def init_record_thread(self):
        self.record_thread.set_continuous()
        self.record_thread.set_pipeline(self.pipeline)
        self.record_thread.prediction_sig.connect(self.update_plot)

    def dispose_record_thread(self):
        self.record_thread.prediction_sig.disconnect(self.update_plot)
        self.record_thread.pipeline = None
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
        self.cfg.conditioner.clear()

        self.plot_items = []
        self.plot_data_items = []
        pen = MultiPen(self.n_channels)
        for i in range(self.n_channels):
            plot_item = self.ui.plotWidget.addPlot(row=i, col=0)
            plot_data_item = plot_item.plot(pen=pen.get_pen(i), antialias=True)

            plot_item.showAxis('bottom', False)
            plot_item.showGrid(y=True, alpha=0.5)
            plot_item.setMouseEnabled(x=False)

            if self.n_channels > 1:
                ch = self.cfg.channels[i]
                label = "%s" % (self.cfg.sensors[ch].name)
                plot_item.setLabels(left=label)

            if i > 0:
                plot_item.setYLink(self.plot_items[0])

            self.plot_items.append(plot_item)
            self.plot_data_items.append(plot_data_item)

        self.plot_items[0].disableAutoRange(pg.ViewBox.YAxis)
        self.plot_items[0].setYRange(-1, 1)

        self.buf = np.zeros((self.n_channels, self.hist*self.samp_per_read))

    def update_plot(self, data):
        data = data.T
        n_channels, spr = data.shape
        if self.n_channels != n_channels:
            return

        if spr != self.samp_per_read:
            self.samp_per_read = spr
            self.buf = np.zeros((n_channels, self.hist*spr))

        self.buf[:, 0:(self.hist-1)*spr] = self.buf[:, spr:]
        self.buf[:, (self.hist-1)*spr:] = data

        for i in range(self.n_channels):
            self.plot_data_items[i].setData(self.buf[i, :])


class MultiPen(object):

    MIN_HUE = 160
    HUE_INC = 20
    VAL = 200

    def __init__(self, n_colors):
        self.n_colors = n_colors
        self.max_hue = self.MIN_HUE + n_colors*self.HUE_INC

    def get_pen(self, index):
        return pg.intColor(
            index, hues=self.n_colors,
            minHue=self.MIN_HUE, maxHue=self.max_hue,
            minValue=self.VAL, maxValue=self.VAL)


class RecordingViewerWidget(QtWidgets.QWidget):
    """
    A widget for viewing EMG recording files.
    """

    def __init__(self, config, parent=None):
        super(RecordingViewerWidget, self).__init__(parent)

        self.cfg = config

        self.ui = Ui_RecordingViewerWidget()
        self.ui.setupUi(self)

        self.data_list = []

        self.init_plot()
        self.init_buttons()
        self.init_browser()

    def init_plot(self):
        self.ui.plotWidget.setBackground(None)

    def init_buttons(self):
        self.ui.nextButton.clicked.connect(self.next_plot_callback)
        self.ui.previousButton.clicked.connect(self.prev_plot_callback)
        self.ui.conditionedCheckBox.stateChanged.connect(
            self.condition_callback)
        self.condition = \
            self.ui.conditionedCheckBox.checkState() == QtCore.Qt.Checked

    def init_browser(self):
        self.ui.sessionBrowser.participant_selected.connect(
            self.on_participant_selected)
        self.ui.sessionBrowser.session_selected.connect(
            self.on_session_selected)
        self.ui.sessionBrowser.set_session_filter("train")
        self.ui.sessionBrowser.set_data_path(self.cfg.data_path)

    def on_participant_selected(self, pid):
        self.pid = pid

    def on_session_selected(self, sid):
        self.sid = sid
        session = processing.Session(self.cfg.data_path, self.pid, sid, None)
        file_list = filestruct.get_recording_file_list(session.rawdir)

        if not file_list:
            return

        self.data_list = []
        for f in file_list:
            rec = processing.Recording(f, self.cfg.post_processor)
            data = rec.raw_data

            if self.condition:
                self.cfg.conditioner.clear()
                data = self.cfg.conditioner.process(data)

            n_samples, n_channels = rec.raw_data.shape
            rate = rec.fs_raw
            t = np.arange(0, n_samples/rate, 1/float(rate))
            self.data_list.append(
                (t, data, rec.trial_number, rec.label))

        self.trial_index = 0
        self.update_num_channels(self.data_list[0][1].shape[1])
        self.set_data(self.data_list[0])

    def next_plot_callback(self):
        if len(self.data_list) == 0:
            return

        self.trial_index += 1
        if self.trial_index == len(self.data_list):
            self.trial_index = 0

        self.set_data(self.data_list[self.trial_index])

    def prev_plot_callback(self):
        if len(self.data_list) == 0:
            return

        self.trial_index -= 1
        if self.trial_index < 0:
            self.trial_index = len(self.data_list) - 1

        self.set_data(self.data_list[self.trial_index])

    def condition_callback(self, state):
        if state == QtCore.Qt.Checked:
            self.condition = True
        else:
            self.condition = False

        if self.sid is not None:
            self.on_session_selected(self.sid)

    def update_num_channels(self, num_channels):
        self.ui.plotWidget.clear()

        self.plot_items = []
        self.plot_data_items = []
        pen = MultiPen(num_channels)
        for i in range(num_channels):
            plot_item = self.ui.plotWidget.addPlot(row=i, col=0)
            plot_data_item = plot_item.plot(pen=pen.get_pen(i), antialias=True)

            # plot_item.showAxis('bottom', False)
            plot_item.showGrid(y=True, alpha=0.5)
            plot_item.setYRange(-0.2, 0.2)
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


class ProcessWidget(QtWidgets.QWidget):

    def __init__(self, config, parent=None):
        super(ProcessWidget, self).__init__(parent)

        self.cfg = config
        self.plot_items = []

        self.ui = Ui_ProcessWidget()
        self.ui.setupUi(self)

        self.init_plot()
        self.init_layout()
        self.init_browser()

        self.ui.processButton.clicked.connect(self.process_button_callback)

    def init_plot(self):
        if USE_GL:
            self.plotWidget = gl.GLViewWidget()
            g = gl.GLGridItem()
            self.plotWidget.addItem(g)
        else:
            self.plotWidget = pg.PlotWidget()

    def init_layout(self):
        self.ui.verticalLayout.addWidget(self.plotWidget)

    def init_browser(self):
        self.ui.sessionBrowser.participant_selected.connect(
            self.on_participant_selected)
        self.ui.sessionBrowser.session_selected.connect(
            self.on_session_selected)
        self.ui.sessionBrowser.set_session_filter("train")
        self.ui.sessionBrowser.set_data_path(self.cfg.data_path)

    def on_participant_selected(self, pid):
        self.pid = pid

    def on_session_selected(self, sid):
        self.sid = sid
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
        self.on_session_selected(self.sid)

    def plot_data(self, X, y):
        self.clear_plot()

        # get the simple cross validation score
        clf = self.cfg.learner.clf
        scores = cross_validation.cross_val_score(clf, X, y, cv=5)
        score = np.mean(scores)
        self.ui.titleLabel.setText("Accuracy: %.2f" % score)

        # project the data for visualization
        X_proj = clf.fit(X, y).transform(X)

        labels = sorted(np.unique(y))
        for i in labels:
            if USE_GL:
                plot = gl.GLScatterPlotItem(
                    pos=X_proj[y == i, :3], color=pg.glColor(pg.intColor(i)))
            else:
                plot = pg.ScatterPlotItem(
                    pos=X_proj[y == i, :2],
                    brush=pg.mkBrush(pg.intColor(i)))
            self.plotWidget.addItem(plot)
            self.plot_items.append(plot)

    def clear_plot(self):
        for item in self.plot_items:
            self.plotWidget.removeItem(item)
        self.plot_items = []
        self.ui.titleLabel.setText("Process to View Data")


class SessionProcessorThread(QtCore.QThread):
    """
    Simple thread for processing a pygesture.processing.Session object.
    """

    finished = QtCore.pyqtSignal()

    def __init__(self, session):
        super(SessionProcessorThread, self).__init__()
        self.session = session

    def run(self):
        self.session.process()

        self.finished.emit()


class TaskTabDesc(object):

    def __init__(self, name, cls):
        self.name = name
        self.cls = cls
