# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pygesture/ui/test_widget.ui'
#
# Created: Wed May 13 14:04:00 2015
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

class Ui_TestWidget(object):
    def setupUi(self, TestWidget):
        TestWidget.setObjectName(_fromUtf8("TestWidget"))
        TestWidget.resize(678, 454)
        self.horizontalLayout_3 = QtGui.QHBoxLayout(TestWidget)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.frame_2 = QtGui.QFrame(TestWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.frame_2)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gestureDisplayLabel = GestureView(self.frame_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gestureDisplayLabel.sizePolicy().hasHeightForWidth())
        self.gestureDisplayLabel.setSizePolicy(sizePolicy)
        self.gestureDisplayLabel.setFrameShape(QtGui.QFrame.NoFrame)
        self.gestureDisplayLabel.setText(_fromUtf8(""))
        self.gestureDisplayLabel.setScaledContents(False)
        self.gestureDisplayLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.gestureDisplayLabel.setObjectName(_fromUtf8("gestureDisplayLabel"))
        self.gridLayout_2.addWidget(self.gestureDisplayLabel, 0, 0, 1, 1)
        self.horizontalLayout_3.addWidget(self.frame_2)
        self.frame = QtGui.QFrame(TestWidget)
        self.frame.setMinimumSize(QtCore.QSize(200, 0))
        self.frame.setMaximumSize(QtCore.QSize(250, 16777215))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout = QtGui.QGridLayout(self.frame)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.connectButton = QtGui.QPushButton(self.frame)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("insert-link"))
        self.connectButton.setIcon(icon)
        self.connectButton.setCheckable(True)
        self.connectButton.setChecked(False)
        self.connectButton.setFlat(False)
        self.connectButton.setObjectName(_fromUtf8("connectButton"))
        self.gridLayout.addWidget(self.connectButton, 2, 0, 1, 1)
        self.startButton = QtGui.QPushButton(self.frame)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("media-playback-start"))
        self.startButton.setIcon(icon)
        self.startButton.setObjectName(_fromUtf8("startButton"))
        self.gridLayout.addWidget(self.startButton, 3, 0, 1, 1)
        self.sessionInfoBox = QtGui.QGroupBox(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sessionInfoBox.sizePolicy().hasHeightForWidth())
        self.sessionInfoBox.setSizePolicy(sizePolicy)
        self.sessionInfoBox.setObjectName(_fromUtf8("sessionInfoBox"))
        self.gridLayout_3 = QtGui.QGridLayout(self.sessionInfoBox)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.classifierLabel = QtGui.QLabel(self.sessionInfoBox)
        self.classifierLabel.setObjectName(_fromUtf8("classifierLabel"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.classifierLabel)
        self.classifierComboBox = QtGui.QComboBox(self.sessionInfoBox)
        self.classifierComboBox.setObjectName(_fromUtf8("classifierComboBox"))
        self.classifierComboBox.addItem(_fromUtf8(""))
        self.classifierComboBox.addItem(_fromUtf8(""))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.classifierComboBox)
        self.trainingLabel = QtGui.QLabel(self.sessionInfoBox)
        self.trainingLabel.setObjectName(_fromUtf8("trainingLabel"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.trainingLabel)
        self.trainingList = QtGui.QListWidget(self.sessionInfoBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.trainingList.sizePolicy().hasHeightForWidth())
        self.trainingList.setSizePolicy(sizePolicy)
        self.trainingList.setProperty("showDropIndicator", False)
        self.trainingList.setAlternatingRowColors(False)
        self.trainingList.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.trainingList.setResizeMode(QtGui.QListView.Fixed)
        self.trainingList.setObjectName(_fromUtf8("trainingList"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.SpanningRole, self.trainingList)
        self.gridLayout_3.addLayout(self.formLayout, 0, 0, 1, 1)
        self.trainButton = QtGui.QPushButton(self.sessionInfoBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.trainButton.sizePolicy().hasHeightForWidth())
        self.trainButton.setSizePolicy(sizePolicy)
        self.trainButton.setDefault(False)
        self.trainButton.setFlat(False)
        self.trainButton.setObjectName(_fromUtf8("trainButton"))
        self.gridLayout_3.addWidget(self.trainButton, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.sessionInfoBox, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.horizontalLayout_3.addWidget(self.frame)

        self.retranslateUi(TestWidget)
        QtCore.QMetaObject.connectSlotsByName(TestWidget)

    def retranslateUi(self, TestWidget):
        TestWidget.setWindowTitle(_translate("TestWidget", "Form", None))
        self.connectButton.setText(_translate("TestWidget", "Connect", None))
        self.startButton.setText(_translate("TestWidget", "Start", None))
        self.sessionInfoBox.setTitle(_translate("TestWidget", "Classification", None))
        self.classifierLabel.setText(_translate("TestWidget", "Classifier:", None))
        self.classifierComboBox.setItemText(0, _translate("TestWidget", "LDA", None))
        self.classifierComboBox.setItemText(1, _translate("TestWidget", "SVM", None))
        self.trainingLabel.setText(_translate("TestWidget", "Training Data:", None))
        self.trainButton.setText(_translate("TestWidget", "Train", None))

from pygesture.ui.widgets import GestureView
