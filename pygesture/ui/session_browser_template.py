# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pygesture/ui/session_browser_template.ui'
#
# Created by: PyQt5 UI code generator 5.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SessionBrowser(object):
    def setupUi(self, SessionBrowser):
        SessionBrowser.setObjectName("SessionBrowser")
        SessionBrowser.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(SessionBrowser)
        self.gridLayout.setObjectName("gridLayout")
        self.hlayout = QtWidgets.QHBoxLayout()
        self.hlayout.setObjectName("hlayout")
        self.participantLabel = QtWidgets.QLabel(SessionBrowser)
        self.participantLabel.setObjectName("participantLabel")
        self.hlayout.addWidget(self.participantLabel)
        self.participantComboBox = QtWidgets.QComboBox(SessionBrowser)
        self.participantComboBox.setObjectName("participantComboBox")
        self.hlayout.addWidget(self.participantComboBox)
        self.gridLayout.addLayout(self.hlayout, 0, 0, 1, 1)
        self.sessionList = QtWidgets.QListWidget(SessionBrowser)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sessionList.sizePolicy().hasHeightForWidth())
        self.sessionList.setSizePolicy(sizePolicy)
        self.sessionList.setProperty("showDropIndicator", False)
        self.sessionList.setAlternatingRowColors(True)
        self.sessionList.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.sessionList.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.sessionList.setResizeMode(QtWidgets.QListView.Fixed)
        self.sessionList.setObjectName("sessionList")
        self.gridLayout.addWidget(self.sessionList, 1, 0, 1, 1)

        self.retranslateUi(SessionBrowser)
        QtCore.QMetaObject.connectSlotsByName(SessionBrowser)

    def retranslateUi(self, SessionBrowser):
        _translate = QtCore.QCoreApplication.translate
        SessionBrowser.setWindowTitle(_translate("SessionBrowser", "Form"))
        self.participantLabel.setText(_translate("SessionBrowser", "Participant:"))

