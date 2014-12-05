#from PySide import QtGui, QtCore
from PyQt4 import QtGui, QtCore
qtbackend = 'PyQt4'

import matplotlib
matplotlib.rcParams['backend.qt4'] = qtbackend
from matplotlib.backends.backend_qt4agg \
    import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import pygesture.settings as st
from pygesture import processing
from pygesture import classification


class SessionResultsDialog(QtGui.QDialog):

    def __init__(self, pid):
        super(SessionResultsDialog, self).__init__()

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

        self.processor = SessionProcessor(pid)
        self.processor.finished_sig.connect(self.show_plots)
        self.processor.start()

    def show_plots(self):
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(100)

        clf_dict_arm = {
            'name': 'arm',
            'n_train': 2,
            'sid_list': st.arm_session_list}
        clf_dict_leg = {
            'name': 'leg',
            'n_train': 2,
            'sid_list': st.leg_session_list}

        cm_arm = classification.run_cv(st.DATA_ROOT, self.pid, clf_dict_arm)
        cm_leg = classification.run_cv(st.DATA_ROOT, self.pid, clf_dict_leg)
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

    def __init__(self, pid):
        QtCore.QThread.__init__(self, parent=None)
        self.pid = pid

    def run(self):
        sid_list = st.arm_session_list + st.leg_session_list
        processing.batch_process(st.DATA_ROOT, self.pid,
                                 sid_list=sid_list, pool=6)
        self.finished_sig.emit()
