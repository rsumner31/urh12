<<<<<<< HEAD
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QCompleter, QDirModel

from urh.controller.SendRecvDialogController import SendRecvDialogController
from urh.plugins.NetworkSDRInterface.NetworkSDRInterfacePlugin import NetworkSDRInterfacePlugin
from urh.signalprocessing.ProtocolSniffer import ProtocolSniffer


class ProtocolSniffDialogController(SendRecvDialogController):
    protocol_accepted = pyqtSignal(list)

    def __init__(self, project_manager, noise,
                 center, bit_length, tolerance, modulation_type_index,
                 parent=None, testing_mode=False):
        super().__init__(project_manager, is_tx=False, parent=parent, testing_mode=testing_mode)

        self.ui.stackedWidget.setCurrentIndex(2)
        self.hide_send_ui_items()
        self.hide_receive_ui_items()
        self.ui.sliderYscale.hide()
        self.ui.label_y_scale.hide()

        self.ui.spinbox_sniff_Noise.setValue(noise)
        self.ui.spinbox_sniff_Center.setValue(center)
        self.ui.spinbox_sniff_BitLen.setValue(bit_length)
        self.ui.spinbox_sniff_ErrorTolerance.setValue(tolerance)
        self.ui.combox_sniff_Modulation.setCurrentIndex(modulation_type_index)

        device = self.ui.cbDevice.currentText()
        self.sniffer = ProtocolSniffer(bit_length, center, noise, tolerance,
                                       modulation_type_index, device, testing_mode=testing_mode)

        self.set_sniff_ui_items_visible(True)
        self.set_device_ui_items_visibility(device)
=======
from PyQt5.QtCore import Qt, pyqtSlot, QRegExp, pyqtSignal
from PyQt5.QtGui import QRegExpValidator, QCloseEvent
from PyQt5.QtWidgets import QDialog, QCompleter, QDirModel

from urh import constants
from urh.signalprocessing.ProtocolSniffer import ProtocolSniffer
from urh.ui.ui_proto_sniff import Ui_SniffProtocol


class ProtocolSniffDialogController(QDialog):
    protocol_accepted = pyqtSignal(list)

    def __init__(self, freq, samp_rate, bw, gain, device, noise,
                 center, bit_length, tolerance, modulation_type_index,
                 parent=None):
        super().__init__(parent)
        self.ui = Ui_SniffProtocol()
        self.ui.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.ui.spinBoxFreq.setValue(freq)
        self.ui.spinBoxSampleRate.setValue(samp_rate)
        self.ui.spinBoxBandwidth.setValue(bw)
        self.ui.spinBoxGain.setValue(gain)
        self.ui.spinboxNoise.setValue(noise)
        self.ui.spinboxCenter.setValue(center)
        self.ui.spinboxBitLen.setValue(bit_length)
        self.ui.spinboxErrorTolerance.setValue(tolerance)
        self.ui.comboxModulation.setCurrentIndex(modulation_type_index)

        self.sniffer = ProtocolSniffer(bit_length, center, noise, tolerance,
                                       modulation_type_index, samp_rate, freq,
                                       gain, bw, device)

        self.sniffer.usrp_ip = self.ui.lineEditIP.text()

        self.ui.btnStop.setEnabled(False)
        self.ui.btnClear.setEnabled(False)

        self.ui.cbDevice.clear()
        items = []
        if constants.SETTINGS.value('usrp_available', type=bool):
            items.append("USRP")
        if constants.SETTINGS.value('hackrf_available', type=bool):
            items.append("HackRF")
        self.ui.cbDevice.addItems(items)
        if device in items:
            self.ui.cbDevice.setCurrentIndex(items.index(device))

        self.on_device_edited()

        ipRange = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"
        ipRegex = QRegExp("^" + ipRange
                          + "\\." + ipRange
                          + "\\." + ipRange
                          + "\\." + ipRange + "$")
        self.ui.lineEditIP.setValidator(QRegExpValidator(ipRegex))
>>>>>>> b1ae517... Inital Commit

        # Auto Complete like a Boss
        completer = QCompleter()
        completer.setModel(QDirModel(completer))
<<<<<<< HEAD
        self.ui.lineEdit_sniff_OutputFile.setCompleter(completer)
=======
        self.ui.lineEditOutputFile.setCompleter(completer)
>>>>>>> b1ae517... Inital Commit

        self.create_connects()

    def create_connects(self):
<<<<<<< HEAD
        super().create_connects()
        self.ui.btnAccept.clicked.connect(self.on_btn_accept_clicked)

        self.sniffer.started.connect(self.on_sniffer_rcv_started)
        self.sniffer.stopped.connect(self.on_sniffer_rcv_stopped)
        self.sniffer.qt_signals.data_sniffed.connect(self.on_data_sniffed)
        self.sniffer.qt_signals.sniff_device_errors_changed.connect(self.on_device_errors_changed)

        self.ui.spinbox_sniff_Noise.editingFinished.connect(self.on_noise_edited)
        self.ui.spinbox_sniff_Center.editingFinished.connect(self.on_center_edited)
        self.ui.spinbox_sniff_BitLen.editingFinished.connect(self.on_bit_len_edited)
        self.ui.spinbox_sniff_ErrorTolerance.editingFinished.connect(self.on_tolerance_edited)
        self.ui.combox_sniff_Modulation.currentIndexChanged.connect(self.on_modulation_changed)
        self.ui.comboBox_sniff_viewtype.currentIndexChanged.connect(self.on_view_type_changed)
        self.ui.lineEdit_sniff_OutputFile.textChanged.connect(self.on_line_edit_output_file_text_changed)

    def set_device_ui_items_visibility(self, device_name: str):
        super().set_device_ui_items_visibility(device_name)
        visible = device_name != NetworkSDRInterfacePlugin.NETWORK_SDR_NAME
        for item in ("spinbox_sniff_Noise", "combox_sniff_Modulation", "label_sniff_Modulation",
                     "spinbox_sniff_Center", "spinbox_sniff_BitLen", "spinbox_sniff_ErrorTolerance",
                     "label_sniff_Noise", "label_sniff_Center", "label_sniff_BitLength", "label_sniff_Tolerance"):
            getattr(self.ui, item).setVisible(visible)

    def closeEvent(self, event: QCloseEvent):
        if hasattr(self, "sniffer"):
            self.sniffer.stop()
        event.accept()

    @property
    def device(self):
        if hasattr(self, "sniffer"):
            return self.sniffer.rcv_device
        else:
            return None

    @device.setter
    def device(self, value):
        if hasattr(self, "sniffer"):
            self.sniffer.rcv_device = value
        else:
            pass

    @property
    def view_type(self):
        return self.ui.comboBox_sniff_viewtype.currentIndex()

    @pyqtSlot()
    def on_noise_edited(self):
        self.sniffer.signal._noise_threshold = self.ui.spinbox_sniff_Noise.value()

    @pyqtSlot()
    def on_center_edited(self):
        self.sniffer.signal.qad_center = self.ui.spinbox_sniff_Center.value()

    @pyqtSlot()
    def on_bit_len_edited(self):
        self.sniffer.signal.bit_len = self.ui.spinbox_sniff_BitLen.value()

    @pyqtSlot()
    def on_tolerance_edited(self):
        self.sniffer.signal.tolerance = self.ui.spinbox_sniff_ErrorTolerance.value()
=======
        self.ui.btnStart.clicked.connect(self.on_start_clicked)
        self.ui.btnStop.clicked.connect(self.on_stop_clicked)
        self.ui.btnClear.clicked.connect(self.on_clear_clicked)
        self.ui.btnAccept.clicked.connect(self.on_btn_accept_clicked)
        self.ui.btnClose.clicked.connect(self.close)

        self.sniffer.rcv_thrd.started.connect(self.on_sniffer_rcv_started)
        self.sniffer.rcv_thrd.stopped.connect(self.on_sniffer_rcv_stopped)
        self.sniffer.qt_signals.data_sniffed.connect(self.on_data_sniffed)
        self.sniffer.qt_signals.sniff_device_errors_changed.connect(
            self.on_device_errors_changed)

        self.ui.spinBoxSampleRate.editingFinished.connect(
            self.on_sample_rate_edited)
        self.ui.spinBoxGain.editingFinished.connect(self.on_gain_edited)
        self.ui.spinBoxFreq.editingFinished.connect(self.on_freq_edited)
        self.ui.spinBoxBandwidth.editingFinished.connect(self.on_bw_edited)
        self.ui.lineEditIP.editingFinished.connect(self.on_usrp_ip_edited)
        self.ui.cbDevice.currentIndexChanged.connect(self.on_device_edited)

        self.ui.spinboxNoise.editingFinished.connect(self.on_noise_edited)
        self.ui.spinboxCenter.editingFinished.connect(self.on_center_edited)
        self.ui.spinboxBitLen.editingFinished.connect(self.on_bit_len_edited)
        self.ui.spinboxErrorTolerance.editingFinished.connect(
            self.on_tolerance_edited)
        self.ui.comboxModulation.currentIndexChanged.connect(
            self.on_modulation_changed)
        self.ui.comboBoxViewType.currentIndexChanged.connect(
            self.on_view_type_changed)
    @property
    def view_type(self):
        return self.ui.comboBoxViewType.currentIndex()

    @property
    def has_empty_device_list(self):
        return self.ui.cbDevice.count() == 0

    @pyqtSlot()
    def on_sample_rate_edited(self):
        self.sniffer.rcv_thrd.sample_rate = self.ui.spinBoxSampleRate.value()

    @pyqtSlot()
    def on_freq_edited(self):
        self.sniffer.rcv_thrd.freq = self.ui.spinBoxFreq.value()

    @pyqtSlot()
    def on_bw_edited(self):
        self.sniffer.rcv_thrd.bandwidth = self.ui.spinBoxBandwidth.value()

    @pyqtSlot()
    def on_usrp_ip_edited(self):
        self.sniffer.usrp_ip = self.ui.lineEditIP.text()

    @pyqtSlot()
    def on_gain_edited(self):
        self.sniffer.rcv_thrd.gain = self.ui.spinBoxGain.value()

    @pyqtSlot()
    def on_noise_edited(self):
        self.sniffer.signal._noise_treshold = self.ui.spinboxNoise.value()

    @pyqtSlot()
    def on_center_edited(self):
        self.sniffer.signal.qad_center = self.ui.spinboxCenter.value()

    @pyqtSlot()
    def on_bit_len_edited(self):
        self.sniffer.signal.bit_len = self.ui.spinboxBitLen.value()

    @pyqtSlot()
    def on_tolerance_edited(self):
        self.sniffer.signal.tolerance = self.ui.spinboxErrorTolerance.value()
>>>>>>> b1ae517... Inital Commit

    @pyqtSlot(int)
    def on_modulation_changed(self, new_index: int):
        self.sniffer.signal.silent_set_modulation_type(new_index)

    @pyqtSlot()
<<<<<<< HEAD
    def on_selected_device_changed(self):
        dev_name = self.ui.cbDevice.currentText()
        self.sniffer.device_name = dev_name
        self.set_device_ui_items_visibility(dev_name)
=======
    def on_device_edited(self):
        dev = self.ui.cbDevice.currentText()
        self.sniffer.device = dev
        self.ui.lineEditIP.setVisible(dev == "USRP")
        self.ui.labelIP.setVisible(dev == "USRP")
>>>>>>> b1ae517... Inital Commit

    @pyqtSlot()
    def on_start_clicked(self):
        self.ui.spinBoxFreq.editingFinished.emit()
        self.ui.lineEditIP.editingFinished.emit()
        self.ui.spinBoxBandwidth.editingFinished.emit()
        self.ui.spinBoxSampleRate.editingFinished.emit()
<<<<<<< HEAD
        self.ui.spinbox_sniff_Noise.editingFinished.emit()
        self.ui.spinbox_sniff_Center.editingFinished.emit()
        self.ui.spinbox_sniff_BitLen.editingFinished.emit()
        self.ui.spinbox_sniff_ErrorTolerance.editingFinished.emit()
=======
        self.ui.spinboxNoise.editingFinished.emit()
        self.ui.spinboxCenter.editingFinished.emit()
        self.ui.spinboxBitLen.editingFinished.emit()
        self.ui.spinboxErrorTolerance.editingFinished.emit()
>>>>>>> b1ae517... Inital Commit

        self.sniffer.sniff()

    @pyqtSlot()
    def on_stop_clicked(self):
        self.sniffer.stop()

    @pyqtSlot()
    def on_sniffer_rcv_stopped(self):
        self.ui.btnStart.setEnabled(True)
        self.ui.btnStop.setEnabled(False)
        self.ui.btnClear.setEnabled(True)

        self.ui.spinBoxSampleRate.setEnabled(True)
        self.ui.spinBoxFreq.setEnabled(True)
        self.ui.lineEditIP.setEnabled(True)
        self.ui.spinBoxBandwidth.setEnabled(True)
        self.ui.spinBoxGain.setEnabled(True)
        self.ui.cbDevice.setEnabled(True)

<<<<<<< HEAD
        self.ui.spinbox_sniff_Noise.setEnabled(True)
        self.ui.spinbox_sniff_Center.setEnabled(True)
        self.ui.spinbox_sniff_BitLen.setEnabled(True)
        self.ui.spinbox_sniff_ErrorTolerance.setEnabled(True)
        self.ui.combox_sniff_Modulation.setEnabled(True)
=======
        self.ui.spinboxNoise.setEnabled(True)
        self.ui.spinboxCenter.setEnabled(True)
        self.ui.spinboxBitLen.setEnabled(True)
        self.ui.spinboxErrorTolerance.setEnabled(True)
        self.ui.comboxModulation.setEnabled(True)
>>>>>>> b1ae517... Inital Commit

    @pyqtSlot()
    def on_sniffer_rcv_started(self):
        self.ui.txtEditErrors.clear()
        self.ui.btnStart.setEnabled(False)
        self.ui.btnClear.setEnabled(False)
        self.ui.btnStop.setEnabled(True)

        self.ui.spinBoxSampleRate.setDisabled(True)
        self.ui.spinBoxFreq.setDisabled(True)
        self.ui.spinBoxGain.setDisabled(True)
        self.ui.spinBoxBandwidth.setDisabled(True)

<<<<<<< HEAD
        self.ui.spinbox_sniff_Noise.setDisabled(True)
        self.ui.spinbox_sniff_Center.setDisabled(True)
        self.ui.spinbox_sniff_BitLen.setDisabled(True)
        self.ui.spinbox_sniff_ErrorTolerance.setDisabled(True)
        self.ui.combox_sniff_Modulation.setDisabled(True)
=======
        self.ui.spinboxNoise.setDisabled(True)
        self.ui.spinboxCenter.setDisabled(True)
        self.ui.spinboxBitLen.setDisabled(True)
        self.ui.spinboxErrorTolerance.setDisabled(True)
        self.ui.comboxModulation.setDisabled(True)
>>>>>>> b1ae517... Inital Commit

        self.ui.lineEditIP.setDisabled(True)
        self.ui.cbDevice.setDisabled(True)

    @pyqtSlot()
    def on_clear_clicked(self):
        self.ui.btnClear.setEnabled(False)
<<<<<<< HEAD
        self.ui.txtEd_sniff_Preview.clear()
=======
        self.ui.txtEdPreview.clear()
>>>>>>> b1ae517... Inital Commit
        self.sniffer.clear()

    @pyqtSlot(int)
    def on_data_sniffed(self, from_index: int):
<<<<<<< HEAD
        new_data = self.sniffer.plain_to_string(self.view_type, start=from_index, show_pauses=False)
        if new_data.strip():
            self.ui.txtEd_sniff_Preview.appendPlainText(new_data)
            self.ui.txtEd_sniff_Preview.verticalScrollBar().setValue(self.ui.txtEd_sniff_Preview.verticalScrollBar().maximum())

    @pyqtSlot(int)
    def on_view_type_changed(self, new_index: int):
        self.ui.txtEd_sniff_Preview.setPlainText(self.sniffer.plain_to_string(new_index, show_pauses=False))

    @pyqtSlot()
    def on_btn_accept_clicked(self):
        self.protocol_accepted.emit(self.sniffer.messages)
=======
        self.ui.txtEdPreview.appendPlainText(self.sniffer.plain_to_string(
            self.view_type, start=from_index))
        self.ui.txtEdPreview.verticalScrollBar().setValue(
            self.ui.txtEdPreview.verticalScrollBar().maximum())

    @pyqtSlot(int)
    def on_view_type_changed(self, new_index: int):
        self.ui.txtEdPreview.setPlainText(
            self.sniffer.plain_to_string(new_index))

    @pyqtSlot()
    def on_btn_accept_clicked(self):
        self.protocol_accepted.emit(self.sniffer.blocks)
>>>>>>> b1ae517... Inital Commit
        self.close()

    @pyqtSlot(str)
    def on_device_errors_changed(self, txt: str):
        self.ui.txtEditErrors.append(txt)

<<<<<<< HEAD
    @pyqtSlot(str)
    def on_line_edit_output_file_text_changed(self, text: str):
=======
    def closeEvent(self, event: QCloseEvent):
        self.sniffer.stop()
        event.accept()

    @pyqtSlot(str)
    def on_lineEditOutputFile_textChanged(self, text: str):
>>>>>>> b1ae517... Inital Commit
        self.sniffer.sniff_file = text
        self.ui.btnAccept.setDisabled(bool(self.sniffer.sniff_file))
