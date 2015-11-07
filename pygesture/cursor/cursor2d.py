import sys

from pygesture.ui.qt import QtCore, QtGui, QtWidgets

class CursorInterface2D(QtWidgets.QGraphicsView):

    left = -150
    bottom = -150
    width = 300
    height = 300

    def __init__(self, parent=None):
        super(CursorInterface2D, self).__init__(parent)

        self.init_scene()
        self.init_border()

    def init_scene(self):
        scene = QtWidgets.QGraphicsScene(self)
        scene.setSceneRect(self.left, self.bottom, self.width, self.height)

        self.setScene(scene)
        self.setRenderHint(QtGui.QPainter.Antialiasing)

    def init_border(self):
        rect = self.scene().sceneRect()
        pen = QtGui.QPen(QtCore.Qt.red)
        lines = [
            QtCore.QLineF(rect.topLeft(), rect.topRight()),
            QtCore.QLineF(rect.topLeft(), rect.bottomLeft()),
            QtCore.QLineF(rect.topRight(), rect.bottomRight()),
            QtCore.QLineF(rect.bottomLeft(), rect.bottomRight())
        ]

        for line in lines:
            self.scene().addLine(line, pen)


class Circle(QtWidgets.QGraphicsObject):

    def __init__(self, diameter, startx=0, starty=0):
        super(Circle, self).__init__()

        self.diameter = diameter
        self.startx = startx
        self.starty = starty

    def boundingRect(self):
        return QtCore.QRectF(0, 0, self.diameter, self.diameter)

    def paint(self, painter, option, widget):
        rect = self.boundingRect()

        if self.scene().collidingItems(self):
            col = QtCore.Qt.red
        else:
            col = QtCore.Qt.green

        painter.setPen(QtGui.QPen(col))

        painter.drawEllipse(rect)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    dialog = QtWidgets.QDialog()
    layout = QtWidgets.QGridLayout()
    interface = CursorInterface2D()

    layout.addWidget(CursorInterface2D())
    dialog.setLayout(layout)

    dialog.show()
    sys.exit(app.exec_())
