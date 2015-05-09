# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pygesture/ui/main_template.ui'
#
# Created: Fri May  8 18:41:28 2015
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
        PygestureMainWindow.resize(1045, 714)
        self.centralwidget = QtGui.QWidget(PygestureMainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.trainTab = QtGui.QWidget()
        self.trainTab.setObjectName(_fromUtf8("trainTab"))
        self.tabWidget.addTab(self.trainTab, _fromUtf8(""))
        self.processTab = QtGui.QWidget()
        self.processTab.setObjectName(_fromUtf8("processTab"))
        self.tabWidget.addTab(self.processTab, _fromUtf8(""))
        self.testTab = QtGui.QWidget()
        self.testTab.setObjectName(_fromUtf8("testTab"))
        self.tabWidget.addTab(self.testTab, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        PygestureMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(PygestureMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1045, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu_File = QtGui.QMenu(self.menubar)
        self.menu_File.setObjectName(_fromUtf8("menu_File"))
        self.menu_View = QtGui.QMenu(self.menubar)
        self.menu_View.setObjectName(_fromUtf8("menu_View"))
        PygestureMainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(PygestureMainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        PygestureMainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(PygestureMainWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        PygestureMainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.mainDock = QtGui.QDockWidget(PygestureMainWindow)
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
        self.action_Quit = QtGui.QAction(PygestureMainWindow)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("application-exit"))
        self.action_Quit.setIcon(icon)
        self.action_Quit.setObjectName(_fromUtf8("action_Quit"))
        self.actionCheck_Signals = QtGui.QAction(PygestureMainWindow)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("audio-card"))
        self.actionCheck_Signals.setIcon(icon)
        self.actionCheck_Signals.setObjectName(_fromUtf8("actionCheck_Signals"))
        self.actionProbe = QtGui.QAction(PygestureMainWindow)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("audio-input-microphone"))
        self.actionProbe.setIcon(icon)
        self.actionProbe.setObjectName(_fromUtf8("actionProbe"))
        self.menu_File.addAction(self.action_Quit)
        self.menu_View.addAction(self.actionCheck_Signals)
        self.menu_View.addAction(self.actionProbe)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_View.menuAction())
        self.toolBar.addAction(self.actionProbe)
        self.toolBar.addAction(self.actionCheck_Signals)

        self.retranslateUi(PygestureMainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(PygestureMainWindow)

    def retranslateUi(self, PygestureMainWindow):
        PygestureMainWindow.setWindowTitle(_translate("PygestureMainWindow", "MainWindow", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.trainTab), _translate("PygestureMainWindow", "Train", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.processTab), _translate("PygestureMainWindow", "Process", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.testTab), _translate("PygestureMainWindow", "Test", None))
        self.menu_File.setTitle(_translate("PygestureMainWindow", "&File", None))
        self.menu_View.setTitle(_translate("PygestureMainWindow", "&View", None))
        self.toolBar.setWindowTitle(_translate("PygestureMainWindow", "toolBar", None))
        self.mainDock.setWindowTitle(_translate("PygestureMainWindow", "Session", None))
        self.participantLabel.setText(_translate("PygestureMainWindow", "Participant:", None))
        self.sessionLabel.setText(_translate("PygestureMainWindow", "Session:", None))
        self.action_Quit.setText(_translate("PygestureMainWindow", "&Quit", None))
        self.actionCheck_Signals.setText(_translate("PygestureMainWindow", "Check Signals", None))
        self.actionProbe.setText(_translate("PygestureMainWindow", "Probe", None))

