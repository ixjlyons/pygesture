# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pygesture/ui/signal_widget_template.ui'
#
# Created: Thu May 14 12:33:43 2015
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

class Ui_SignalWidget(object):
    def setupUi(self, SignalWidget):
        SignalWidget.setObjectName(_fromUtf8("SignalWidget"))
        SignalWidget.resize(650, 511)
        self.gridLayout = QtGui.QGridLayout(SignalWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.plotWidget = GraphicsLayoutWidget(SignalWidget)
        self.plotWidget.setObjectName(_fromUtf8("plotWidget"))
        self.horizontalLayout_2.addWidget(self.plotWidget)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.hMinusButton = QtGui.QPushButton(SignalWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hMinusButton.sizePolicy().hasHeightForWidth())
        self.hMinusButton.setSizePolicy(sizePolicy)
        self.hMinusButton.setMinimumSize(QtCore.QSize(30, 30))
        self.hMinusButton.setMaximumSize(QtCore.QSize(30, 30))
        self.hMinusButton.setFlat(False)
        self.hMinusButton.setObjectName(_fromUtf8("hMinusButton"))
        self.horizontalLayout.addWidget(self.hMinusButton)
        self.hPlusButton = QtGui.QPushButton(SignalWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hPlusButton.sizePolicy().hasHeightForWidth())
        self.hPlusButton.setSizePolicy(sizePolicy)
        self.hPlusButton.setMinimumSize(QtCore.QSize(30, 30))
        self.hPlusButton.setMaximumSize(QtCore.QSize(30, 30))
        self.hPlusButton.setObjectName(_fromUtf8("hPlusButton"))
        self.horizontalLayout.addWidget(self.hPlusButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.groupBox = QtGui.QGroupBox(SignalWidget)
        self.groupBox.setMinimumSize(QtCore.QSize(200, 0))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.probeButton = QtGui.QRadioButton(self.groupBox)
        self.probeButton.setChecked(True)
        self.probeButton.setObjectName(_fromUtf8("probeButton"))
        self.buttonGroup = QtGui.QButtonGroup(SignalWidget)
        self.buttonGroup.setObjectName(_fromUtf8("buttonGroup"))
        self.buttonGroup.addButton(self.probeButton)
        self.verticalLayout_3.addWidget(self.probeButton)
        self.signalButton = QtGui.QRadioButton(self.groupBox)
        self.signalButton.setObjectName(_fromUtf8("signalButton"))
        self.buttonGroup.addButton(self.signalButton)
        self.verticalLayout_3.addWidget(self.signalButton)
        spacerItem = QtGui.QSpacerItem(20, 400, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.gridLayout.addWidget(self.groupBox, 0, 1, 1, 1)

        self.retranslateUi(SignalWidget)
        QtCore.QMetaObject.connectSlotsByName(SignalWidget)

    def retranslateUi(self, SignalWidget):
        SignalWidget.setWindowTitle(_translate("SignalWidget", "Form", None))
        self.hMinusButton.setText(_translate("SignalWidget", "-", None))
        self.hPlusButton.setText(_translate("SignalWidget", "+", None))
        self.groupBox.setTitle(_translate("SignalWidget", "Control", None))
        self.probeButton.setText(_translate("SignalWidget", "Probe", None))
        self.signalButton.setText(_translate("SignalWidget", "Signals", None))

from pyqtgraph import GraphicsLayoutWidget