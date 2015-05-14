import sys
import argparse

from pygesture import config
from pygesture import recorder

from PyQt4 import QtGui

from pygesture.ui.main_template import Ui_PygestureMainWindow
from pygesture.ui import train
from pygesture.ui import test
from pygesture.ui import signals
from pygesture.ui import widgets


class PygestureMainWindow(QtGui.QMainWindow):

    def __init__(self, config, parent=None):
        super(PygestureMainWindow, self).__init__(parent)

        self.cfg = config

        self.ui = Ui_PygestureMainWindow()
        self.ui.setupUi(self)

        self.record_thread = recorder.RecordThread(self.cfg.daq)
        self.init_tabs()

        self.ui.actionNew.triggered.connect(self.show_new_session_dialog)

    def showEvent(self, event):
        #self.show_new_session_dialog()
        pass

    def closeEvent(self, event):
        if self.record_thread is not None:
            self.record_thread.kill()

    def init_tabs(self):
        self.signal_tab = signals.SignalWidget(
            self.cfg, self.record_thread, parent=self)
        self.train_tab = train.TrainWidget(
            self.cfg, self.record_thread, parent=self)
        self.viewer_tab = widgets.RecordingViewerWidget(
            self.cfg, parent=self)
        self.test_tab = test.TestWidget(
            self.cfg, self.record_thread, parent=self)

        self.ui.tabWidget.addTab(self.signal_tab, "Signals")
        self.ui.tabWidget.addTab(self.train_tab, "Train")
        self.ui.tabWidget.addTab(self.viewer_tab, "View")
        self.ui.tabWidget.addTab(self.test_tab, "Test")

    def show_new_session_dialog(self):
        dialog = widgets.NewSessionDialog(self)
        if dialog.exec_():
            data = dialog.get_data()
            self.create_session(data['pid'], data['sid'])

    def create_session(self, pid, sid):
        if pid == '' or sid == '':
           QtGui.QMessageBox.critical(
                self,
                "Error",
                "Session info incomplete.")
           return

        self.ui.statusbar.addWidget(
            QtGui.QLabel("pid: %s, sid: %s" % (pid, sid)))

        self.test_tab.set_pid(pid)
        self.viewer_tab.set_pid(pid)


def main():
    parser = argparse.ArgumentParser(
        description="EMG gesture recognition with real-time feedback.")
    parser.add_argument(
        '-c', '--config',
        dest='config',
        default='config.py',
        help="Config file. Default is `config.py` (current directory).")
    args = parser.parse_args()

    cfg = config.Config(args.config)

    app = QtGui.QApplication([])
    mw = PygestureMainWindow(cfg)
    mw.show()
    app.exec_()
    app.deleteLater()
    sys.exit(0)
