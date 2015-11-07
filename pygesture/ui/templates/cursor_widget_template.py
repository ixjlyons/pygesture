# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pygesture/ui/templates/cursor_widget_template.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CursorWidget(object):
    def setupUi(self, CursorWidget):
        CursorWidget.setObjectName("CursorWidget")
        CursorWidget.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(CursorWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.cursorView = CursorInterface2D(CursorWidget)
        self.cursorView.setObjectName("cursorView")
        self.gridLayout.addWidget(self.cursorView, 0, 0, 1, 1)

        self.retranslateUi(CursorWidget)
        QtCore.QMetaObject.connectSlotsByName(CursorWidget)

    def retranslateUi(self, CursorWidget):
        _translate = QtCore.QCoreApplication.translate
        CursorWidget.setWindowTitle(_translate("CursorWidget", "Form"))

from pygesture.cursor.cursor2d import CursorInterface2D
