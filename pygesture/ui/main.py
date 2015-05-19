import os
import sys
import argparse
import shutil

from pygesture import config
from pygesture import filestruct

from pygesture.ui.qt import QtGui

from pygesture.ui.main_template import Ui_PygestureMainWindow
from pygesture.ui import recorder
from pygesture.ui import train
from pygesture.ui import test
from pygesture.ui import widgets


class PygestureMainWindow(QtGui.QMainWindow):

    def __init__(self, config, parent=None):
        super(PygestureMainWindow, self).__init__(parent)

        self.cfg = config
        self.session = None

        self.ui = Ui_PygestureMainWindow()
        self.ui.setupUi(self)

        self.record_thread = recorder.RecordThread(self.cfg.daq)
        self.init_tabs()

        self.statusbar_label = QtGui.QLabel("not signed in")
        self.ui.statusbar.addPermanentWidget(self.statusbar_label)

        self.ui.actionNew.triggered.connect(self.show_new_session_dialog)

    def closeEvent(self, event):
        if self.record_thread is not None:
            self.record_thread.kill()

    def init_tabs(self):
        self.tabs = {
            "Signals":
                widgets.SignalWidget(
                    self.cfg, self.record_thread, parent=self),
            "Train":
                train.TrainWidget(
                    self.cfg, self.record_thread, parent=self),
            "View":
                widgets.RecordingViewerWidget(
                    self.cfg, parent=self),
            "Process":
                widgets.ProcessWidget(
                    self.cfg, parent=self),
            "Test":
                test.TestWidget(
                    self.cfg, self.record_thread, parent=self)
        }

        for name in ["Signals", "Train", "View", "Process", "Test"]:
            self.ui.tabWidget.addTab(self.tabs[name], name)

            if name != "Signals":
                self.tabs[name].setEnabled(False)

    def show_new_session_dialog(self):
        dialog = widgets.NewSessionDialog(self)
        if dialog.exec_():
            data = dialog.get_data()
            self.update_session(data)

    def update_session(self, data):
        # make sure all info was filled in
        if data['pid'] == '' or data['sid'] == '':
            QtGui.QMessageBox.critical(
                self,
                "Error",
                "Session info incomplete.")
            return

        self.session = Session(
            self.cfg.data_path,
            data['pid'],
            data['sid'],
            data['configuration'])

        # if session exists, make sure the user wants to overwrite it
        try:
            self.session.init_file_structure()
        except IOError:
            message = QtGui.QMessageBox().warning(
                self,
                "Warning",
                "Session directory already exists.\nOverwrite?",
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

            if message == QtGui.QMessageBox.No:
                self.session = None
                return
            elif message == QtGui.QMessageBox.Yes:
                self.session.init_file_structure(force=True)

        self.statusbar_label.setText("Session " + str(self.session))

        for name, tab in self.tabs.items():
            tab.setEnabled(True)

            if name in ["Train", "Test", "View", "Process"]:
                tab.set_session(self.session)


class Session(object):

    def __init__(self, data_path, pid, sid, configuration):
        self.data_path = data_path
        self.pid = pid
        self.sid = sid
        self.configuration = configuration

    def init_file_structure(self, force=False):
        session_dir, datestr = filestruct.new_session_dir(
            self.data_path, self.pid, self.sid)

        if os.path.isdir(session_dir):
            if force:
                shutil.rmtree(session_dir)
            else:
                raise IOError('Session directory already exists.')

        os.makedirs(session_dir)

        self.datestr = datestr
        self.session_dir = session_dir

    def __str__(self):
        return "pid: %s, sid: %s, config: %s" % (
            self.pid, self.sid, self.configuration
        )


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
