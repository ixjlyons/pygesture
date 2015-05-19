# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pygesture/ui/new_session_template.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_NewSessionDialog(object):
    def setupUi(self, NewSessionDialog):
        NewSessionDialog.setObjectName("NewSessionDialog")
        NewSessionDialog.setWindowModality(QtCore.Qt.NonModal)
        NewSessionDialog.resize(328, 163)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(NewSessionDialog.sizePolicy().hasHeightForWidth())
        NewSessionDialog.setSizePolicy(sizePolicy)
        NewSessionDialog.setSizeGripEnabled(False)
        NewSessionDialog.setModal(True)
        self.gridLayout = QtWidgets.QGridLayout(NewSessionDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.participantLabel = QtWidgets.QLabel(NewSessionDialog)
        self.participantLabel.setObjectName("participantLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.participantLabel)
        self.participantLineEdit = QtWidgets.QLineEdit(NewSessionDialog)
        self.participantLineEdit.setObjectName("participantLineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.participantLineEdit)
        self.sessionLabel = QtWidgets.QLabel(NewSessionDialog)
        self.sessionLabel.setObjectName("sessionLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.sessionLabel)
        self.sessionLineEdit = QtWidgets.QLineEdit(NewSessionDialog)
        self.sessionLineEdit.setObjectName("sessionLineEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.sessionLineEdit)
        self.configurationLabel = QtWidgets.QLabel(NewSessionDialog)
        self.configurationLabel.setObjectName("configurationLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.configurationLabel)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.armRadioButton = QtWidgets.QRadioButton(NewSessionDialog)
        self.armRadioButton.setChecked(True)
        self.armRadioButton.setObjectName("armRadioButton")
        self.configurationGroup = QtWidgets.QButtonGroup(NewSessionDialog)
        self.configurationGroup.setObjectName("configurationGroup")
        self.configurationGroup.addButton(self.armRadioButton)
        self.horizontalLayout.addWidget(self.armRadioButton)
        self.legRadioButton = QtWidgets.QRadioButton(NewSessionDialog)
        self.legRadioButton.setObjectName("legRadioButton")
        self.configurationGroup.addButton(self.legRadioButton)
        self.horizontalLayout.addWidget(self.legRadioButton)
        self.formLayout.setLayout(2, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)
        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(NewSessionDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(NewSessionDialog)
        self.buttonBox.accepted.connect(NewSessionDialog.accept)
        self.buttonBox.rejected.connect(NewSessionDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NewSessionDialog)
        NewSessionDialog.setTabOrder(self.participantLineEdit, self.sessionLineEdit)
        NewSessionDialog.setTabOrder(self.sessionLineEdit, self.armRadioButton)
        NewSessionDialog.setTabOrder(self.armRadioButton, self.legRadioButton)

    def retranslateUi(self, NewSessionDialog):
        _translate = QtCore.QCoreApplication.translate
        NewSessionDialog.setWindowTitle(_translate("NewSessionDialog", "New Session"))
        self.participantLabel.setText(_translate("NewSessionDialog", "Participant ID:"))
        self.sessionLabel.setText(_translate("NewSessionDialog", "Session ID:"))
        self.configurationLabel.setText(_translate("NewSessionDialog", "Configuration:"))
        self.armRadioButton.setText(_translate("NewSessionDialog", "arm"))
        self.legRadioButton.setText(_translate("NewSessionDialog", "leg"))

