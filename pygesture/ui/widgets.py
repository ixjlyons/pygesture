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
