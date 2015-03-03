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
from pygesture import features
from pygesture import pipeline


class SessionResultsDialog(QtGui.QDialog):

    def __init__(self, pid, config):
        super(SessionResultsDialog, self).__init__()

        self.config = config
        self.pid = pid

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

        self.processor = SessionProcessor(
            config.data_path, self.pid, 
            config.results_sid_arm+config.results_sid_leg,
            config.post_processor)
        self.processor.finished_sig.connect(self._show_plots)
        self.processor.start()

    def _show_plots(self):
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(100)

        clf_dict_arm = {
            'name': 'arm',
            'n_train': 2,
            'sid_list': self.config.results_sid_arm}
        clf_dict_leg = {
            'name': 'leg',
            'n_train': 2,
            'sid_list': self.config.results_sid_leg}

        cm_arm = classification.run_cv(self.config.data_path, [self.pid],
                clf_dict_arm, label_dict=self.config.arm_gestures)
        cm_leg = classification.run_cv(self.config.data_path, [self.pid],
                clf_dict_leg, label_dict=self.config.leg_gestures)
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

    def __init__(self, data_root, pid, sid_list, processor, pools=6):
        QtCore.QThread.__init__(self, parent=None)
        self.data_root = data_root
        self.pid = pid
        self.sid_list = sid_list
        self.processor = processor
        self.pools = pools

    def run(self):
        processing.batch_process(self.data_root, self.pid, self.processor,
                                 sid_list=self.sid_list, pool=self.pools)
        self.finished_sig.emit()
