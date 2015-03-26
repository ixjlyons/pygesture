from PyQt4 import QtGui
import pyqtgraph


class SignalCheckWindow(QtGui.QDialog):

    def __init__(self, n_channels, parent=None):
        super(SignalCheckWindow, self).__init__()
        self.n_channels = n_channels
        self.spacer = 0.5

        self.create_plot()
        self.create_button_box()

        self.layout = QtGui.QHBoxLayout()
        self.layout.addWidget(self.plot_widget)
        self.layout.addLayout(self.button_box)

        self.setLayout(self.layout)
        self.setWindowTitle("signal check")

    def create_plot(self):
        self.plot_widget = pyqtgraph.PlotWidget(name='Signal Check')
        self.plot_list = [self.plot_widget.plot(pen=(i, self.n_channels))
                          for i in range(self.n_channels)]
        # p = self.plot_widget.getPlotItem()
        self.plot_widget.getPlotItem().showAxis('bottom', False)
        self.plot_widget.getPlotItem().showAxis('left', False)

    def create_button_box(self):
        self.button_box = QtGui.QVBoxLayout()
        self.contract_button = QtGui.QPushButton("+")
        self.contract_button.setFixedSize(50, 50)
        self.expand_button = QtGui.QPushButton("-")
        self.expand_button.setFixedSize(50, 50)
        self.button_box.addWidget(self.contract_button)
        self.button_box.addWidget(self.expand_button)
        self.button_box.setSpacing(0)

        self.expand_button.clicked.connect(self.zoom_out)
        self.contract_button.clicked.connect(self.zoom_in)

    def zoom_out(self):
        self.spacer += 0.1

    def zoom_in(self):
        self.spacer -= 0.1
        if self.spacer < 0:
            self.spacer = 0

    def update_plot(self, data):
        for i in range(self.n_channels):
            self.plot_list[i].setData(data[i, :] - i*self.spacer)


class SignalProbeWindow(QtGui.QDialog):

    def __init__(self, parent=None):
        super(SignalProbeWindow, self).__init__()
        self.lim = 1.0

        self.create_plot()
        self.create_button_box()

        self.layout = QtGui.QHBoxLayout()
        self.layout.addWidget(self.plot_widget)
        self.layout.addLayout(self.button_box)

        self.setLayout(self.layout)
        self.setWindowTitle("signal probe")

    def create_plot(self):
        self.plot_widget = pyqtgraph.PlotWidget(name='View Signal')
        self.plot = self.plot_widget.plot()
        self.plot_item = self.plot_widget.getPlotItem()
        self.plot_item.showAxis('bottom', False)
        self.plot_item.showGrid(x=True, y=True, alpha=0.8)
        self.plot_item.setYRange(-self.lim, self.lim)

    def create_button_box(self):
        self.button_box = QtGui.QVBoxLayout()
        self.contract_button = QtGui.QPushButton("+")
        self.contract_button.setFixedSize(50, 50)
        self.expand_button = QtGui.QPushButton("-")
        self.expand_button.setFixedSize(50, 50)
        self.button_box.addWidget(self.contract_button)
        self.button_box.addWidget(self.expand_button)
        self.button_box.setSpacing(0)

        self.expand_button.clicked.connect(self.zoom_out)
        self.contract_button.clicked.connect(self.zoom_in)

    def zoom_out(self):
        self.lim += 0.05
        self.update_lim()

    def zoom_in(self):
        self.lim -= 0.05
        if self.lim < 0.05:
            self.lim = 0.05
        self.update_lim()

    def update_lim(self):
        self.plot_item.setYRange(-self.lim, self.lim)

    def update_plot(self, data):
        self.plot.setData(data[0, :])
