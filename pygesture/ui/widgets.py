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

    def __init__(self, parent=None, length=6, transitions=(2, 5)):
        super(PromptWidget, self).__init__()
        self.setFixedHeight(PromptWidget.HEIGHT)
        self.value = 0
        self.tick_labels = [str(i) for i in range(1, int(length))]
        self.maximum = length*1000
        self.length = length
        self.trans1 = transitions[0]*1000
        self.trans2 = transitions[1]*1000
        self.transitions = transitions

        self.tick_font = QtGui.QFont('Serif', 7, QtGui.QFont.Light)
        self.prompt_font = QtGui.QFont('Serif', 10, QtGui.QFont.Light)

    def setProgress(self, value):
        self.value = value
        self.repaint()

    def getProgress(self):
        return self.value

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.draw(qp)
        qp.end()

    def draw(self, qp):

        w = self.size().width()
        h = self.size().height()

        tick_step = int(round(w / self.length))

        till = int(((w / float(self.maximum)) * self.value))
        full1 = int(((w / float(self.maximum)) * self.trans1))
        full2 = int(((w / float(self.maximum)) * self.trans2))

        qp.setPen(PromptWidget.REST_COLOR)
        qp.setBrush(PromptWidget.REST_COLOR)
        qp.drawRect(0, 0, till, h)

        qp.setPen(PromptWidget.CONTRACT_COLOR)
        qp.setBrush(PromptWidget.CONTRACT_COLOR)
        qp.drawRect(full1, 0, full2-full1, h)

        pen = QtGui.QPen(QtGui.QColor(20, 20, 20), 1, QtCore.Qt.SolidLine)

        qp.setPen(pen)
        qp.setBrush(QtCore.Qt.NoBrush)
        qp.drawRect(0, 0, w-1, h-1)

        qp.setFont(self.prompt_font)
        for t, l in zip(self.transitions, ['contract', 'rest']):
            x = int(((w / float(self.maximum)) * (t*1000.)))
            metrics = qp.fontMetrics()
            fw = metrics.width(l)
            qp.drawText(x-fw/2, h/2, l)

        qp.setFont(self.tick_font)
        j = 0
        for i in range(tick_step, self.length*tick_step, tick_step):
            qp.drawLine(i, h-5, i, h)
            metrics = qp.fontMetrics()
            fw = metrics.width(self.tick_labels[j])
            qp.drawText(i-fw/2, h-7, self.tick_labels[j])
            j += 1

    value_prop = QtCore.pyqtProperty(float, getProgress, setProgress)
