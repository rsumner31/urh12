<<<<<<< HEAD
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QHeaderView

from urh import constants
from urh.models.PLabelTableModel import PLabelTableModel
from urh.signalprocessing.FieldType import FieldType
from urh.signalprocessing.Message import Message
from urh.signalprocessing.MessageType import MessageType
from urh.signalprocessing.ProtocoLabel import ProtocolLabel
from urh.ui.delegates.CheckBoxDelegate import CheckBoxDelegate
from urh.ui.delegates.ComboBoxDelegate import ComboBoxDelegate
=======
import numpy
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QDialog, QApplication

from urh import constants
from urh.models.PLabelTableModel import PLabelTableModel
from urh.signalprocessing.ProtocolAnalyzer import ProtocolAnalyzer
from urh.signalprocessing.ProtocolGroup import ProtocolGroup
from urh.ui.delegates.CheckBoxDelegate import CheckBoxDelegate
from urh.ui.delegates.ComboBoxDelegate import ComboBoxDelegate
from urh.ui.delegates.DeleteButtonDelegate import DeleteButtonDelegate
>>>>>>> b1ae517... Inital Commit
from urh.ui.delegates.SpinBoxDelegate import SpinBoxDelegate
from urh.ui.ui_properties_dialog import Ui_DialogLabels


class ProtocolLabelController(QDialog):
<<<<<<< HEAD
    apply_decoding_changed = pyqtSignal(ProtocolLabel, MessageType)

    def __init__(self, preselected_index, message: Message, viewtype: int, parent=None):
        super().__init__(parent)
        self.ui = Ui_DialogLabels()
        self.ui.setupUi(self)
        field_types = FieldType.load_from_xml()
        self.model = PLabelTableModel(message, field_types)
        self.preselected_index = preselected_index

        self.ui.tblViewProtoLabels.setItemDelegateForColumn(0, ComboBoxDelegate([ft.caption for ft in field_types],
                                                                                is_editable=True,
                                                                                return_index=False, parent=self))
        self.ui.tblViewProtoLabels.setItemDelegateForColumn(1, SpinBoxDelegate(1, len(message), self))
        self.ui.tblViewProtoLabels.setItemDelegateForColumn(2, SpinBoxDelegate(1, len(message), self))
        self.ui.tblViewProtoLabels.setItemDelegateForColumn(3,
                                                            ComboBoxDelegate([""] * len(constants.LABEL_COLORS),
                                                                             colors=constants.LABEL_COLORS,
                                                                             parent=self))
        self.ui.tblViewProtoLabels.setItemDelegateForColumn(4, CheckBoxDelegate(self))
=======
    def __init__(self, preselected_index, proto_group: ProtocolGroup, offset: int, viewtype: int,
                 parent=None):
        super().__init__(parent)
        self.ui = Ui_DialogLabels()
        self.ui.setupUi(self)
        self.model = PLabelTableModel(proto_group, offset)
        self.preselected_index = preselected_index

        if proto_group.num_blocks > 0:
            maxval = numpy.max([len(block) for block in proto_group.decoded_bits_str])
        else:
            maxval = 42000

        self.ui.tblViewProtoLabels.setItemDelegateForColumn(1, SpinBoxDelegate(1, maxval, self))
        self.ui.tblViewProtoLabels.setItemDelegateForColumn(2, SpinBoxDelegate(1, maxval, self))
        self.ui.tblViewProtoLabels.setItemDelegateForColumn(3, CheckBoxDelegate(self))
        self.ui.tblViewProtoLabels.setItemDelegateForColumn(4, SpinBoxDelegate(offset+1,
                                                                               offset+proto_group.num_blocks,
                                                                               self))

        self.ui.tblViewProtoLabels.setItemDelegateForColumn(5,
                                                            ComboBoxDelegate([""] * len(constants.LABEL_COLORS), True,
                                                                             self))
        self.ui.tblViewProtoLabels.setItemDelegateForColumn(6, CheckBoxDelegate(self))
        self.ui.tblViewProtoLabels.setItemDelegateForColumn(7, DeleteButtonDelegate(self))
>>>>>>> b1ae517... Inital Commit

        self.ui.tblViewProtoLabels.setModel(self.model)
        self.ui.tblViewProtoLabels.selectRow(preselected_index)

<<<<<<< HEAD
        self.ui.tblViewProtoLabels.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for i in range(self.model.rowCount()):
            self.open_editors(i)

        self.ui.tblViewProtoLabels.resizeColumnsToContents()
        self.setWindowTitle(self.tr("Edit Protocol Labels from %s") % message.message_type.name)
=======
        for i in range(self.model.row_count):
            self.openEditors(i)

        self.ui.tblViewProtoLabels.resizeColumnsToContents()
        self.setWindowTitle(self.tr("Edit Protocol Labels from %s") % proto_group.name)
>>>>>>> b1ae517... Inital Commit

        self.create_connects()
        self.ui.cbProtoView.setCurrentIndex(viewtype)
        self.setAttribute(Qt.WA_DeleteOnClose)

    def create_connects(self):
        self.ui.btnConfirm.clicked.connect(self.confirm)
        self.ui.cbProtoView.currentIndexChanged.connect(self.set_view_index)
<<<<<<< HEAD
        self.model.apply_decoding_changed.connect(self.on_apply_decoding_changed)

    def open_editors(self, row):
=======
        self.model.restrictive_changed.connect(self.handle_restrictive_changed)

    @pyqtSlot()
    def confirm(self):
        self.close()

    def openEditors(self, row):
>>>>>>> b1ae517... Inital Commit
        self.ui.tblViewProtoLabels.openPersistentEditor(self.model.index(row, 1))
        self.ui.tblViewProtoLabels.openPersistentEditor(self.model.index(row, 2))
        self.ui.tblViewProtoLabels.openPersistentEditor(self.model.index(row, 3))

<<<<<<< HEAD
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Enter:
            event.ignore()
        else:
            event.accept()

    @pyqtSlot()
    def confirm(self):
        self.close()
=======
        if self.model.protocol_labels[row].restrictive:
            self.ui.tblViewProtoLabels.openPersistentEditor(self.model.index(row, 4))

        self.ui.tblViewProtoLabels.openPersistentEditor(self.model.index(row, 5))
        self.ui.tblViewProtoLabels.openPersistentEditor(self.model.index(row, 6))
        self.ui.tblViewProtoLabels.openPersistentEditor(self.model.index(row, 7))

    @pyqtSlot(int, bool)
    def handle_restrictive_changed(self, row: int, restrictive: bool):
        if restrictive:
            self.ui.tblViewProtoLabels.openPersistentEditor(self.model.index(row, 4))
        else:
            self.ui.tblViewProtoLabels.closePersistentEditor(self.model.index(row, 4))
>>>>>>> b1ae517... Inital Commit

    @pyqtSlot(int)
    def set_view_index(self, ind):
        self.model.proto_view = ind
<<<<<<< HEAD
        self.model.update()

    @pyqtSlot(ProtocolLabel)
    def on_apply_decoding_changed(self, lbl: ProtocolLabel):
        self.apply_decoding_changed.emit(lbl, self.model.message_type)
=======
        self.model.update()
>>>>>>> b1ae517... Inital Commit
