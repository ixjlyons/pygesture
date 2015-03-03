#from PySide import QtGui, QtCore
from PyQt4 import QtGui, QtCore
qtbackend = 'PyQt4'

import matplotlib
matplotlib.rcParams['backend.qt4'] = qtbackend
from matplotlib.backends.backend_qt4agg \
    import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from pygesture import processing
from pygesture import classification


class SessionResultsDialog(QtGui.QDialog):

    def __init__(self, data_root, pid, arm_sid_list, leg_sid_list, arm_labels,
            leg_labels):
        super(SessionResultsDialog, self).__init__()

        self.data_root = data_root
        self.pid = pid
        self.arm_sid_list = arm_sid_list
        self.leg_sid_list = leg_sid_list
        self.arm_labels = arm_labels
        self.leg_labels = leg_labels

        self.progress_layout = QtGui.QVBoxLayout()
        self.progress_bar = QtGui.QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(0)
        self.progress_bar.setTextVisible(False)
        self.progress_layout.addWidget(self.progress_bar)

        self.layout = QtGui.QHBoxLayout()
        self.arm_plot = ConfusionMatrixWidget()
        self.leg_plot = ConfusionMatrixWidget()
        self.layout.addWidget(self.arm_plot)
        self.layout.addWidget(self.leg_plot)
        self.progress_layout.addLayout(self.layout)

        self.setLayout(self.progress_layout)
        self.setWindowTitle("session results")

        self.processor = SessionProcessor(self.data_root, self.pid, 
            self.arm_sid_list+self.leg_sid_list)
        self.processor.finished_sig.connect(self._show_plots)
        self.processor.start()

    def _show_plots(self):
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(100)

        clf_dict_arm = {
            'name': 'arm',
            'n_train': 2,
            'sid_list': self.arm_sid_list}
        clf_dict_leg = {
            'name': 'leg',
            'n_train': 2,
            'sid_list': self.leg_sid_list}

        cm_arm = classification.run_cv(self.data_root, [self.pid], clf_dict_arm,
            label_dict=self.arm_labels)
        cm_leg = classification.run_cv(self.data_root, [self.pid], clf_dict_leg,
            label_dict=self.leg_labels)
        self.arm_plot.plot(cm_arm)
        self.leg_plot.plot(cm_leg)


class ConfusionMatrixWidget(FigureCanvas):
    def __init__(self):
        super(ConfusionMatrixWidget, self).__init__(Figure())
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

    def plot(self, cm):
        cm.show(fig=self.figure)
        self.draw()


class SessionProcessor(QtCore.QThread):
    finished_sig = QtCore.Signal()

    def __init__(self, data_root, pid, sid_list, pools=6):
        QtCore.QThread.__init__(self, parent=None)
        self.data_root = data_root
        self.pid = pid
        self.sid_list = sid_list
        self.pools = pools

    def run(self):
        processing.batch_process(self.data_root, self.pid,
                                 sid_list=self.sid_list, pool=self.pools)
        self.finished_sig.emit()
