import numpy as np

from PyQt4 import QtGui
from pygesture.ui.signal_dialog_template import Ui_SignalDialog
from pygesture.ui.signal_widget import Ui_SignalWidget


class SignalWidget(QtGui.QWidget):

    def __init__(self, config, record_thread, parent=None):
        super(SignalWidget, self).__init__(parent)

        self.cfg = config
        self.record_thread = record_thread

        self.samp_per_read = 1
        self.spacer = 0.5

        self.ui = Ui_SignalWidget()
        self.ui.setupUi(self)

        self.init_plot()
        self.init_button_group()

    def showEvent(self, event):
        self.record_thread.set_continuous()
        self.record_thread.update_sig.connect(self.update_plot)
        self.set_mode_callback()

    def hideEvent(self, event):
        self.record_thread.update_sig.disconnect(self.update_plot)
        self.record_thread.kill()

    def init_button_group(self):
        self.ui.probeButton.clicked.connect(self.set_mode_callback)
        self.ui.signalButton.clicked.connect(self.set_mode_callback)
        self.set_mode_callback()

    def init_plot(self):
        self.ui.plotWidget.setBackground(None)
        self.ui.plotWidget.setMouseEnabled(x=False, y=False)
        self.plotItem = self.ui.plotWidget.getPlotItem()
        self.plotItem.showAxis('bottom', False)
        self.plotItem.showAxis('left', False)

    def set_mode_callback(self):
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
        self.line_list = [
            self.ui.plotWidget.plot(
                pen={'color': '555'}) for i in range(self.n_channels)
        ]

        self.plot_list = [
            self.ui.plotWidget.plot(
                pen=(i, self.n_channels)) for i in range(self.n_channels)
        ]

    def update_plot(self, data):
        n_channels, spr = data.shape
        if self.n_channels != n_channels:
            return

        if spr != self.samp_per_read:
            self.samp_per_read = spr

        for i in range(self.n_channels):
            # "grid" line for each signal
            self.line_list[i].setData(
                [0, data.shape[1]-1], 2*[-i*self.spacer])
            self.plot_list[i].setData(data[i, :] - i*self.spacer)


class SignalDialog(QtGui.QDialog):

    def __init__(self, n_channels, parent=None):
        super(SignalDialog, self).__init__()
        self.n_channels = n_channels
        self.samp_per_read = 1
        self.spacer = 0.5
        self.hist = 1

        self.ui = Ui_SignalDialog()
        self.ui.setupUi(self)

        self.init_buttons()
        self.init_plot()
        self._update_hist()

    def init_buttons(self):
        self.ui.vPlusButton.clicked.connect(self.v_plus_callback)
        self.ui.vMinusButton.clicked.connect(self.v_minus_callback)
        self.ui.hPlusButton.clicked.connect(self.h_plus_callback)
        self.ui.hMinusButton.clicked.connect(self.h_minus_callback)

    def init_plot(self):
        self.ui.plotWidget.setMouseEnabled(x=False, y=False)
        self.plotItem = self.ui.plotWidget.getPlotItem()
        self.plotItem.showAxis('bottom', False)
        self.plotItem.showAxis('left', False)

        self.line_list = [
            self.ui.plotWidget.plot(
                pen={'color': '555'}) for i in range(self.n_channels)
        ]

        self.plot_list = [
            self.ui.plotWidget.plot(
                pen=(i, self.n_channels)) for i in range(self.n_channels)
        ]

    def v_plus_callback(self):
        self.spacer -= 0.1
        if self.spacer < 0:
            self.spacer = 0

    def v_minus_callback(self):
        self.spacer += 0.1

    def h_plus_callback(self):
        self.hist -= 1
        if self.hist < 1:
            self.hist = 1
        self._update_hist()

    def h_minus_callback(self):
        self.hist += 1
        self._update_hist()

    def _update_hist(self):
        self.data = np.zeros((self.n_channels, self.hist*self.samp_per_read))

    def update_plot(self, data):
        spr = data.shape[1]
        if spr != self.samp_per_read:
            self.samp_per_read = spr
            self._update_hist()

        # shift values backward along horizontal axis
        self.data = np.roll(self.data, -self.samp_per_read, axis=1)
        self.data[:, -self.samp_per_read:] = data

        for i in range(self.n_channels):
            # "grid" line for each signal
            self.line_list[i].setData(
                [0, self.data.shape[1]-1], 2*[-i*self.spacer])
            self.plot_list[i].setData(self.data[i, :] - i*self.spacer)
