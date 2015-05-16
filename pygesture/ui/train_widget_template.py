# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pygesture/ui/train_widget_template.ui'
#
# Created: Fri May 15 17:42:27 2015
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

class Ui_TrainWidget(object):
    def setupUi(self, TrainWidget):
        TrainWidget.setObjectName(_fromUtf8("TrainWidget"))
        TrainWidget.resize(698, 325)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(TrainWidget)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.frame_2 = QtGui.QFrame(TrainWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.gridLayout = QtGui.QGridLayout(self.frame_2)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.promptWidget = PromptWidget(self.frame_2)
        self.promptWidget.setMinimumSize(QtCore.QSize(0, 40))
        self.promptWidget.setProperty("value", 0)
        self.promptWidget.setTextVisible(False)
        self.promptWidget.setOrientation(QtCore.Qt.Horizontal)
        self.promptWidget.setObjectName(_fromUtf8("promptWidget"))
        self.gridLayout.addWidget(self.promptWidget, 1, 0, 1, 1)
        self.gestureView = GestureView(self.frame_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gestureView.sizePolicy().hasHeightForWidth())
        self.gestureView.setSizePolicy(sizePolicy)
        self.gestureView.setObjectName(_fromUtf8("gestureView"))
        self.gridLayout.addWidget(self.gestureView, 0, 0, 1, 1)
        self.horizontalLayout_2.addWidget(self.frame_2)
        self.frame = QtGui.QFrame(TrainWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(200, 0))
        self.frame.setMaximumSize(QtCore.QSize(250, 16777215))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setMidLineWidth(0)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout_3 = QtGui.QGridLayout(self.frame)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        spacerItem = QtGui.QSpacerItem(17, 85, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem, 1, 0, 1, 1)
        self.statusBox = QtGui.QGroupBox(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statusBox.sizePolicy().hasHeightForWidth())
        self.statusBox.setSizePolicy(sizePolicy)
        self.statusBox.setObjectName(_fromUtf8("statusBox"))
        self.gridLayout_5 = QtGui.QGridLayout(self.statusBox)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.sessionProgressBar = QtGui.QProgressBar(self.statusBox)
        self.sessionProgressBar.setProperty("value", 24)
        self.sessionProgressBar.setObjectName(_fromUtf8("sessionProgressBar"))
        self.gridLayout_5.addWidget(self.sessionProgressBar, 1, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.startButton = QtGui.QPushButton(self.statusBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.startButton.sizePolicy().hasHeightForWidth())
        self.startButton.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("media-playback-start"))
        self.startButton.setIcon(icon)
        self.startButton.setObjectName(_fromUtf8("startButton"))
        self.horizontalLayout.addWidget(self.startButton)
        self.pauseButton = QtGui.QPushButton(self.statusBox)
        self.pauseButton.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pauseButton.sizePolicy().hasHeightForWidth())
        self.pauseButton.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("media-playback-pause"))
        self.pauseButton.setIcon(icon)
        self.pauseButton.setObjectName(_fromUtf8("pauseButton"))
        self.horizontalLayout.addWidget(self.pauseButton)
        self.gridLayout_5.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.statusBox, 0, 0, 1, 1)
        self.horizontalLayout_2.addWidget(self.frame)

        self.retranslateUi(TrainWidget)
        QtCore.QMetaObject.connectSlotsByName(TrainWidget)

    def retranslateUi(self, TrainWidget):
        TrainWidget.setWindowTitle(_translate("TrainWidget", "Form", None))
        self.statusBox.setTitle(_translate("TrainWidget", "Controls", None))
        self.sessionProgressBar.setFormat(_translate("TrainWidget", "Trial: %v / %m", None))
        self.startButton.setText(_translate("TrainWidget", "Start", None))
        self.pauseButton.setText(_translate("TrainWidget", "Pause", None))

from pygesture.ui.widgets import PromptWidget, GestureView
