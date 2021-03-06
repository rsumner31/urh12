# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../ui/options.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogOptions(object):
    def setupUi(self, DialogOptions):
        DialogOptions.setObjectName("DialogOptions")
        DialogOptions.resize(666, 486)
        self.horizontalLayout = QtWidgets.QHBoxLayout(DialogOptions)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget = QtWidgets.QTabWidget(DialogOptions)
        self.tabWidget.setObjectName("tabWidget")
        self.tabInterpretation = QtWidgets.QWidget()
        self.tabInterpretation.setObjectName("tabInterpretation")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tabInterpretation)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.tabInterpretation)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.spinBoxSymbolTreshold = QtWidgets.QSpinBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxSymbolTreshold.sizePolicy().hasHeightForWidth())
        self.spinBoxSymbolTreshold.setSizePolicy(sizePolicy)
        self.spinBoxSymbolTreshold.setMaximum(50)
        self.spinBoxSymbolTreshold.setObjectName("spinBoxSymbolTreshold")
        self.gridLayout.addWidget(self.spinBoxSymbolTreshold, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.lSymbolLength = QtWidgets.QLabel(self.groupBox)
        self.lSymbolLength.setObjectName("lSymbolLength")
        self.gridLayout.addWidget(self.lSymbolLength, 1, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 1, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.lExplanation = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lExplanation.setFont(font)
        self.lExplanation.setWordWrap(True)
        self.lExplanation.setObjectName("lExplanation")
        self.verticalLayout.addWidget(self.lExplanation)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.tabWidget.addTab(self.tabInterpretation, "")
        self.tabView = QtWidgets.QWidget()
        self.tabView.setObjectName("tabView")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tabView)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_7 = QtWidgets.QLabel(self.tabView)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_2.addWidget(self.label_7)
        self.comboBoxDefaultView = QtWidgets.QComboBox(self.tabView)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxDefaultView.sizePolicy().hasHeightForWidth())
        self.comboBoxDefaultView.setSizePolicy(sizePolicy)
        self.comboBoxDefaultView.setObjectName("comboBoxDefaultView")
        self.comboBoxDefaultView.addItem("")
        self.comboBoxDefaultView.addItem("")
        self.comboBoxDefaultView.addItem("")
        self.horizontalLayout_2.addWidget(self.comboBoxDefaultView)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.checkBoxPauseTime = QtWidgets.QCheckBox(self.tabView)
        self.checkBoxPauseTime.setObjectName("checkBoxPauseTime")
        self.verticalLayout_4.addWidget(self.checkBoxPauseTime)
        spacerItem2 = QtWidgets.QSpacerItem(20, 383, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem2)
        self.tabWidget.addTab(self.tabView, "")
        self.tab_plugins = QtWidgets.QWidget()
        self.tab_plugins.setObjectName("tab_plugins")
        self.tabWidget.addTab(self.tab_plugins, "")
        self.tabDevices = QtWidgets.QWidget()
        self.tabDevices.setObjectName("tabDevices")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tabDevices)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.groupBox_2 = QtWidgets.QGroupBox(self.tabDevices)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        font = QtGui.QFont()
        font.setItalic(True)
        self.label_5.setFont(font)
        self.label_5.setWordWrap(True)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_3.addWidget(self.label_5)
        self.chkBoxUSRP = QtWidgets.QCheckBox(self.groupBox_2)
        self.chkBoxUSRP.setChecked(True)
        self.chkBoxUSRP.setObjectName("chkBoxUSRP")
        self.verticalLayout_3.addWidget(self.chkBoxUSRP)
        self.chkBoxHackRF = QtWidgets.QCheckBox(self.groupBox_2)
        self.chkBoxHackRF.setChecked(True)
        self.chkBoxHackRF.setObjectName("chkBoxHackRF")
        self.verticalLayout_3.addWidget(self.chkBoxHackRF)
        self.verticalLayout_5.addWidget(self.groupBox_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_8 = QtWidgets.QLabel(self.tabDevices)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_3.addWidget(self.label_8)
        self.spinBoxNumSendingRepeats = QtWidgets.QSpinBox(self.tabDevices)
        self.spinBoxNumSendingRepeats.setProperty("showGroupSeparator", False)
        self.spinBoxNumSendingRepeats.setMaximum(999999999)
        self.spinBoxNumSendingRepeats.setDisplayIntegerBase(10)
        self.spinBoxNumSendingRepeats.setObjectName("spinBoxNumSendingRepeats")
        self.horizontalLayout_3.addWidget(self.spinBoxNumSendingRepeats)
        self.verticalLayout_5.addLayout(self.horizontalLayout_3)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem3)
        self.tabWidget.addTab(self.tabDevices, "")
        self.horizontalLayout.addWidget(self.tabWidget)

        self.retranslateUi(DialogOptions)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(DialogOptions)

    def retranslateUi(self, DialogOptions):
        _translate = QtCore.QCoreApplication.translate
        DialogOptions.setWindowTitle(_translate("DialogOptions", "Options"))
        self.groupBox.setTitle(_translate("DialogOptions", "Symbols"))
        self.label.setText(_translate("DialogOptions", "Some protocols use different information lengths. This can be part of the protocol logic (e.g. to indicate a SOF). You can set a tolerance window for the selected bit length, outside the window a new symbol will be created."))
        self.label_2.setText(_translate("DialogOptions", "Tolerance window:"))
        self.spinBoxSymbolTreshold.setSuffix(_translate("DialogOptions", "%"))
        self.label_3.setText(_translate("DialogOptions", "of selected bit length"))
        self.label_4.setText(_translate("DialogOptions", "Relative symbol length:"))
        self.lSymbolLength.setText(_translate("DialogOptions", "0%"))
        self.label_6.setText(_translate("DialogOptions", "of selected bit length"))
        self.lExplanation.setText(_translate("DialogOptions", "No Symbols will be created"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabInterpretation), _translate("DialogOptions", "Interpretation"))
        self.label_7.setText(_translate("DialogOptions", "Default View:"))
        self.comboBoxDefaultView.setItemText(0, _translate("DialogOptions", "Bit"))
        self.comboBoxDefaultView.setItemText(1, _translate("DialogOptions", "Hex"))
        self.comboBoxDefaultView.setItemText(2, _translate("DialogOptions", "ASCII"))
        self.checkBoxPauseTime.setText(_translate("DialogOptions", "Show pauses as time"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabView), _translate("DialogOptions", "View"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_plugins), _translate("DialogOptions", "Plugins"))
        self.groupBox_2.setTitle(_translate("DialogOptions", "Available Devices"))
        self.label_5.setText(_translate("DialogOptions", "Choose the selectable Devices in send/receive dialogs"))
        self.chkBoxUSRP.setText(_translate("DialogOptions", "USRP"))
        self.chkBoxHackRF.setText(_translate("DialogOptions", "HackRF"))
        self.label_8.setText(_translate("DialogOptions", "Default sending repititions:"))
        self.spinBoxNumSendingRepeats.setSpecialValueText(_translate("DialogOptions", "Infinite"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabDevices), _translate("DialogOptions", "Device"))

