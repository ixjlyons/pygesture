# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pygesture/ui/main_template.ui'
#
# Created: Wed Apr  1 17:10:52 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_PygestureMainWindow(object):
    def setupUi(self, PygestureMainWindow):
        PygestureMainWindow.setObjectName(_fromUtf8("PygestureMainWindow"))
        PygestureMainWindow.resize(724, 640)
        self.centralwidget = QtGui.QWidget(PygestureMainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        PygestureMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(PygestureMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 724, 19))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        PygestureMainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(PygestureMainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        PygestureMainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(PygestureMainWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        PygestureMainWindow.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolBar)
        self.actionTrain = QtGui.QAction(PygestureMainWindow)
        self.actionTrain.setObjectName(_fromUtf8("actionTrain"))
        self.actionProcess = QtGui.QAction(PygestureMainWindow)
        self.actionProcess.setObjectName(_fromUtf8("actionProcess"))
        self.actionTest = QtGui.QAction(PygestureMainWindow)
        self.actionTest.setObjectName(_fromUtf8("actionTest"))
        self.toolBar.addAction(self.actionTrain)
        self.toolBar.addAction(self.actionProcess)
        self.toolBar.addAction(self.actionTest)

        self.retranslateUi(PygestureMainWindow)
        QtCore.QMetaObject.connectSlotsByName(PygestureMainWindow)

    def retranslateUi(self, PygestureMainWindow):
        PygestureMainWindow.setWindowTitle(_translate("PygestureMainWindow", "pygesture", None))
        self.toolBar.setWindowTitle(_translate("PygestureMainWindow", "toolBar", None))
        self.actionTrain.setText(_translate("PygestureMainWindow", "Train", None))
        self.actionTrain.setToolTip(_translate("PygestureMainWindow", "Generate training data", None))
        self.actionProcess.setText(_translate("PygestureMainWindow", "Process", None))
        self.actionProcess.setToolTip(_translate("PygestureMainWindow", "Process data", None))
        self.actionTest.setText(_translate("PygestureMainWindow", "Test", None))
        self.actionTest.setToolTip(_translate("PygestureMainWindow", "Test control in a real-time task", None))

