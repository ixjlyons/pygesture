# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pygesture/ui/settings_template.ui'
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

class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        SettingsDialog.setObjectName(_fromUtf8("SettingsDialog"))
        SettingsDialog.resize(548, 374)
        self.verticalLayout = QtGui.QVBoxLayout(SettingsDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pageList = QtGui.QListWidget(SettingsDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pageList.sizePolicy().hasHeightForWidth())
        self.pageList.setSizePolicy(sizePolicy)
        self.pageList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.pageList.setObjectName(_fromUtf8("pageList"))
        item = QtGui.QListWidgetItem()
        self.pageList.addItem(item)
        item = QtGui.QListWidgetItem()
        self.pageList.addItem(item)
        item = QtGui.QListWidgetItem()
        self.pageList.addItem(item)
        item = QtGui.QListWidgetItem()
        self.pageList.addItem(item)
        self.horizontalLayout.addWidget(self.pageList)
        self.stackedWidget = QtGui.QStackedWidget(SettingsDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.stackedWidget.setObjectName(_fromUtf8("stackedWidget"))
        self.daqPage = QtGui.QWidget()
        self.daqPage.setObjectName(_fromUtf8("daqPage"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.daqPage)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.channelsGroup = QtGui.QGroupBox(self.daqPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.channelsGroup.sizePolicy().hasHeightForWidth())
        self.channelsGroup.setSizePolicy(sizePolicy)
        self.channelsGroup.setObjectName(_fromUtf8("channelsGroup"))
        self.formLayout = QtGui.QFormLayout(self.channelsGroup)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.lowChanSpinBox = QtGui.QSpinBox(self.channelsGroup)
        self.lowChanSpinBox.setObjectName(_fromUtf8("lowChanSpinBox"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.lowChanSpinBox)
        self.lowChanLabel = QtGui.QLabel(self.channelsGroup)
        self.lowChanLabel.setObjectName(_fromUtf8("lowChanLabel"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.lowChanLabel)
        self.highChanLabel = QtGui.QLabel(self.channelsGroup)
        self.highChanLabel.setObjectName(_fromUtf8("highChanLabel"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.highChanLabel)
        self.highChanSpinBox = QtGui.QSpinBox(self.channelsGroup)
        self.highChanSpinBox.setObjectName(_fromUtf8("highChanSpinBox"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.highChanSpinBox)
        self.probeChanLabel = QtGui.QLabel(self.channelsGroup)
        self.probeChanLabel.setObjectName(_fromUtf8("probeChanLabel"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.probeChanLabel)
        self.probeChanSpinBox = QtGui.QSpinBox(self.channelsGroup)
        self.probeChanSpinBox.setObjectName(_fromUtf8("probeChanSpinBox"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.probeChanSpinBox)
        self.inputRangeSpinBox = QtGui.QComboBox(self.channelsGroup)
        self.inputRangeSpinBox.setObjectName(_fromUtf8("inputRangeSpinBox"))
        self.inputRangeSpinBox.addItem(_fromUtf8(""))
        self.inputRangeSpinBox.addItem(_fromUtf8(""))
        self.inputRangeSpinBox.addItem(_fromUtf8(""))
        self.inputRangeSpinBox.addItem(_fromUtf8(""))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.inputRangeSpinBox)
        self.inputRangeLabel = QtGui.QLabel(self.channelsGroup)
        self.inputRangeLabel.setObjectName(_fromUtf8("inputRangeLabel"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.inputRangeLabel)
        self.verticalLayout_2.addWidget(self.channelsGroup)
        self.samplingGroup = QtGui.QGroupBox(self.daqPage)
        self.samplingGroup.setObjectName(_fromUtf8("samplingGroup"))
        self.formLayout_2 = QtGui.QFormLayout(self.samplingGroup)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.sampleRateLabel = QtGui.QLabel(self.samplingGroup)
        self.sampleRateLabel.setObjectName(_fromUtf8("sampleRateLabel"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.sampleRateLabel)
        self.sampleRateSpinbox = QtGui.QSpinBox(self.samplingGroup)
        self.sampleRateSpinbox.setObjectName(_fromUtf8("sampleRateSpinbox"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.sampleRateSpinbox)
        self.sptLabel = QtGui.QLabel(self.samplingGroup)
        self.sptLabel.setObjectName(_fromUtf8("sptLabel"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.sptLabel)
        self.sptSpinBox = QtGui.QSpinBox(self.samplingGroup)
        self.sptSpinBox.setObjectName(_fromUtf8("sptSpinBox"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.sptSpinBox)
        self.verticalLayout_2.addWidget(self.samplingGroup)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.stackedWidget.addWidget(self.daqPage)
        self.processingPage = QtGui.QWidget()
        self.processingPage.setObjectName(_fromUtf8("processingPage"))
        self.stackedWidget.addWidget(self.processingPage)
        self.trainingPage = QtGui.QWidget()
        self.trainingPage.setObjectName(_fromUtf8("trainingPage"))
        self.stackedWidget.addWidget(self.trainingPage)
        self.simulationPage = QtGui.QWidget()
        self.simulationPage.setObjectName(_fromUtf8("simulationPage"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.simulationPage)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.groupBox = QtGui.QGroupBox(self.simulationPage)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.formLayout_3 = QtGui.QFormLayout(self.groupBox)
        self.formLayout_3.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_3.setObjectName(_fromUtf8("formLayout_3"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.lineEdit = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.pushButton = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMinimumSize(QtCore.QSize(30, 0))
        self.pushButton.setMaximumSize(QtCore.QSize(30, 16777215))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.formLayout_3.setLayout(0, QtGui.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_2)
        self.spinBox = QtGui.QSpinBox(self.groupBox)
        self.spinBox.setObjectName(_fromUtf8("spinBox"))
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.FieldRole, self.spinBox)
        self.verticalLayout_3.addWidget(self.groupBox)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.stackedWidget.addWidget(self.simulationPage)
        self.horizontalLayout.addWidget(self.stackedWidget)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtGui.QDialogButtonBox(SettingsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(SettingsDialog)
        self.pageList.setCurrentRow(0)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SettingsDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SettingsDialog.reject)
        QtCore.QObject.connect(self.pageList, QtCore.SIGNAL(_fromUtf8("currentRowChanged(int)")), self.stackedWidget.setCurrentIndex)
        QtCore.QMetaObject.connectSlotsByName(SettingsDialog)

    def retranslateUi(self, SettingsDialog):
        SettingsDialog.setWindowTitle(_translate("SettingsDialog", "Dialog", None))
        __sortingEnabled = self.pageList.isSortingEnabled()
        self.pageList.setSortingEnabled(False)
        item = self.pageList.item(0)
        item.setText(_translate("SettingsDialog", "Data Acquisition", None))
        item = self.pageList.item(1)
        item.setText(_translate("SettingsDialog", "Processing", None))
        item = self.pageList.item(2)
        item.setText(_translate("SettingsDialog", "Training", None))
        item = self.pageList.item(3)
        item.setText(_translate("SettingsDialog", "Simulation", None))
        self.pageList.setSortingEnabled(__sortingEnabled)
        self.channelsGroup.setTitle(_translate("SettingsDialog", "Channels", None))
        self.lowChanLabel.setText(_translate("SettingsDialog", "Low channel:", None))
        self.highChanLabel.setText(_translate("SettingsDialog", "High channel:", None))
        self.probeChanLabel.setText(_translate("SettingsDialog", "Probe channel:", None))
        self.inputRangeSpinBox.setItemText(0, _translate("SettingsDialog", "1V", None))
        self.inputRangeSpinBox.setItemText(1, _translate("SettingsDialog", "2V", None))
        self.inputRangeSpinBox.setItemText(2, _translate("SettingsDialog", "5V", None))
        self.inputRangeSpinBox.setItemText(3, _translate("SettingsDialog", "10V", None))
        self.inputRangeLabel.setText(_translate("SettingsDialog", "Input range:", None))
        self.samplingGroup.setTitle(_translate("SettingsDialog", "Sampling", None))
        self.sampleRateLabel.setText(_translate("SettingsDialog", "Sample rate:", None))
        self.sptLabel.setText(_translate("SettingsDialog", "Samples per trigger:", None))
        self.groupBox.setTitle(_translate("SettingsDialog", "v-rep", None))
        self.label.setText(_translate("SettingsDialog", "Base path:", None))
        self.pushButton.setText(_translate("SettingsDialog", "...", None))
        self.label_2.setText(_translate("SettingsDialog", "Port:", None))
