# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pygesture/ui/main_template.ui'
#
# Created: Tue May 12 16:06:52 2015
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
        self.mainDock = QtGui.QDockWidget(PygestureMainWindow)
        self.mainDock.setEnabled(True)
        self.mainDock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.mainDock.setObjectName(_fromUtf8("mainDock"))
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.formLayout = QtGui.QFormLayout(self.dockWidgetContents)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.participantLabel = QtGui.QLabel(self.dockWidgetContents)
        self.participantLabel.setObjectName(_fromUtf8("participantLabel"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.participantLabel)
        self.participantLineEdit = QtGui.QLineEdit(self.dockWidgetContents)
        self.participantLineEdit.setObjectName(_fromUtf8("participantLineEdit"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.participantLineEdit)
        self.sessionLabel = QtGui.QLabel(self.dockWidgetContents)
        self.sessionLabel.setObjectName(_fromUtf8("sessionLabel"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.sessionLabel)
        self.sessionLineEdit = QtGui.QLineEdit(self.dockWidgetContents)
        self.sessionLineEdit.setObjectName(_fromUtf8("sessionLineEdit"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.sessionLineEdit)
        self.mainDock.setWidget(self.dockWidgetContents)
        PygestureMainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.mainDock)
        self.actionQuit = QtGui.QAction(PygestureMainWindow)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("application-exit"))
        self.actionQuit.setIcon(icon)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
        self.actionCheckSignals = QtGui.QAction(PygestureMainWindow)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("audio-card"))
        self.actionCheckSignals.setIcon(icon)
        self.actionCheckSignals.setObjectName(_fromUtf8("actionCheckSignals"))
        self.actionProbe = QtGui.QAction(PygestureMainWindow)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("audio-input-microphone"))
        self.actionProbe.setIcon(icon)
        self.actionProbe.setObjectName(_fromUtf8("actionProbe"))
        self.menu_File.addAction(self.actionQuit)
        self.menubar.addAction(self.menu_File.menuAction())

        self.retranslateUi(PygestureMainWindow)
        self.tabWidget.setCurrentIndex(-1)
        QtCore.QObject.connect(self.actionQuit, QtCore.SIGNAL(_fromUtf8("triggered()")), PygestureMainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(PygestureMainWindow)

    def retranslateUi(self, PygestureMainWindow):
        PygestureMainWindow.setWindowTitle(_translate("PygestureMainWindow", "PyGesture", None))
        self.menu_File.setTitle(_translate("PygestureMainWindow", "&File", None))
        self.mainDock.setWindowTitle(_translate("PygestureMainWindow", "Session", None))
        self.participantLabel.setText(_translate("PygestureMainWindow", "Participant:", None))
        self.sessionLabel.setText(_translate("PygestureMainWindow", "Session:", None))
        self.actionQuit.setText(_translate("PygestureMainWindow", "&Quit", None))
        self.actionCheckSignals.setText(_translate("PygestureMainWindow", "Check Signals", None))
        self.actionProbe.setText(_translate("PygestureMainWindow", "Probe", None))

