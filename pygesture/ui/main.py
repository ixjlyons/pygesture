import sys
import argparse

from pygesture import config
from pygesture import recorder

from PyQt4 import QtGui

from pygesture.ui.main_template import Ui_PygestureMainWindow
from pygesture.ui import train
from pygesture.ui import test
from pygesture.ui import signals


class PygestureMainWindow(QtGui.QMainWindow):

    def __init__(self, config, parent=None):
        super(PygestureMainWindow, self).__init__(parent)

        self.cfg = config

        self.ui = Ui_PygestureMainWindow()
        self.ui.setupUi(self)

        self.record_thread = recorder.RecordThread(self.cfg.daq)
        self._init_tabs()

    def closeEvent(self, event):
        if self.record_thread is not None:
            self.record_thread.kill()

    def _init_tabs(self):
        self.ui.tabWidget.addTab(
            signals.SignalWidget(self.cfg, self.record_thread, parent=self),
            "Visualize")
        self.ui.tabWidget.addTab(
            train.TrainWidget(self.cfg, self.record_thread, parent=self),
            "Train")
        self.ui.tabWidget.addTab(
            SomeWindow(parent=self),
            "Process")
        self.ui.tabWidget.addTab(
            test.TestWidget(self.cfg, self.record_thread, parent=self),
            "Test")


class SomeWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(SomeWindow, self).__init__(parent)

    def showEvent(self, event):
        super(SomeWindow, self).showEvent(event)
        print("%s show" % self.__class__.__name__)

    def hideEvent(self, event):
        super(SomeWindow, self).hideEvent(event)
        print("%s hide" % self.__class__.__name__)


class AnotherWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(AnotherWindow, self).__init__(parent)

    def showEvent(self, event):
        super(AnotherWindow, self).showEvent(event)
        print("%s show" % self.__class__.__name__)

    def hideEvent(self, event):
        super(AnotherWindow, self).hideEvent(event)
        print("%s hide" % self.__class__.__name__)


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
