# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../ui/generator.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_GeneratorTab(object):
    def setupUi(self, GeneratorTab):
        GeneratorTab.setObjectName("GeneratorTab")
        GeneratorTab.resize(1083, 995)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(GeneratorTab)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.splitter = QtWidgets.QSplitter(GeneratorTab)
        self.splitter.setStyleSheet("QSplitter::handle {\n"
"    background-color: #AAAAAA;\n"
"}")
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setHandleWidth(2)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_proto = QtWidgets.QWidget()
        self.tab_proto.setObjectName("tab_proto")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.tab_proto)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.treeProtocols = GeneratorTreeView(self.tab_proto)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeProtocols.sizePolicy().hasHeightForWidth())
        self.treeProtocols.setSizePolicy(sizePolicy)
        self.treeProtocols.setObjectName("treeProtocols")
        self.treeProtocols.header().setDefaultSectionSize(0)
        self.horizontalLayout.addWidget(self.treeProtocols)
        self.tabWidget.addTab(self.tab_proto, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_4)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.lWPauses = GeneratorListWidget(self.tab_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lWPauses.sizePolicy().hasHeightForWidth())
        self.lWPauses.setSizePolicy(sizePolicy)
        self.lWPauses.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked|QtWidgets.QAbstractItemView.EditKeyPressed)
        self.lWPauses.setProperty("showDropIndicator", False)
        self.lWPauses.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.lWPauses.setObjectName("lWPauses")
        self.gridLayout_4.addWidget(self.lWPauses, 0, 0, 1, 2)
        self.tabWidget.addTab(self.tab_4, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.tab_5)
        self.verticalLayout_8.setSpacing(6)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.listViewProtoLabels = GeneratorListView(self.tab_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listViewProtoLabels.sizePolicy().hasHeightForWidth())
        self.listViewProtoLabels.setSizePolicy(sizePolicy)
        self.listViewProtoLabels.setEditTriggers(QtWidgets.QAbstractItemView.EditKeyPressed)
        self.listViewProtoLabels.setObjectName("listViewProtoLabels")
        self.verticalLayout_8.addWidget(self.listViewProtoLabels)
        self.groupBox = QtWidgets.QGroupBox(self.tab_5)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.btnFuzz = QtWidgets.QPushButton(self.groupBox)
        self.btnFuzz.setObjectName("btnFuzz")
        self.horizontalLayout_5.addWidget(self.btnFuzz)
        self.rBSuccessive = QtWidgets.QRadioButton(self.groupBox)
        self.rBSuccessive.setObjectName("rBSuccessive")
        self.horizontalLayout_5.addWidget(self.rBSuccessive)
        self.rbConcurrent = QtWidgets.QRadioButton(self.groupBox)
        self.rbConcurrent.setObjectName("rbConcurrent")
        self.horizontalLayout_5.addWidget(self.rbConcurrent)
        self.rBExhaustive = QtWidgets.QRadioButton(self.groupBox)
        self.rBExhaustive.setObjectName("rBExhaustive")
        self.horizontalLayout_5.addWidget(self.rBExhaustive)
        self.verticalLayout_8.addWidget(self.groupBox)
        self.tabWidget.addTab(self.tab_5, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.cBoxModulations = QtWidgets.QComboBox(self.layoutWidget)
        self.cBoxModulations.setObjectName("cBoxModulations")
        self.cBoxModulations.addItem("")
        self.gridLayout_3.addWidget(self.cBoxModulations, 2, 1, 1, 1)
        self.modulationLayout = QtWidgets.QGridLayout()
        self.modulationLayout.setObjectName("modulationLayout")
        self.lEncoding = QtWidgets.QLabel(self.layoutWidget)
        self.lEncoding.setObjectName("lEncoding")
        self.modulationLayout.addWidget(self.lEncoding, 0, 0, 1, 1)
        self.lEncodingValue = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lEncodingValue.sizePolicy().hasHeightForWidth())
        self.lEncodingValue.setSizePolicy(sizePolicy)
        self.lEncodingValue.setMinimumSize(QtCore.QSize(0, 0))
        self.lEncodingValue.setObjectName("lEncodingValue")
        self.modulationLayout.addWidget(self.lEncodingValue, 0, 1, 1, 1)
        self.lSampleRate = QtWidgets.QLabel(self.layoutWidget)
        self.lSampleRate.setObjectName("lSampleRate")
        self.modulationLayout.addWidget(self.lSampleRate, 0, 2, 1, 1)
        self.lSampleRateValue = QtWidgets.QLabel(self.layoutWidget)
        self.lSampleRateValue.setObjectName("lSampleRateValue")
        self.modulationLayout.addWidget(self.lSampleRateValue, 0, 3, 1, 1)
        self.lCarrierFrequency = QtWidgets.QLabel(self.layoutWidget)
        self.lCarrierFrequency.setObjectName("lCarrierFrequency")
        self.modulationLayout.addWidget(self.lCarrierFrequency, 1, 0, 1, 1)
        self.lCarrierFreqValue = QtWidgets.QLabel(self.layoutWidget)
        self.lCarrierFreqValue.setObjectName("lCarrierFreqValue")
        self.modulationLayout.addWidget(self.lCarrierFreqValue, 1, 1, 1, 1)
        self.lModType = QtWidgets.QLabel(self.layoutWidget)
        self.lModType.setObjectName("lModType")
        self.modulationLayout.addWidget(self.lModType, 1, 2, 1, 1)
        self.lModTypeValue = QtWidgets.QLabel(self.layoutWidget)
        self.lModTypeValue.setObjectName("lModTypeValue")
        self.modulationLayout.addWidget(self.lModTypeValue, 1, 3, 1, 1)
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.modulationLayout.addWidget(self.label, 2, 0, 1, 1)
        self.lCarrierPhaseValue = QtWidgets.QLabel(self.layoutWidget)
        self.lCarrierPhaseValue.setObjectName("lCarrierPhaseValue")
        self.modulationLayout.addWidget(self.lCarrierPhaseValue, 2, 1, 1, 1)
        self.lParamForZero = QtWidgets.QLabel(self.layoutWidget)
        self.lParamForZero.setObjectName("lParamForZero")
        self.modulationLayout.addWidget(self.lParamForZero, 2, 2, 1, 1)
        self.lParamForZeroValue = QtWidgets.QLabel(self.layoutWidget)
        self.lParamForZeroValue.setObjectName("lParamForZeroValue")
        self.modulationLayout.addWidget(self.lParamForZeroValue, 2, 3, 1, 1)
        self.lBitLength = QtWidgets.QLabel(self.layoutWidget)
        self.lBitLength.setObjectName("lBitLength")
        self.modulationLayout.addWidget(self.lBitLength, 3, 0, 1, 1)
        self.lBitLenValue = QtWidgets.QLabel(self.layoutWidget)
        self.lBitLenValue.setObjectName("lBitLenValue")
        self.modulationLayout.addWidget(self.lBitLenValue, 3, 1, 1, 1)
        self.lParamForOne = QtWidgets.QLabel(self.layoutWidget)
        self.lParamForOne.setObjectName("lParamForOne")
        self.modulationLayout.addWidget(self.lParamForOne, 3, 2, 1, 1)
        self.lParamForOneValue = QtWidgets.QLabel(self.layoutWidget)
        self.lParamForOneValue.setObjectName("lParamForOneValue")
        self.modulationLayout.addWidget(self.lParamForOneValue, 3, 3, 1, 1)
        self.gridLayout_3.addLayout(self.modulationLayout, 0, 0, 1, 3)
        self.lModulation = QtWidgets.QLabel(self.layoutWidget)
        self.lModulation.setObjectName("lModulation")
        self.gridLayout_3.addWidget(self.lModulation, 2, 0, 1, 1)
        self.btnSend = QtWidgets.QPushButton(self.layoutWidget)
        self.btnSend.setEnabled(False)
        self.btnSend.setObjectName("btnSend")
        self.gridLayout_3.addWidget(self.btnSend, 5, 2, 1, 1)
        self.line = QtWidgets.QFrame(self.layoutWidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_3.addWidget(self.line, 1, 0, 1, 3)
        self.btnEditModulation = QtWidgets.QPushButton(self.layoutWidget)
        self.btnEditModulation.setObjectName("btnEditModulation")
        self.gridLayout_3.addWidget(self.btnEditModulation, 2, 2, 1, 1)
        self.prBarGeneration = QtWidgets.QProgressBar(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.prBarGeneration.sizePolicy().hasHeightForWidth())
        self.prBarGeneration.setSizePolicy(sizePolicy)
        self.prBarGeneration.setProperty("value", 0)
        self.prBarGeneration.setObjectName("prBarGeneration")
        self.gridLayout_3.addWidget(self.prBarGeneration, 5, 0, 1, 1)
        self.btnGenerate = QtWidgets.QPushButton(self.layoutWidget)
        self.btnGenerate.setEnabled(False)
        self.btnGenerate.setObjectName("btnGenerate")
        self.gridLayout_3.addWidget(self.btnGenerate, 5, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_3)
        self.layoutWidget1 = QtWidgets.QWidget(self.splitter)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tableBlocks = GeneratorTableView(self.layoutWidget1)
        self.tableBlocks.setAcceptDrops(True)
        self.tableBlocks.setDragEnabled(False)
        self.tableBlocks.setDragDropOverwriteMode(False)
        self.tableBlocks.setDragDropMode(QtWidgets.QAbstractItemView.DropOnly)
        self.tableBlocks.setDefaultDropAction(QtCore.Qt.CopyAction)
        self.tableBlocks.setAlternatingRowColors(True)
        self.tableBlocks.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.tableBlocks.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tableBlocks.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tableBlocks.setShowGrid(False)
        self.tableBlocks.setObjectName("tableBlocks")
        self.tableBlocks.horizontalHeader().setHighlightSections(False)
        self.tableBlocks.verticalHeader().setHighlightSections(False)
        self.gridLayout_2.addWidget(self.tableBlocks, 1, 0, 1, 4)
        self.lEstimatedTime = QtWidgets.QLabel(self.layoutWidget1)
        self.lEstimatedTime.setObjectName("lEstimatedTime")
        self.gridLayout_2.addWidget(self.lEstimatedTime, 2, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(38, 22, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 2, 1, 1, 1)
        self.lViewType = QtWidgets.QLabel(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lViewType.sizePolicy().hasHeightForWidth())
        self.lViewType.setSizePolicy(sizePolicy)
        self.lViewType.setObjectName("lViewType")
        self.gridLayout_2.addWidget(self.lViewType, 2, 2, 1, 1)
        self.cbViewType = QtWidgets.QComboBox(self.layoutWidget1)
        self.cbViewType.setObjectName("cbViewType")
        self.cbViewType.addItem("")
        self.cbViewType.addItem("")
        self.cbViewType.addItem("")
        self.gridLayout_2.addWidget(self.cbViewType, 2, 3, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 0, 1, 4)
        self.horizontalLayout_2.addWidget(self.splitter)

        self.retranslateUi(GeneratorTab)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(GeneratorTab)

    def retranslateUi(self, GeneratorTab):
        _translate = QtCore.QCoreApplication.translate
        GeneratorTab.setWindowTitle(_translate("GeneratorTab", "Form"))
        self.treeProtocols.setToolTip(_translate("GeneratorTab", "<html><head/><body><p>Drag&amp;Drop Protocols to the table on the right to fill the generation table.</p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_proto), _translate("GeneratorTab", "Protocols"))
        self.lWPauses.setToolTip(_translate("GeneratorTab", "<html><head/><body><p>The pause blocks will be added automatically when you drag a protocol from the tree above to the table on the right.<br/></p><p>You can see the <span style=\" font-weight:600;\">position</span> of each pause by <span style=\" font-weight:600;\">selecting it</span>. There will be drawn a line in the table indiciating the position of the pause.<br/></p><p>Use context menu or double click to <span style=\" font-weight:600;\">edit a pauses\' length</span>.</p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("GeneratorTab", "Pauses"))
        self.groupBox.setTitle(_translate("GeneratorTab", "Add fuzzing values to generated data"))
        self.btnFuzz.setText(_translate("GeneratorTab", "Fuzz"))
        self.rBSuccessive.setToolTip(_translate("GeneratorTab", "<html><head/><body><p>For multiple labels per block the fuzzed values are inserted <span style=\" font-weight:600;\">one-by-one</span>.</p></body></html>"))
        self.rBSuccessive.setText(_translate("GeneratorTab", "S&uccessive"))
        self.rbConcurrent.setToolTip(_translate("GeneratorTab", "<html><head/><body><p>For multiple labels per block the labels are fuzzed <span style=\" font-weight:600;\">at the same time</span>.</p></body></html>"))
        self.rbConcurrent.setText(_translate("GeneratorTab", "&Concurrent"))
        self.rBExhaustive.setToolTip(_translate("GeneratorTab", "<html><head/><body><p>For multiple labels per block the fuzzed values are inserted in <span style=\" font-weight:600;\">all possible combinations</span>.</p></body></html>"))
        self.rBExhaustive.setText(_translate("GeneratorTab", "E&xhaustive"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("GeneratorTab", "Fuzzing"))
        self.cBoxModulations.setItemText(0, _translate("GeneratorTab", "MyModulation"))
        self.lEncoding.setText(_translate("GeneratorTab", "Encoding:"))
        self.lEncodingValue.setText(_translate("GeneratorTab", "-"))
        self.lSampleRate.setText(_translate("GeneratorTab", "Sample Rate:"))
        self.lSampleRateValue.setText(_translate("GeneratorTab", "TextLabel"))
        self.lCarrierFrequency.setText(_translate("GeneratorTab", "Carrier Frequency:"))
        self.lCarrierFreqValue.setText(_translate("GeneratorTab", "TextLabel"))
        self.lModType.setText(_translate("GeneratorTab", "Modulation Type:"))
        self.lModTypeValue.setText(_translate("GeneratorTab", "TextLabel"))
        self.label.setText(_translate("GeneratorTab", "Carrier Phase:"))
        self.lCarrierPhaseValue.setText(_translate("GeneratorTab", "TextLabel"))
        self.lParamForZero.setText(_translate("GeneratorTab", "Amplitude for 0:"))
        self.lParamForZeroValue.setText(_translate("GeneratorTab", "TextLabel"))
        self.lBitLength.setText(_translate("GeneratorTab", "Bit Length:"))
        self.lBitLenValue.setText(_translate("GeneratorTab", "TextLabel"))
        self.lParamForOne.setText(_translate("GeneratorTab", "Amplitude for 1:"))
        self.lParamForOneValue.setText(_translate("GeneratorTab", "TextLabel"))
        self.lModulation.setText(_translate("GeneratorTab", "Modulation:"))
        self.btnSend.setText(_translate("GeneratorTab", "Send data..."))
        self.btnEditModulation.setText(_translate("GeneratorTab", "Edit ..."))
        self.prBarGeneration.setFormat(_translate("GeneratorTab", "Modulating %p%"))
        self.btnGenerate.setToolTip(_translate("GeneratorTab", "Generate the complex file of the modulated signal, after tuning all parameters above."))
        self.btnGenerate.setText(_translate("GeneratorTab", "Generate file..."))
        self.lEstimatedTime.setToolTip(_translate("GeneratorTab", "<html><head/><body><p>The estimated average time is based on the average number of bits per block and average sample rate, you set for the modulations.</p></body></html>"))
        self.lEstimatedTime.setText(_translate("GeneratorTab", "Estimated Time: "))
        self.lViewType.setText(_translate("GeneratorTab", "Viewtype:"))
        self.cbViewType.setItemText(0, _translate("GeneratorTab", "Bit"))
        self.cbViewType.setItemText(1, _translate("GeneratorTab", "Hex"))
        self.cbViewType.setItemText(2, _translate("GeneratorTab", "ASCII"))
        self.label_3.setText(_translate("GeneratorTab", "Generated data"))

from urh.ui.GeneratorListWidget import GeneratorListWidget
from urh.ui.views.GeneratorListView import GeneratorListView
from urh.ui.views.GeneratorTableView import GeneratorTableView
from urh.ui.views.GeneratorTreeView import GeneratorTreeView
from . import urh_rc
