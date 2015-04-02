import sys
import argparse

from pygesture import config

from PyQt4 import QtGui, QtCore
from pygesture.ui.main_template import Ui_PygestureMainWindow
from pygesture.ui import train2
from pygesture.ui import test

class MainGUI(QtGui.QMainWindow):

    def __init__(self, config, parent=None):
        super(MainGUI, self).__init__(parent)

        self.cfg = config

        self.ui = Ui_PygestureMainWindow()
        self.ui.setupUi(self)

        self.ui.trainButton.clicked.connect(self.launch_train)
        self.ui.processButton.clicked.connect(self.launch_process)
        self.ui.testButton.clicked.connect(self.launch_test)

    def launch_train(self):
        trainGUI = train2.TrainGUI(self.cfg, parent=self)
        trainGUI.show()
        trainGUI.destroyed.connect(self.window_closed_callback)

    def launch_process(self):
        pass

    def launch_test(self):
        testGUI = test.RealTimeGUI(self.cfg, parent=self)
        testGUI.show()
        #testGUI.destroyed.connect(self.window_closed_callback)

    def window_closed_callback(self):
        print('hello')

    def closeEvent(self, event):
        print('hellothere')
        QtGui.QMainWindow.closeEvent(self, event)


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
    mw = MainGUI(cfg)
    mw.show()
    app.exec_()
    app.deleteLater()
    sys.exit(0)
