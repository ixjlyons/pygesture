# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'recording_viewer_template.ui'
#
# Created by: PyQt5 UI code generator 5.5
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_RecordingViewerWidget(object):
    def setupUi(self, RecordingViewerWidget):
        RecordingViewerWidget.setObjectName("RecordingViewerWidget")
        RecordingViewerWidget.resize(489, 402)
        self.gridLayout_2 = QtWidgets.QGridLayout(RecordingViewerWidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.titleLabel = QtWidgets.QLabel(RecordingViewerWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
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
        self.plotWidget = GraphicsLayoutWidget(RecordingViewerWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.plotWidget.sizePolicy().hasHeightForWidth())
        self.plotWidget.setSizePolicy(sizePolicy)
        self.plotWidget.setObjectName("plotWidget")
        self.verticalLayout.addWidget(self.plotWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.previousButton = QtWidgets.QPushButton(RecordingViewerWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.previousButton.sizePolicy().hasHeightForWidth())
        self.previousButton.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon.fromTheme("go-previous")
        self.previousButton.setIcon(icon)
        self.previousButton.setObjectName("previousButton")
        self.horizontalLayout.addWidget(self.previousButton)
        self.nextButton = QtWidgets.QPushButton(RecordingViewerWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nextButton.sizePolicy().hasHeightForWidth())
        self.nextButton.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon.fromTheme("go-next")
        self.nextButton.setIcon(icon)
        self.nextButton.setObjectName("nextButton")
        self.horizontalLayout.addWidget(self.nextButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(RecordingViewerWidget)
        self.groupBox.setMinimumSize(QtCore.QSize(250, 0))
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.sessionBrowser = SessionBrowser(self.groupBox)
        self.sessionBrowser.setObjectName("sessionBrowser")
        self.gridLayout.addWidget(self.sessionBrowser, 0, 0, 1, 1)
        self.conditionedCheckBox = QtWidgets.QCheckBox(self.groupBox)
        self.conditionedCheckBox.setObjectName("conditionedCheckBox")
        self.gridLayout.addWidget(self.conditionedCheckBox, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 0, 1, 1, 1)

        self.retranslateUi(RecordingViewerWidget)
        QtCore.QMetaObject.connectSlotsByName(RecordingViewerWidget)

    def retranslateUi(self, RecordingViewerWidget):
        _translate = QtCore.QCoreApplication.translate
        RecordingViewerWidget.setWindowTitle(_translate("RecordingViewerWidget", "Form"))
        self.previousButton.setText(_translate("RecordingViewerWidget", "Prev"))
        self.nextButton.setText(_translate("RecordingViewerWidget", "Next"))
        self.groupBox.setTitle(_translate("RecordingViewerWidget", "Sessions"))
        self.conditionedCheckBox.setText(_translate("RecordingViewerWidget", "Conditioned"))

from pygesture.ui.widgets import SessionBrowser
from pyqtgraph import GraphicsLayoutWidget
