# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pygesture/ui/signal_widget_template.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SignalWidget(object):
    def setupUi(self, SignalWidget):
        SignalWidget.setObjectName("SignalWidget")
        SignalWidget.resize(650, 511)
        self.gridLayout = QtWidgets.QGridLayout(SignalWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.plotWidget = GraphicsLayoutWidget(SignalWidget)
        self.plotWidget.setObjectName("plotWidget")
        self.horizontalLayout_2.addWidget(self.plotWidget)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.hMinusButton = QtWidgets.QPushButton(SignalWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hMinusButton.sizePolicy().hasHeightForWidth())
        self.hMinusButton.setSizePolicy(sizePolicy)
        self.hMinusButton.setMinimumSize(QtCore.QSize(30, 30))
        self.hMinusButton.setMaximumSize(QtCore.QSize(30, 30))
        self.hMinusButton.setFlat(False)
        self.hMinusButton.setObjectName("hMinusButton")
        self.horizontalLayout.addWidget(self.hMinusButton)
        self.hPlusButton = QtWidgets.QPushButton(SignalWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hPlusButton.sizePolicy().hasHeightForWidth())
        self.hPlusButton.setSizePolicy(sizePolicy)
        self.hPlusButton.setMinimumSize(QtCore.QSize(30, 30))
        self.hPlusButton.setMaximumSize(QtCore.QSize(30, 30))
        self.hPlusButton.setObjectName("hPlusButton")
        self.horizontalLayout.addWidget(self.hPlusButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(SignalWidget)
        self.groupBox.setMinimumSize(QtCore.QSize(200, 0))
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.probeButton = QtWidgets.QRadioButton(self.groupBox)
        self.probeButton.setChecked(True)
        self.probeButton.setObjectName("probeButton")
        self.buttonGroup = QtWidgets.QButtonGroup(SignalWidget)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.probeButton)
        self.verticalLayout_3.addWidget(self.probeButton)
        self.signalButton = QtWidgets.QRadioButton(self.groupBox)
        self.signalButton.setObjectName("signalButton")
        self.buttonGroup.addButton(self.signalButton)
        self.verticalLayout_3.addWidget(self.signalButton)
        spacerItem = QtWidgets.QSpacerItem(20, 400, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.gridLayout.addWidget(self.groupBox, 0, 1, 1, 1)

        self.retranslateUi(SignalWidget)
        QtCore.QMetaObject.connectSlotsByName(SignalWidget)

    def retranslateUi(self, SignalWidget):
        _translate = QtCore.QCoreApplication.translate
        SignalWidget.setWindowTitle(_translate("SignalWidget", "Form"))
        self.hMinusButton.setText(_translate("SignalWidget", "-"))
        self.hPlusButton.setText(_translate("SignalWidget", "+"))
        self.groupBox.setTitle(_translate("SignalWidget", "Control"))
        self.probeButton.setText(_translate("SignalWidget", "Probe"))
        self.signalButton.setText(_translate("SignalWidget", "Signals"))

from pyqtgraph import GraphicsLayoutWidget
