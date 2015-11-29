import sys

from pygesture.ui.qt import QtCore, QtGui, QtWidgets


class CursorInterface2D(QtWidgets.QGraphicsView):
    """
    A 2D cursor control interface implemented using a QGraphicsView.

    This view essentially just holds a QGraphicsScene that grows to fit the
    size of the view, keeping the aspect ratio square. The scene is displayed
    with a gray border.
    """

    initleft = -200
    initbottom = initleft
    initwidth = -initleft*2
    initheight = -initleft*2

    def __init__(self, parent=None):
        super(CursorInterface2D, self).__init__(parent)

        self._init_scene()
        self._init_border()

    def _init_scene(self):
        scene = QtWidgets.QGraphicsScene()
        scene.setSceneRect(self.initleft, self.initbottom,
                           self.initwidth, self.initheight)
        scene.setItemIndexMethod(QtWidgets.QGraphicsScene.NoIndex)

        self.setScene(scene)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setBackgroundBrush(QtCore.Qt.white)

    def _init_border(self):
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
        super(CursorInterface2D, self).resizeEvent(event)
        self.fitInView(self.sceneRect(), QtCore.Qt.KeepAspectRatio)


class CircleItem(QtWidgets.QGraphicsObject):

    POSITION_CTRL = 0
    VELOCITY_CTRL = 1

    def __init__(self, radius, color='#333333'):
        super(CircleItem, self).__init__()

        self._radius = None
        self.radius = radius
        self._color = None
        self.color = color
        self._norm_x = 0
        self._norm_y = 0

        self.init_bounding_rect(self._radius)
        self.init_shape()

    def init_bounding_rect(self, radius):
        self._bounding_rect = QtCore.QRectF(-radius, -radius,
                                            2*radius, 2*radius)

    def init_shape(self):
        p = QtGui.QPainterPath()
        p.addEllipse(self.boundingRect())
        self._shape = p

    def boundingRect(self):
        return self._bounding_rect

    def shape(self):
        return self._shape

    def paint(self, painter, option, widget):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(self._color)
        painter.drawEllipse(self._bounding_rect)

    def advance(self, progress=1.0):
        if self.ctrl_mode == self.POSITION_CTRL:
            print
        elif self.ctrl_mode == self.VELOCITY_CTRL:
            print

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = QtGui.QColor(value)
        self.update()

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        self._radius = value
        self.init_bounding_rect(self._radius)
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

    def move_to(self, nx, ny):
        pass

    def move_toward(self, vx, vy):
        pass


class _TestDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(_TestDialog, self).__init__(parent)
        self.layout = QtWidgets.QGridLayout()
        self.interface = CursorInterface2D()
        self.layout.addWidget(self.interface)
        self.setLayout(self.layout)

        self.target = CircleItem(self.interface.map_size(0.1), color='#672311')
        self.cursor = CircleItem(self.interface.map_size(0.05), color='#219421')
        self.interface.scene().addItem(self.target)
        self.interface.scene().addItem(self.cursor)

        self.target.set_norm_pos(0.5, 0.5)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.on_timer_timeout)

    def showEvent(self, event):
        self.timer.start(250)

    def hideEvent(self, event):
        self.timer.stop()

    def keyPressEvent(self, event):
        key = event.key()
        dx = 0
        dy = 0
        inc = 0.04
        if key == QtCore.Qt.Key_W:
            dy += inc
        elif key == QtCore.Qt.Key_S:
            dy -= inc
        elif key == QtCore.Qt.Key_D:
            dx += inc
        elif key == QtCore.Qt.Key_A:
            dx -= inc
        else:
            super().keyPressEvent(event)
            return

        self.cursor.set_norm_pos(self.cursor.norm_x+dx,
                                 self.cursor.norm_y+dy)

    def on_timer_timeout(self):
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    dialog = _TestDialog()
    dialog.show()
    sys.exit(app.exec_())
