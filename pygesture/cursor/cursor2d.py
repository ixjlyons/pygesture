import sys

from pygesture.ui.qt import QtCore, QtGui, QtWidgets

class CursorInterface2D(QtWidgets.QGraphicsView):

    initleft = -100
    initbottom = initleft
    initwidth = -initleft*2
    initheight = -initleft*2

    def __init__(self, parent=None):
        super(CursorInterface2D, self).__init__(parent)

        self.init_scene()
        self.init_border()

    def init_scene(self):
        scene = QtWidgets.QGraphicsScene()
        scene.setSceneRect(self.initleft, self.initbottom,
                           self.initwidth, self.initheight)
        scene.setItemIndexMethod(QtWidgets.QGraphicsScene.NoIndex)

        self.setScene(scene)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setBackgroundBrush(QtCore.Qt.white)

    def init_border(self):
        rect = self.scene().sceneRect()
        pen = QtGui.QPen(QtGui.QColor('#444444'))
        lines = [
            QtCore.QLineF(rect.topLeft(), rect.topRight()),
            QtCore.QLineF(rect.topLeft(), rect.bottomLeft()),
            QtCore.QLineF(rect.topRight(), rect.bottomRight()),
            QtCore.QLineF(rect.bottomLeft(), rect.bottomRight())
        ]

        for line in lines:
            self.scene().addLine(line, pen)

    def map_coords(self, nx, ny):
        return self.map_size(nx), -self.map_size(ny)

    def map_size(self, size):
        return size * (self.sceneRect().width()/2)

    def resizeEvent(self, event):
        self.fitInView(self.sceneRect(), QtCore.Qt.KeepAspectRatio)


class Circle(QtWidgets.QGraphicsObject):

    def __init__(self, diameter, color='#333333'):
        super(Circle, self).__init__()

        self.diameter = diameter

        self._bounding_rect = QtCore.QRectF(-self.diameter/2, -self.diameter/2,
                                            self.diameter, self.diameter)
        p = QtGui.QPainterPath()
        p.addEllipse(self._bounding_rect)
        self._shape = p

        self._color = None
        self.color = color

        self._norm_x = 0
        self._norm_y = 0

    def boundingRect(self):
        return self._bounding_rect

    def shape(self):
        return self._shape

    def paint(self, painter, option, widget):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(self._color)

        painter.drawEllipse(self._bounding_rect)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = QtGui.QColor(value)
        self.update()

    def set_norm_pos(self, nx, ny):
        self.norm_x = nx
        self.norm_y = ny

    @property
    def norm_x(self):
        return self._norm_x

    @norm_x.setter
    def norm_x(self, value):
        self._norm_x = value
        self.setX(self.scene().width()/2*self._norm_x)

    @property
    def norm_y(self):
        return self._norm_y

    @norm_y.setter
    def norm_y(self, value):
        self._norm_y = value
        self.setY(-self.scene().width()/2*self._norm_y)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    dialog = QtWidgets.QDialog()
    layout = QtWidgets.QGridLayout()

    interface = CursorInterface2D()

    target = Circle(interface.map_size(0.2), color='#672311')
    target.setPos(*interface.map_coords(0.5, 0.5))
    interface.scene().addItem(target)

    cursor = Circle(interface.map_size(0.1), color='#219421')
    cursor.setPos(*interface.map_coords(0, 0))
    interface.scene().addItem(cursor)

    def timerEvent():
        cursor.set_norm_pos(cursor.norm_x+0.01, cursor.norm_y+0.01)

    timer = QtCore.QTimer()
    timer.timeout.connect(timerEvent)
    timer.start(1000/33)


    layout.addWidget(interface)
    dialog.setLayout(layout)

    dialog.show()
    sys.exit(app.exec_())
