# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pygesture/ui/recording_viewer_template.ui'
#
# Created: Thu May 14 12:38:53 2015
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

class Ui_RecordingViewerWidget(object):
    def setupUi(self, RecordingViewerWidget):
        RecordingViewerWidget.setObjectName(_fromUtf8("RecordingViewerWidget"))
        RecordingViewerWidget.resize(489, 402)
        self.gridLayout_2 = QtGui.QGridLayout(RecordingViewerWidget)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.titleLabel = QtGui.QLabel(RecordingViewerWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
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
        self.plotWidget = GraphicsLayoutWidget(RecordingViewerWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.plotWidget.sizePolicy().hasHeightForWidth())
        self.plotWidget.setSizePolicy(sizePolicy)
        self.plotWidget.setObjectName(_fromUtf8("plotWidget"))
        self.verticalLayout.addWidget(self.plotWidget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.previousButton = QtGui.QPushButton(RecordingViewerWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.previousButton.sizePolicy().hasHeightForWidth())
        self.previousButton.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("go-previous"))
        self.previousButton.setIcon(icon)
        self.previousButton.setObjectName(_fromUtf8("previousButton"))
        self.horizontalLayout.addWidget(self.previousButton)
        self.nextButton = QtGui.QPushButton(RecordingViewerWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nextButton.sizePolicy().hasHeightForWidth())
        self.nextButton.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("go-next"))
        self.nextButton.setIcon(icon)
        self.nextButton.setObjectName(_fromUtf8("nextButton"))
        self.horizontalLayout.addWidget(self.nextButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.groupBox = QtGui.QGroupBox(RecordingViewerWidget)
        self.groupBox.setMinimumSize(QtCore.QSize(200, 0))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
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
        self.sessionList.setObjectName(_fromUtf8("sessionList"))
        self.gridLayout.addWidget(self.sessionList, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 0, 1, 1, 1)

        self.retranslateUi(RecordingViewerWidget)
        QtCore.QMetaObject.connectSlotsByName(RecordingViewerWidget)

    def retranslateUi(self, RecordingViewerWidget):
        RecordingViewerWidget.setWindowTitle(_translate("RecordingViewerWidget", "Form", None))
        self.previousButton.setText(_translate("RecordingViewerWidget", "Prev", None))
        self.nextButton.setText(_translate("RecordingViewerWidget", "Next", None))
        self.groupBox.setTitle(_translate("RecordingViewerWidget", "Sessions", None))

from pyqtgraph import GraphicsLayoutWidget
