# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pygesture/ui/main_template.ui'
#
# Created: Wed May 13 15:30:15 2015
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
        PygestureMainWindow.resize(1004, 652)
        PygestureMainWindow.setStyleSheet(_fromUtf8(""))
        self.centralwidget = QtGui.QWidget(PygestureMainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setStyleSheet(_fromUtf8(""))
        self.tabWidget.setTabPosition(QtGui.QTabWidget.North)
        self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        PygestureMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(PygestureMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1004, 27))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu_File = QtGui.QMenu(self.menubar)
        self.menu_File.setObjectName(_fromUtf8("menu_File"))
        PygestureMainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(PygestureMainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        PygestureMainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(PygestureMainWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        PygestureMainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionQuit = QtGui.QAction(PygestureMainWindow)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("application-exit"))
        self.actionQuit.setIcon(icon)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
        self.actionNew = QtGui.QAction(PygestureMainWindow)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("document-new"))
        self.actionNew.setIcon(icon)
        self.actionNew.setObjectName(_fromUtf8("actionNew"))
        self.menu_File.addAction(self.actionNew)
        self.menu_File.addAction(self.actionQuit)
        self.menubar.addAction(self.menu_File.menuAction())
        self.toolBar.addAction(self.actionNew)

        self.retranslateUi(PygestureMainWindow)
        self.tabWidget.setCurrentIndex(-1)
        QtCore.QObject.connect(self.actionQuit, QtCore.SIGNAL(_fromUtf8("triggered()")), PygestureMainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(PygestureMainWindow)

    def retranslateUi(self, PygestureMainWindow):
        PygestureMainWindow.setWindowTitle(_translate("PygestureMainWindow", "PyGesture", None))
        self.menu_File.setTitle(_translate("PygestureMainWindow", "&File", None))
        self.toolBar.setWindowTitle(_translate("PygestureMainWindow", "toolBar", None))
        self.actionQuit.setText(_translate("PygestureMainWindow", "&Quit", None))
        self.actionNew.setText(_translate("PygestureMainWindow", "&New", None))
        self.actionNew.setShortcut(_translate("PygestureMainWindow", "Ctrl+N", None))

