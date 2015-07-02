# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pygesture/ui/main_template.ui'
#
# Created by: PyQt5 UI code generator 5.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_PygestureMainWindow(object):
    def setupUi(self, PygestureMainWindow):
        PygestureMainWindow.setObjectName("PygestureMainWindow")
        PygestureMainWindow.resize(1004, 652)
        PygestureMainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(PygestureMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setStyleSheet("")
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setObjectName("tabWidget")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        PygestureMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(PygestureMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1004, 27))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        PygestureMainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(PygestureMainWindow)
        self.statusbar.setObjectName("statusbar")
        PygestureMainWindow.setStatusBar(self.statusbar)
        self.actionQuit = QtWidgets.QAction(PygestureMainWindow)
        icon = QtGui.QIcon.fromTheme("application-exit")
        self.actionQuit.setIcon(icon)
        self.actionQuit.setObjectName("actionQuit")
        self.actionNew = QtWidgets.QAction(PygestureMainWindow)
        icon = QtGui.QIcon.fromTheme("document-new")
        self.actionNew.setIcon(icon)
        self.actionNew.setObjectName("actionNew")
        self.menu_File.addAction(self.actionNew)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.actionQuit)
        self.menubar.addAction(self.menu_File.menuAction())

        self.retranslateUi(PygestureMainWindow)
        self.tabWidget.setCurrentIndex(-1)
        self.actionQuit.triggered.connect(PygestureMainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(PygestureMainWindow)

    def retranslateUi(self, PygestureMainWindow):
        _translate = QtCore.QCoreApplication.translate
        PygestureMainWindow.setWindowTitle(_translate("PygestureMainWindow", "PyGesture"))
        self.menu_File.setTitle(_translate("PygestureMainWindow", "&File"))
        self.actionQuit.setText(_translate("PygestureMainWindow", "&Quit"))
        self.actionNew.setText(_translate("PygestureMainWindow", "&New"))
        self.actionNew.setShortcut(_translate("PygestureMainWindow", "Ctrl+N"))

