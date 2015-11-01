from pygesture import filestruct

from pygesture.ui.qt import QtGui, QtCore, QtWidgets
from .templates.new_session_template import Ui_NewSessionDialog
from .templates.session_browser_template import Ui_SessionBrowser


class GestureView(QtWidgets.QWidget):
    """
    A widget meant to display a QPixmap. It automatically adjusts the size of
    the image while keeping the aspect ratio constant.
    """
    # TODO figure out how to center child QLabel (setAlignment doesn't work)

    def __init__(self, parent=None):
        super(GestureView, self).__init__(parent)

        self.label = QtWidgets.QLabel(self)
        self.label.setScaledContents(True)
        self.label.setFixedSize(0, 0)

    def resizeEvent(self, event=None):
        super(GestureView, self).resizeEvent(event)
        self.resize_image()

    def pixmap(self):
        return self.label.pixmap()

    def setPixmap(self, pixmap):
        self.label.setPixmap(pixmap)
        self.resize_image()

    def resize_image(self):
        pm = self.label.pixmap()
        if pm is not None:
            new_size = pm.size()
            new_size.scale(self.size(), QtCore.Qt.KeepAspectRatio)
            self.label.setFixedSize(new_size)


class PromptWidget(QtWidgets.QProgressBar):
    """
    A custom QProgressBar which paints tick marks and a highlight bar over the
    base bar. The ticks can be used, for instance, for indicating the number
    of seconds in a trial. The highlight bar can be used to indicate the
    boundaries of some event during the trial.
    """

    def __init__(self, parent=None):
        super(PromptWidget, self).__init__(parent)

        self.value = 0
        self._ticks = 1
        self.update_tick_labels()
        self._transitions = (0, 1)

        self.palette = QtGui.QPalette()

    @property
    def ticks(self):
        return self._ticks

    @ticks.setter
    def ticks(self, value):
        self._ticks = value
        self.update_tick_labels()
        self.repaint()

    @property
    def transitions(self):
        return self._transitions

    @transitions.setter
    def transitions(self, value):
        self._transitions = value
        self.repaint()

    def update_tick_labels(self):
        self.tick_labels = [str(i) for i in range(1, int(self._ticks))]

    def paintEvent(self, event):
        super(PromptWidget, self).paintEvent(event)
        painter = QtGui.QPainter()
        painter.begin(self)
        self.draw_ticks(painter)
        painter.end()

    def reset(self):
        self.setValue(0)

    def draw_ticks(self, painter):
        w = self.width()
        h = self.height()

        tick_step = int(round(w / self._ticks))

        f1 = int(((w / float(self._ticks*1000)) * self._transitions[0]*1000))
        f2 = int(((w / float(self._ticks*1000)) * self._transitions[1]*1000))

        # the contract indicator window
        painter.setPen(QtGui.QColor(0, 0, 0, 0))
        painter.setBrush(QtGui.QColor(180, 80, 80, 140))
        painter.drawRect(f1, 0, f2-f1, h)

        painter.setPen(self.palette.color(QtGui.QPalette.Text))
        painter.setFont(self.font())

        # draw the "contact" and "rest" text
        for t, l in zip(self._transitions, ['contract', 'rest']):
            x = int(((w / float(self._ticks*1000)) * (t*1000.)))
            metrics = painter.fontMetrics()
            fw = metrics.width(l)
            painter.drawText(x-fw/2, h/2, l)

        # draw the ticks marking each second
        j = 0
        for i in range(tick_step, self._ticks*tick_step, tick_step):
            painter.drawLine(i, h-5, i, h)
            metrics = painter.fontMetrics()
            fw = metrics.width(self.tick_labels[j])
            painter.drawText(i-fw/2, h-7, self.tick_labels[j])
            j += 1


class NewSessionDialog(QtWidgets.QDialog):
    """
    A very simple QDialog for getting some "log in" type information for a
    session. Layout comes from a ui file.
    """

    def __init__(self, parent=None):
        super(NewSessionDialog, self).__init__(parent)

        self.ui = Ui_NewSessionDialog()
        self.ui.setupUi(self)

    def set_task_list(self, task_list):
        self.ui.taskComboBox.addItems(task_list)

    def get_data(self):
        data = {
            'pid':
                str(self.ui.participantLineEdit.text()),
            'sid':
                str(self.ui.sessionLineEdit.text()),
            'task':
                str(self.ui.taskComboBox.currentText()),
            'configuration':
                str(self.ui.configurationGroup.checkedButton().text()),
            'hand':
                str(self.ui.handGroup.checkedButton().text())
        }
        return data


class SessionBrowser(QtWidgets.QWidget):
    """
    A composite widget with a combo box for selecting a participant and a
    list widget for seeing the participant's sessions.
    """

    participant_selected = QtCore.pyqtSignal(str)
    session_selected = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(SessionBrowser, self).__init__(parent)

        self.ui = Ui_SessionBrowser()
        self.ui.setupUi(self)

        self.session_filter = ""

        self.ui.refreshButton.clicked.connect(self.on_refresh_clicked)

    def set_session_filter(self, search):
        """
        Allows for filtering of the session list by requiring `search` to be
        contained in the session ID.
        """
        self.session_filter = search

    def set_data_path(self, path):
        self.data_path = path

        self.ui.participantComboBox.clear()
        self.ui.sessionList.clear()

        self.ui.participantComboBox.currentIndexChanged[str].connect(
            self.on_participant_selection)

        pids = filestruct.get_participant_list(self.data_path)
        self.ui.participantComboBox.addItems(pids)

        self.ui.sessionList.currentTextChanged.connect(
            self.on_session_selection)

        if len(pids) > 0:
            self.on_participant_selection(
                self.ui.participantComboBox.currentText())

    def on_refresh_clicked(self):
        self.set_data_path(self.data_path)

    def on_participant_selection(self, text):
        pid = str(text)
        if pid == '':
            return

        self.pid = pid

        self.sid_list = filestruct.get_session_list(
            self.data_path, self.pid, search=self.session_filter)

        self.ui.sessionList.clear()
        for sid in self.sid_list:
            QtWidgets.QListWidgetItem(sid, self.ui.sessionList)

        self.participant_selected.emit(pid)

    def on_session_selection(self, text):
        sid = str(text)
        if sid == '':
            return

        self.session_selected.emit(sid)
