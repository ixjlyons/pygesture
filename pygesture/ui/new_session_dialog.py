# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pygesture/ui/new_session_dialog.ui'
#
# Created: Wed May 13 12:29:21 2015
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
        NewSessionDialog.resize(313, 219)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(NewSessionDialog.sizePolicy().hasHeightForWidth())
        NewSessionDialog.setSizePolicy(sizePolicy)
        NewSessionDialog.setSizeGripEnabled(False)
        NewSessionDialog.setModal(True)
        self.gridLayout = QtGui.QGridLayout(NewSessionDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.sessionInfoBox = QtGui.QGroupBox(NewSessionDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sessionInfoBox.sizePolicy().hasHeightForWidth())
        self.sessionInfoBox.setSizePolicy(sizePolicy)
        self.sessionInfoBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.sessionInfoBox.setFlat(False)
        self.sessionInfoBox.setCheckable(False)
        self.sessionInfoBox.setObjectName(_fromUtf8("sessionInfoBox"))
        self.gridLayout_4 = QtGui.QGridLayout(self.sessionInfoBox)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.participantLabel = QtGui.QLabel(self.sessionInfoBox)
        self.participantLabel.setObjectName(_fromUtf8("participantLabel"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.participantLabel)
        self.participantLineEdit = QtGui.QLineEdit(self.sessionInfoBox)
        self.participantLineEdit.setObjectName(_fromUtf8("participantLineEdit"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.participantLineEdit)
        self.sessionLabel = QtGui.QLabel(self.sessionInfoBox)
        self.sessionLabel.setObjectName(_fromUtf8("sessionLabel"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.sessionLabel)
        self.sessionLineEdit = QtGui.QLineEdit(self.sessionInfoBox)
        self.sessionLineEdit.setObjectName(_fromUtf8("sessionLineEdit"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.sessionLineEdit)
        self.gridLayout_4.addLayout(self.formLayout, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.sessionInfoBox, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(NewSessionDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(NewSessionDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), NewSessionDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), NewSessionDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NewSessionDialog)

    def retranslateUi(self, NewSessionDialog):
        NewSessionDialog.setWindowTitle(_translate("NewSessionDialog", "New Session", None))
        self.sessionInfoBox.setTitle(_translate("NewSessionDialog", "Session Info", None))
        self.participantLabel.setText(_translate("NewSessionDialog", "Participant:", None))
        self.sessionLabel.setText(_translate("NewSessionDialog", "Session:", None))

