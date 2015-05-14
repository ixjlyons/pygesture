# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pygesture/ui/process_widget.ui'
#
# Created: Thu May 14 11:44:14 2015
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

class Ui_ProcessWidget(object):
    def setupUi(self, ProcessWidget):
        ProcessWidget.setObjectName(_fromUtf8("ProcessWidget"))
        ProcessWidget.resize(823, 539)
        self.gridLayout_2 = QtGui.QGridLayout(ProcessWidget)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.titleLabel = QtGui.QLabel(ProcessWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleLabel.sizePolicy().hasHeightForWidth())
        self.titleLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.titleLabel.setFont(font)
        self.titleLabel.setText(_fromUtf8(""))
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setObjectName(_fromUtf8("titleLabel"))
        self.verticalLayout.addWidget(self.titleLabel)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.groupBox = QtGui.QGroupBox(ProcessWidget)
        self.groupBox.setMinimumSize(QtCore.QSize(200, 0))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.processButton = QtGui.QPushButton(self.groupBox)
        self.processButton.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.processButton.sizePolicy().hasHeightForWidth())
        self.processButton.setSizePolicy(sizePolicy)
        self.processButton.setObjectName(_fromUtf8("processButton"))
        self.gridLayout.addWidget(self.processButton, 1, 1, 1, 1)
        self.sessionList = QtGui.QListWidget(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sessionList.sizePolicy().hasHeightForWidth())
        self.sessionList.setSizePolicy(sizePolicy)
        self.sessionList.setProperty("showDropIndicator", False)
        self.sessionList.setAlternatingRowColors(True)
        self.sessionList.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.sessionList.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        self.sessionList.setResizeMode(QtGui.QListView.Fixed)
        self.sessionList.setViewMode(QtGui.QListView.ListMode)
        self.sessionList.setObjectName(_fromUtf8("sessionList"))
        self.gridLayout.addWidget(self.sessionList, 0, 1, 1, 1)
        self.progressBar = QtGui.QProgressBar(self.groupBox)
        self.progressBar.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy)
        self.progressBar.setMaximum(1)
        self.progressBar.setProperty("value", 1)
        self.progressBar.setTextVisible(True)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setFormat(_fromUtf8(""))
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout.addWidget(self.progressBar, 2, 1, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 0, 1, 1, 1)

        self.retranslateUi(ProcessWidget)
        QtCore.QMetaObject.connectSlotsByName(ProcessWidget)

    def retranslateUi(self, ProcessWidget):
        ProcessWidget.setWindowTitle(_translate("ProcessWidget", "Form", None))
        self.groupBox.setTitle(_translate("ProcessWidget", "Sessions", None))
        self.processButton.setText(_translate("ProcessWidget", "Process", None))

