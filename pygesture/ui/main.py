import os
import sys
import argparse
import shutil

from pygesture import config
from pygesture import filestruct

from pygesture.ui.qt import QtWidgets

from pygesture.ui.templates.main_template import Ui_PygestureMainWindow
from pygesture.ui import recorder
from pygesture.ui import tabs
from pygesture.ui import widgets


class PygestureMainWindow(QtWidgets.QMainWindow):

    def __init__(self, config, parent=None):
        super(PygestureMainWindow, self).__init__(parent)

        self.cfg = config
        self.session = None

        self.ui = Ui_PygestureMainWindow()
        self.ui.setupUi(self)

        self.record_thread = recorder.RecordThread(self.cfg.daq)
        self.init_tabs()

        self.statusbar_label = QtWidgets.QLabel("not signed in")
        self.ui.statusbar.addPermanentWidget(self.statusbar_label)

        self.ui.actionNew.triggered.connect(self.show_new_session_dialog)

    def closeEvent(self, event):
        if self.record_thread is not None:
            self.record_thread.kill()

    def init_tabs(self):
        self.permanent_tabs = [
            (
                "Signals",
                tabs.SignalWidget(
                    self.cfg, self.record_thread, parent=self)
            ),
            (
                "View",
                tabs.RecordingViewerWidget(
                    self.cfg, parent=self),
            ),
            (
                "Process",
                tabs.ProcessWidget(
                    self.cfg, parent=self),
            )
        ]

        for name, widget in self.permanent_tabs:
            self.ui.tabWidget.addTab(widget, name)

    def show_new_session_dialog(self):
        dialog = widgets.NewSessionDialog(self)
        dialog.set_task_list(list(self.cfg.ui_tabs.keys()))
        if dialog.exec_():
            data = dialog.get_data()
            self.new_session(data)

    def new_session(self, data):
        if data['pid'] == '' or data['sid'] == '':
            QtWidgets.QMessageBox.critical(
                self,
                "Error",
                "Session info incomplete.")
            return

        self.session = Session(
            self.cfg.data_path,
            data['pid'],
            data['sid'],
            data['task'],
            data['configuration'],
            data['hand'])

        # if session exists, make sure the user wants to overwrite it
        try:
            self.session.init_file_structure()
        except IOError:
            message = QtWidgets.QMessageBox().warning(
                self,
                "Warning",
                "Session directory already exists.\nOverwrite?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

            if message == QtWidgets.QMessageBox.No:
                self.session = None
                return
            else:
                self.session.init_file_structure(force=True)

        self.remove_session_tab()

        widgetcls = self.cfg.ui_tabs[self.session.task]
        widget = widgetcls(
            self.cfg, self.record_thread, self.session, parent=self)

        self.ui.tabWidget.addTab(widget, self.session.task)
        self.ui.tabWidget.setCurrentIndex(self.ui.tabWidget.count()-1)

        self.statusbar_label.setText("Session " + str(self.session))

    def remove_session_tab(self):
        """Removes a session tab (train or test) if one exists."""
        count = self.ui.tabWidget.count()
        if count > len(self.permanent_tabs):
            self.ui.tabWidget.removeTab(count-1)


class Session(object):

    def __init__(self, data_path, pid, sid, task, configuration, hand):
        self.data_path = data_path
        self.pid = pid
        self.sid = sid
        self.task = task
        self.configuration = configuration
        self.hand = hand

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
        return "pid: %s, sid: %s, task: %s, config: %s, hand: %s" % (
            self.pid, self.sid, self.task, self.configuration, self.hand
        )


def main():
    parser = argparse.ArgumentParser(
        description="EMG gesture recognition with real-time feedback.")
    parser.add_argument(
        '-c', '--config',
        dest='config',
        default='config.py',
        help="Config file. Default is `config.py` (current directory).")
    parser.add_argument(
        '-t', '--test',
        dest='test',
        action='store_true', default=False)
    args = parser.parse_args()

    cfg = config.Config(args.config)
    cfg.test = args.test

    app = QtWidgets.QApplication([])
    mw = PygestureMainWindow(cfg)
    mw.show()
    app.exec_()
    app.deleteLater()
    sys.exit(0)
