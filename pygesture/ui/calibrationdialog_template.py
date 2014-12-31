# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pygesture/ui/calibrationdialog_template.ui'
#
# Created: Tue Dec 30 18:28:39 2014
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

class Ui_CalibrationDialog(object):
    def setupUi(self, CalibrationDialog):
        CalibrationDialog.setObjectName(_fromUtf8("CalibrationDialog"))
        CalibrationDialog.resize(283, 98)
        CalibrationDialog.setModal(True)
        self.gridLayout = QtGui.QGridLayout(CalibrationDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.buttonBox = QtGui.QDialogButtonBox(CalibrationDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.startButton = QtGui.QPushButton(CalibrationDialog)
        self.startButton.setObjectName(_fromUtf8("startButton"))
        self.horizontalLayout_2.addWidget(self.startButton)
        self.progressBar = QtGui.QProgressBar(CalibrationDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.horizontalLayout_2.addWidget(self.progressBar)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)

        self.retranslateUi(CalibrationDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), CalibrationDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), CalibrationDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(CalibrationDialog)

    def retranslateUi(self, CalibrationDialog):
        CalibrationDialog.setWindowTitle(_translate("CalibrationDialog", "Calibration", None))
        self.startButton.setText(_translate("CalibrationDialog", "Start", None))

