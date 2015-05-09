import sys
import argparse

from pygesture import config

from PyQt4 import QtGui
from pygesture.ui.main_template import Ui_PygestureMainWindow
from pygesture.ui import train
from pygesture.ui import test


class MainGUI(QtGui.QMainWindow):

    def __init__(self, config, parent=None):
        super(MainGUI, self).__init__(parent)

        self.cfg = config

        self.ui = Ui_PygestureMainWindow()
        self.ui.setupUi(self)


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
