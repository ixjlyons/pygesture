# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pygesture/ui/process_widget_template.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ProcessWidget(object):
    def setupUi(self, ProcessWidget):
        ProcessWidget.setObjectName("ProcessWidget")
        ProcessWidget.resize(823, 539)
        self.gridLayout_2 = QtWidgets.QGridLayout(ProcessWidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.titleLabel = QtWidgets.QLabel(ProcessWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleLabel.sizePolicy().hasHeightForWidth())
        self.titleLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.titleLabel.setFont(font)
        self.titleLabel.setText("")
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setObjectName("titleLabel")
        self.verticalLayout.addWidget(self.titleLabel)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(ProcessWidget)
        self.groupBox.setMinimumSize(QtCore.QSize(200, 0))
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.processButton = QtWidgets.QPushButton(self.groupBox)
        self.processButton.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.processButton.sizePolicy().hasHeightForWidth())
        self.processButton.setSizePolicy(sizePolicy)
        self.processButton.setObjectName("processButton")
        self.gridLayout.addWidget(self.processButton, 1, 1, 1, 1)
        self.sessionList = QtWidgets.QListWidget(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sessionList.sizePolicy().hasHeightForWidth())
        self.sessionList.setSizePolicy(sizePolicy)
        self.sessionList.setProperty("showDropIndicator", False)
        self.sessionList.setAlternatingRowColors(True)
        self.sessionList.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.sessionList.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.sessionList.setResizeMode(QtWidgets.QListView.Fixed)
        self.sessionList.setViewMode(QtWidgets.QListView.ListMode)
        self.sessionList.setObjectName("sessionList")
        self.gridLayout.addWidget(self.sessionList, 0, 1, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(self.groupBox)
        self.progressBar.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy)
        self.progressBar.setMaximum(1)
        self.progressBar.setProperty("value", 1)
        self.progressBar.setTextVisible(True)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setFormat("")
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 2, 1, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 0, 1, 1, 1)

        self.retranslateUi(ProcessWidget)
        QtCore.QMetaObject.connectSlotsByName(ProcessWidget)

    def retranslateUi(self, ProcessWidget):
        _translate = QtCore.QCoreApplication.translate
        ProcessWidget.setWindowTitle(_translate("ProcessWidget", "Form"))
        self.groupBox.setTitle(_translate("ProcessWidget", "Sessions"))
        self.processButton.setText(_translate("ProcessWidget", "Process"))

