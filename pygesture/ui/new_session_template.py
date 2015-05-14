# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pygesture/ui/new_session_template.ui'
#
# Created: Thu May 14 15:22:10 2015
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

class Ui_NewSessionDialog(object):
    def setupUi(self, NewSessionDialog):
        NewSessionDialog.setObjectName(_fromUtf8("NewSessionDialog"))
        NewSessionDialog.setWindowModality(QtCore.Qt.NonModal)
        NewSessionDialog.resize(328, 163)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(NewSessionDialog.sizePolicy().hasHeightForWidth())
        NewSessionDialog.setSizePolicy(sizePolicy)
        NewSessionDialog.setSizeGripEnabled(False)
        NewSessionDialog.setModal(True)
        self.gridLayout = QtGui.QGridLayout(NewSessionDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.participantLabel = QtGui.QLabel(NewSessionDialog)
        self.participantLabel.setObjectName(_fromUtf8("participantLabel"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.participantLabel)
        self.participantLineEdit = QtGui.QLineEdit(NewSessionDialog)
        self.participantLineEdit.setObjectName(_fromUtf8("participantLineEdit"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.participantLineEdit)
        self.sessionLabel = QtGui.QLabel(NewSessionDialog)
        self.sessionLabel.setObjectName(_fromUtf8("sessionLabel"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.sessionLabel)
        self.sessionLineEdit = QtGui.QLineEdit(NewSessionDialog)
        self.sessionLineEdit.setObjectName(_fromUtf8("sessionLineEdit"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.sessionLineEdit)
        self.configurationLabel = QtGui.QLabel(NewSessionDialog)
        self.configurationLabel.setObjectName(_fromUtf8("configurationLabel"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.configurationLabel)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.armRadioButton = QtGui.QRadioButton(NewSessionDialog)
        self.armRadioButton.setChecked(True)
        self.armRadioButton.setObjectName(_fromUtf8("armRadioButton"))
        self.configurationGroup = QtGui.QButtonGroup(NewSessionDialog)
        self.configurationGroup.setObjectName(_fromUtf8("configurationGroup"))
        self.configurationGroup.addButton(self.armRadioButton)
        self.horizontalLayout.addWidget(self.armRadioButton)
        self.legRadioButton = QtGui.QRadioButton(NewSessionDialog)
        self.legRadioButton.setObjectName(_fromUtf8("legRadioButton"))
        self.configurationGroup.addButton(self.legRadioButton)
        self.horizontalLayout.addWidget(self.legRadioButton)
        self.formLayout.setLayout(2, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(NewSessionDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(NewSessionDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), NewSessionDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), NewSessionDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NewSessionDialog)
        NewSessionDialog.setTabOrder(self.participantLineEdit, self.sessionLineEdit)
        NewSessionDialog.setTabOrder(self.sessionLineEdit, self.armRadioButton)
        NewSessionDialog.setTabOrder(self.armRadioButton, self.legRadioButton)

    def retranslateUi(self, NewSessionDialog):
        NewSessionDialog.setWindowTitle(_translate("NewSessionDialog", "New Session", None))
        self.participantLabel.setText(_translate("NewSessionDialog", "Participant ID:", None))
        self.sessionLabel.setText(_translate("NewSessionDialog", "Session ID:", None))
        self.configurationLabel.setText(_translate("NewSessionDialog", "Configuration:", None))
        self.armRadioButton.setText(_translate("NewSessionDialog", "arm", None))
        self.legRadioButton.setText(_translate("NewSessionDialog", "leg", None))

