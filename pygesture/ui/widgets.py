from PyQt4 import QtGui, QtCore


class GestureView(QtGui.QLabel):
    """
    A trivial extension of QLabel so we can connect to resizeEvent.
    """

    resize_signal = QtCore.pyqtSignal(QtGui.QResizeEvent)

    def __init__(self, parent=None):
        QtGui.QLabel.__init__(self, parent)

    def resizeEvent(self, event=None):
        self.resize_signal.emit(event)


class PromptWidget(QtGui.QWidget):

    HEIGHT = 40
    REST_COLOR = QtGui.QColor(90, 90, 90)
    CONTRACT_COLOR = QtGui.QColor(150, 80, 80, 150)

    def __init__(self, parent=None):
        super(PromptWidget, self).__init__()
        self.setFixedHeight(PromptWidget.HEIGHT)
        self.value = 0
        self._ticks = 1
        self.update_tick_labels()
        self._transitions = (0, 1)

        self.tick_font = QtGui.QFont('Serif', 7, QtGui.QFont.Light)
        self.prompt_font = QtGui.QFont('Serif', 10, QtGui.QFont.Light)

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

    def setProgress(self, value):
        self.value = value
        self.repaint()

    def getProgress(self):
        return self.value

    def update_tick_labels(self):
        self.tick_labels = [str(i) for i in range(1, int(self._ticks))]

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.draw(qp)
        qp.end()

    def draw(self, qp):

        w = self.size().width()
        h = self.size().height()

        tick_step = int(round(w / self._ticks))

        till = int(((w / float(self._ticks*1000)) * self.value))
        f1 = int(((w / float(self._ticks*1000)) * self._transitions[0]*1000))
        f2 = int(((w / float(self._ticks*1000)) * self._transitions[1]*1000))

        qp.setPen(PromptWidget.REST_COLOR)
        qp.setBrush(PromptWidget.REST_COLOR)
        qp.drawRect(0, 0, till, h)

        qp.setPen(PromptWidget.CONTRACT_COLOR)
        qp.setBrush(PromptWidget.CONTRACT_COLOR)
        qp.drawRect(f1, 0, f2-f1, h)

        pen = QtGui.QPen(QtGui.QColor(20, 20, 20), 1, QtCore.Qt.SolidLine)

        qp.setPen(pen)
        qp.setBrush(QtCore.Qt.NoBrush)
        qp.drawRect(0, 0, w-1, h-1)

        qp.setFont(self.prompt_font)
        for t, l in zip(self._transitions, ['contract', 'rest']):
            x = int(((w / float(self._ticks*1000)) * (t*1000.)))
            metrics = qp.fontMetrics()
            fw = metrics.width(l)
            qp.drawText(x-fw/2, h/2, l)

        qp.setFont(self.tick_font)
        j = 0
        for i in range(tick_step, self._ticks*tick_step, tick_step):
            qp.drawLine(i, h-5, i, h)
            metrics = qp.fontMetrics()
            fw = metrics.width(self.tick_labels[j])
            qp.drawText(i-fw/2, h-7, self.tick_labels[j])
            j += 1

    value_prop = QtCore.pyqtProperty(float, getProgress, setProgress)


class BoostsWidget(QtGui.QWidget):

    updated = QtCore.pyqtSignal(dict)

    def __init__(self, parent=None):
        super(BoostsWidget, self).__init__(parent)

        self.spinboxes = dict()
        self.values = dict()
        self.form = QtGui.QFormLayout()
        self.setLayout(self.form)

    def set_mapping(self, labels, limits=(0, 1), init=0.5, step=0.1):
        # labels is a list of tuples [(int, str), (int, str)...]
        for num, text in labels:
            spinbox = QtGui.QDoubleSpinBox()
            spinbox.setRange(*limits)
            spinbox.setValue(init)
            spinbox.setSingleStep(step)
            spinbox.valueChanged.connect(self.spinbox_callback)

            self.spinboxes[num] = spinbox
            self.values[num] = init

            self.form.addRow(text, spinbox)

    def spinbox_callback(self, value):
        for label, box in self.spinboxes.items():
            self.values[label] = box.value()

        self.updated.emit(self.values)

    def set_values(self, values):
        for label, box in self.spinboxes.items():
            box.setValue(values[label])
