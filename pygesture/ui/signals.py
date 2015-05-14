import numpy as np

from PyQt4 import QtGui
from pygesture.ui.signal_widget import Ui_SignalWidget


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
