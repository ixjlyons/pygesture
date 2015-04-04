# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pygesture/ui/signal_dialog_template.ui'
#
# Created: Fri Apr  3 15:36:36 2015
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

class Ui_SignalDialog(object):
    def setupUi(self, SignalDialog):
        SignalDialog.setObjectName(_fromUtf8("SignalDialog"))
        SignalDialog.resize(704, 484)
        self.gridLayout = QtGui.QGridLayout(SignalDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.plotWidget = PlotWidget(SignalDialog)
        self.plotWidget.setObjectName(_fromUtf8("plotWidget"))
        self.horizontalLayout_2.addWidget(self.plotWidget)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.vPlusButton = QtGui.QPushButton(SignalDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vPlusButton.sizePolicy().hasHeightForWidth())
        self.vPlusButton.setSizePolicy(sizePolicy)
        self.vPlusButton.setMinimumSize(QtCore.QSize(30, 30))
        self.vPlusButton.setMaximumSize(QtCore.QSize(30, 30))
        self.vPlusButton.setObjectName(_fromUtf8("vPlusButton"))
        self.verticalLayout.addWidget(self.vPlusButton)
        self.vMinusButton = QtGui.QPushButton(SignalDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vMinusButton.sizePolicy().hasHeightForWidth())
        self.vMinusButton.setSizePolicy(sizePolicy)
        self.vMinusButton.setMinimumSize(QtCore.QSize(30, 30))
        self.vMinusButton.setMaximumSize(QtCore.QSize(30, 30))
        self.vMinusButton.setObjectName(_fromUtf8("vMinusButton"))
        self.verticalLayout.addWidget(self.vMinusButton)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.hMinusButton = QtGui.QPushButton(SignalDialog)
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
        self.hPlusButton = QtGui.QPushButton(SignalDialog)
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

        self.retranslateUi(SignalDialog)
        QtCore.QMetaObject.connectSlotsByName(SignalDialog)

    def retranslateUi(self, SignalDialog):
        SignalDialog.setWindowTitle(_translate("SignalDialog", "Dialog", None))
        self.vPlusButton.setText(_translate("SignalDialog", "+", None))
        self.vMinusButton.setText(_translate("SignalDialog", "-", None))
        self.hMinusButton.setText(_translate("SignalDialog", "-", None))
        self.hPlusButton.setText(_translate("SignalDialog", "+", None))

from pyqtgraph import PlotWidget
