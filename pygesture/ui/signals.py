import numpy as np
import pyqtgraph
pyqtgraph.setConfigOption('background', '#282828')

from PyQt4 import QtGui
from pygesture.ui.signal_dialog_template import Ui_SignalDialog


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
