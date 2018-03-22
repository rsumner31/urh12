import locale
<<<<<<< HEAD
import time

from PyQt5.QtCore import pyqtSlot, QTimer, QRegExp, pyqtSignal
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtGui import QRegExpValidator, QIcon
from PyQt5.QtGui import QTransform
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QSlider
from PyQt5.QtWidgets import QSpinBox

from urh import constants
from urh.dev import config
from urh.dev.BackendHandler import BackendHandler, Backends
from urh.dev.VirtualDevice import VirtualDevice
from urh.plugins.NetworkSDRInterface.NetworkSDRInterfacePlugin import NetworkSDRInterfacePlugin
from urh.plugins.PluginManager import PluginManager
from urh.ui.ui_send_recv import Ui_SendRecvDialog
from urh.util.Errors import Errors
from urh.util.Logger import logger
from urh.util.ProjectManager import ProjectManager


class SendRecvDialogController(QDialog):
    recording_parameters = pyqtSignal(str, dict)

    def __init__(self, project_manager: ProjectManager, is_tx: bool, parent=None, testing_mode=False):
        super().__init__(parent)
        self.is_tx = is_tx

        self.ui = Ui_SendRecvDialog()
        logger.debug("{}: Call setupUi".format(self.__class__.__name__))
        self.ui.setupUi(self)
        logger.debug("{}: Called setupUi".format(self.__class__.__name__))

        self.set_sniff_ui_items_visible(False)

        self.graphics_view = None  # type: QGraphicsView
        self.__device = None  # type: VirtualDevice

        self.backend_handler = BackendHandler(testing_mode=testing_mode)
=======
import random
import time
from enum import Enum

from PyQt5.QtCore import Qt, pyqtSlot, QTimer, QRegExp, pyqtSignal
from PyQt5.QtGui import QRegExpValidator, QIcon
from PyQt5.QtWidgets import QDialog, QMessageBox, QApplication

from urh import constants
from urh.FFTSceneManager import FFTSceneManager
from urh.LiveSceneManager import LiveSceneManager
from urh.dev.ReceiverThread import ReceiverThread
from urh.dev.SenderThread import SenderThread
from urh.dev.SpectrumThread import SpectrumThread
from urh.ui.ui_send_recv import Ui_SendRecvDialog
from urh.util import FileOperator
from urh.util.Errors import Errors


class Mode(Enum):
    receive = 1
    send = 2
    spectrum = 3


class SendRecvDialogController(QDialog):
    files_recorded = pyqtSignal(list)
    recording_parameters = pyqtSignal(str, str, str, str, str)

    def __init__(self, freq, samp_rate, bw, gain, device, mode: Mode, modulated_data=None, parent=None):
        super().__init__(parent)
        self.ui = Ui_SendRecvDialog()
        self.ui.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.update_interval = 125

        self.mode = mode  # recv, send, or spectrum
        if self.mode == Mode.send and modulated_data is None:
            raise ValueError("I need modulated data to send!")

        if self.mode == Mode.receive or self.mode == Mode.spectrum:
            self.ui.spinBoxNRepeat.hide()
            self.ui.labelNRepeat.hide()
            self.ui.lblCurrentRepeatValue.hide()
            self.ui.lblRepeatText.hide()
            self.ui.lSamplesSentText.hide()
            self.ui.progressBar.hide()

        if self.mode == Mode.send or self.mode == Mode.spectrum:
            self.ui.lSamplesCaptured.hide()
            self.ui.lSamplesCapturedText.hide()
            self.ui.lSignalSize.hide()
            self.ui.lSignalSizeText.hide()
            self.ui.lTime.hide()
            self.ui.lTimeText.hide()
            self.ui.btnSave.hide()

        if self.mode == Mode.spectrum:
            self.ui.btnClear.hide()
            self.setWindowTitle("Spectrum analyzer")

        if self.mode == Mode.send:
            self.ui.btnStart.setIcon(QIcon.fromTheme("media-playback-start"))
            self.setWindowTitle("Send signal")
            self.ui.btnStart.setToolTip("Send data")
>>>>>>> b1ae517... Inital Commit

        self.ui.btnStop.setEnabled(False)
        self.ui.btnClear.setEnabled(False)
        self.ui.btnSave.setEnabled(False)
<<<<<<< HEAD

        self.start = 0

        self.bw_sr_are_locked = constants.SETTINGS.value("lock_bandwidth_sample_rate", True, bool)

        self.ui.spinBoxFreq.setValue(project_manager.device_conf["frequency"])
        self.ui.spinBoxSampleRate.setValue(project_manager.device_conf["sample_rate"])
        self.ui.spinBoxBandwidth.setValue(project_manager.device_conf["bandwidth"])
        self.ui.spinBoxGain.setValue(project_manager.device_conf["gain"])
        try:
            if_gain = project_manager.device_conf["if_gain"]
        except KeyError:
            if_gain = config.DEFAULT_IF_GAIN
        self.ui.spinBoxIFGain.setValue(if_gain)

        try:
            baseband_gain = project_manager.device_conf["baseband_gain"]
        except KeyError:
            baseband_gain = config.DEFAULT_BB_GAIN
        self.ui.spinBoxBasebandGain.setValue(baseband_gain)

        try:
            freq_correction = project_manager.device_conf["freq_correction"]
        except KeyError:
            freq_correction = config.DEFAULT_FREQ_CORRECTION
        self.ui.spinBoxFreqCorrection.setValue(freq_correction)

        self.ui.spinBoxNRepeat.setValue(constants.SETTINGS.value('num_sending_repeats', 1, type=int))
        device = project_manager.device

        self.ui.cbDevice.clear()
        items = self.get_devices_for_combobox()
        self.ui.cbDevice.addItems(items)

        if device in items:
            self.ui.cbDevice.setCurrentIndex(items.index(device))

        self.timer = QTimer(self)

        dev_name = self.ui.cbDevice.currentText()
        self.set_device_ui_items_visibility(dev_name)

        self.ui.btnLockBWSR.setChecked(self.bw_sr_are_locked)
        self.on_btn_lock_bw_sr_clicked()

        ip_range = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"
        ip_regex = QRegExp("^" + ip_range
                          + "\\." + ip_range
                          + "\\." + ip_range
                          + "\\." + ip_range + "$")
        self.ui.lineEditIP.setValidator(QRegExpValidator(ip_regex))


    @property
    def is_rx(self) -> bool:
        return not self.is_tx

    @property
    def rx_tx_prefix(self) -> str:
        return "rx_" if self.is_rx else "tx_"

    @property
    def has_empty_device_list(self):
        return self.ui.cbDevice.count() == 0

    @property
    def device(self) -> VirtualDevice:
        return self.__device

    @device.setter
    def device(self, value):
        self.__device = value

    def hide_send_ui_items(self):
        for item in ("spinBoxNRepeat", "labelNRepeat", "lblCurrentRepeatValue",
                     "lblRepeatText", "lSamplesSentText", "progressBar"):
            getattr(self.ui, item).hide()

    def hide_receive_ui_items(self):
        for item in ("lSamplesCaptured", "lSamplesCapturedText", "lSignalSize", "lSignalSizeText",
                     "lTime", "lTimeText", "btnSave", "labelReceiveBufferFull", "lReceiveBufferFullText"):
            getattr(self.ui, item).hide()

    def set_sniff_ui_items_visible(self, visible: bool):
        for item in self.ui.__dict__:
            if "_sniff_" in item:
                getattr(self.ui, item).setVisible(visible)

    def get_config_for_selected_device(self):
        device_name = self.ui.cbDevice.currentText()
        key = device_name if device_name in config.DEVICE_CONFIG.keys() else "Fallback"
        conf = config.DEVICE_CONFIG[key]
        return conf

    def sync_gain_sliders(self):
        conf = self.get_config_for_selected_device()
        prefix = self.rx_tx_prefix

        if prefix + "rf_gain" in conf:
            gain = min(conf[prefix + "rf_gain"], key=lambda x: abs(x - self.ui.spinBoxGain.value()))
            self.ui.spinBoxGain.setValue(gain)
            self.ui.spinBoxGain.valueChanged.emit(gain)
        if prefix + "if_gain" in conf:
            if_gain = min(conf[prefix + "if_gain"], key=lambda x: abs(x - self.ui.spinBoxIFGain.value()))
            self.ui.spinBoxIFGain.setValue(if_gain)
            self.ui.spinBoxIFGain.valueChanged.emit(if_gain)
        if prefix + "baseband_gain" in conf:
            baseband_gain = min(conf[prefix + "baseband_gain"],
                                key=lambda x: abs(x - self.ui.spinBoxBasebandGain.value()))
            self.ui.spinBoxBasebandGain.setValue(baseband_gain)
            self.ui.spinBoxBasebandGain.valueChanged.emit(baseband_gain)

    def set_device_ui_items_visibility(self, device_name: str):
        key = device_name if device_name in config.DEVICE_CONFIG.keys() else "Fallback"
        conf = config.DEVICE_CONFIG[key]
        key_ui_dev_param_map = {"center_freq": "Freq", "sample_rate": "SampleRate", "bandwidth": "Bandwidth"}

        for key, ui_item in key_ui_dev_param_map.items():
            spinbox = getattr(self.ui, "spinBox"+ui_item)  # type: QSpinBox
            label = getattr(self.ui, "label"+ui_item)  # type: QLabel
            if key in conf:
                spinbox.setVisible(True)
                label.setVisible(True)

                if isinstance(conf[key], list):
                    spinbox.allowed_values = conf[key]
                    spinbox.setMinimum(min(conf[key]))
                    spinbox.setMaximum(max(conf[key]))
                    spinbox.setSingleStep(conf[key][1] - conf[key][0])
                    spinbox.auto_update_step_size = False
                else:
                    spinbox.setMinimum(conf[key].start)
                    spinbox.setMaximum(conf[key].stop)
                    spinbox.auto_update_step_size = True
                    spinbox.allowed_values = "all"
                    spinbox.adjust_step()
            else:
                spinbox.setVisible(False)
                label.setVisible(False)

        self.ui.btnLockBWSR.setVisible("sample_rate" in conf and "bandwidth" in conf)

        if "freq_correction" in conf:
            self.ui.labelFreqCorrection.setVisible(True)
            self.ui.spinBoxFreqCorrection.setVisible(True)
            self.ui.spinBoxFreqCorrection.setMinimum(conf["freq_correction"].start)
            self.ui.spinBoxFreqCorrection.setMaximum(conf["freq_correction"].stop)
            self.ui.spinBoxFreqCorrection.setSingleStep(conf["freq_correction"].step)
        else:
            self.ui.labelFreqCorrection.setVisible(False)
            self.ui.spinBoxFreqCorrection.setVisible(False)

        if "direct_sampling" in conf:
            self.ui.labelDirectSampling.setVisible(True)
            self.ui.comboBoxDirectSampling.setVisible(True)
            items = [self.ui.comboBoxDirectSampling.itemText(i) for i in range(self.ui.comboBoxDirectSampling.count())]
            if items != conf["direct_sampling"]:
                self.ui.comboBoxDirectSampling.clear()
                self.ui.comboBoxDirectSampling.addItems(conf["direct_sampling"])
        else:
            self.ui.labelDirectSampling.setVisible(False)
            self.ui.comboBoxDirectSampling.setVisible(False)

        prefix = self.rx_tx_prefix
        key_ui_gain_map = {prefix + "rf_gain": "Gain", prefix + "if_gain": "IFGain",
                           prefix + "baseband_gain": "BasebandGain"}
        for conf_key, ui_element in key_ui_gain_map.items():
            getattr(self.ui, "label" + ui_element).setVisible(conf_key in conf)

            spinbox = getattr(self.ui, "spinBox" + ui_element)  # type: QSpinBox
            slider = getattr(self.ui, "slider" + ui_element)  # type: QSlider

            if conf_key in conf:
                gain_values = conf[conf_key]
                assert len(gain_values) >= 2
                spinbox.setMinimum(gain_values[0])
                spinbox.setMaximum(gain_values[-1])
                spinbox.setSingleStep(gain_values[1] - gain_values[0])
                spinbox.setVisible(True)

                slider.setMaximum(len(gain_values) - 1)
            else:
                spinbox.setVisible(False)
                slider.setVisible(False)
            getattr(self.ui, "slider" + ui_element).setVisible(conf_key in conf)

        self.ui.lineEditDeviceArgs.setVisible("device_args" in conf)
        self.ui.labelDeviceArgs.setVisible("device_args" in conf)
        self.ui.lineEditIP.setVisible("ip" in conf)
        self.ui.labelIP.setVisible("ip" in conf)
        self.ui.spinBoxPort.setVisible("port" in conf)
        self.ui.labelPort.setVisible("port" in conf)

    def set_device_ui_items_enabled(self, enabled: bool):
        self.ui.spinBoxFreq.setEnabled(enabled)
        self.ui.spinBoxGain.setEnabled(enabled)
        self.ui.sliderGain.setEnabled(enabled)
        self.ui.spinBoxIFGain.setEnabled(enabled)
        self.ui.sliderIFGain.setEnabled(enabled)
        self.ui.spinBoxBasebandGain.setEnabled(enabled)
        self.ui.sliderBasebandGain.setEnabled(enabled)
        self.ui.spinBoxBandwidth.setEnabled(enabled)
        self.ui.spinBoxSampleRate.setEnabled(enabled)
        self.ui.spinBoxFreqCorrection.setEnabled(enabled)
        self.ui.comboBoxDirectSampling.setEnabled(enabled)
        self.ui.lineEditIP.setEnabled(enabled)
        self.ui.spinBoxNRepeat.setEnabled(enabled)
        self.ui.cbDevice.setEnabled(enabled)
        self.ui.spinBoxPort.setEnabled(enabled)

    def emit_editing_finished_signals(self):
        self.ui.spinBoxFreq.editingFinished.emit()
        self.ui.spinBoxBandwidth.editingFinished.emit()
        self.ui.spinBoxGain.editingFinished.emit()
        self.ui.spinBoxIFGain.editingFinished.emit()
        self.ui.spinBoxBasebandGain.editingFinished.emit()
        self.ui.spinBoxNRepeat.editingFinished.emit()
        self.ui.spinBoxSampleRate.editingFinished.emit()
        self.ui.spinBoxFreqCorrection.editingFinished.emit()
        self.ui.lineEditIP.editingFinished.emit()
        self.ui.spinBoxPort.editingFinished.emit()
        self.ui.lineEditDeviceArgs.editingFinished.emit()

    def get_devices_for_combobox(self):
        items = []
        for device_name in self.backend_handler.DEVICE_NAMES:
            dev = self.backend_handler.device_backends[device_name.lower()]
            if self.is_tx and dev.is_enabled and dev.supports_tx:
                items.append(device_name)
            elif self.is_rx and dev.is_enabled and dev.supports_rx:
                items.append(device_name)

        if PluginManager().is_plugin_enabled("NetworkSDRInterface"):
            items.append(NetworkSDRInterfacePlugin.NETWORK_SDR_NAME)

        return items

    def set_bandwidth_status(self):
        if self.device is not None:
            self.ui.spinBoxBandwidth.setEnabled(self.device.bandwidth_is_adjustable)
            self.ui.btnLockBWSR.setEnabled(self.device.bandwidth_is_adjustable)

            if not self.device.bandwidth_is_adjustable:
                self.bw_sr_are_locked = False
                self.ui.spinBoxBandwidth.setToolTip(self.tr("Your driver of RTL-SDR does not support "
                                                            "setting the bandwidth. "
                                                            "If you need this feature, install a recent version."))
            else:
                self.ui.spinBoxBandwidth.setToolTip("")
                self.bw_sr_are_locked = self.ui.btnLockBWSR.isChecked()
=======
        self.start = 0
        self.already_saved = True

        self.ui.spinBoxFreq.setValue(freq)
        self.ui.spinBoxSampleRate.setValue(samp_rate)
        self.ui.spinBoxBandwidth.setValue(bw)
        self.ui.spinBoxGain.setValue(gain)
        self.ui.spinBoxNRepeat.setValue(constants.SETTINGS.value('num_sending_repeats', type=int))

        if self.mode == Mode.receive:
            self.device_thread = ReceiverThread(samp_rate, freq, gain, bw, parent=self)
        elif self.mode == Mode.send:
            self.device_thread = SenderThread(samp_rate, freq, gain, bw, parent=self)
            self.device_thread.data = modulated_data
            self.device_thread.samples_per_transmission = len(modulated_data)

            self.ui.progressBar.setMaximum(len(modulated_data))
        elif self.mode == Mode.spectrum:
            self.device_thread = SpectrumThread(samp_rate, freq, gain, bw, parent=self)

        self.device_thread.usrp_ip = self.ui.lineEditIP.text()

        self.ui.cbDevice.clear()
        items = []
        if constants.SETTINGS.value('usrp_available', type=bool):
            items.append("USRP")
        if constants.SETTINGS.value('hackrf_available', type=bool):
            items.append("HackRF")
        self.ui.cbDevice.addItems(items)
        if device in items:
            self.ui.cbDevice.setCurrentIndex(items.index(device))

        self.on_selected_device_changed()

        self.recorded_files = []

        self.timer = QTimer(self)

        if self.mode == Mode.receive or self.mode == Mode.send:
            self.scene_creator = LiveSceneManager(self.device_thread.data.real, parent=self)
        else:
            self.scene_creator = FFTSceneManager(parent=self, graphic_view=self.ui.graphicsView)

        self.ui.graphicsView.setScene(self.scene_creator.scene)

        ipRange = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"
        ipRegex = QRegExp("^" + ipRange
                          + "\\." + ipRange
                          + "\\." + ipRange
                          + "\\." + ipRange + "$")
        self.ui.lineEditIP.setValidator(QRegExpValidator(ipRegex))
        self.create_connects()
>>>>>>> b1ae517... Inital Commit

    def create_connects(self):
        self.ui.btnStart.clicked.connect(self.on_start_clicked)
        self.ui.btnStop.clicked.connect(self.on_stop_clicked)
        self.ui.btnClear.clicked.connect(self.on_clear_clicked)
<<<<<<< HEAD

        self.timer.timeout.connect(self.update_view)
        self.ui.spinBoxSampleRate.editingFinished.connect(self.on_spinbox_sample_rate_editing_finished)

        self.ui.spinBoxGain.editingFinished.connect(self.on_spinbox_gain_editing_finished)
        self.ui.spinBoxGain.valueChanged.connect(self.on_spinbox_gain_value_changed)
        self.ui.sliderGain.valueChanged.connect(self.on_slider_gain_value_changed)
        self.ui.spinBoxIFGain.editingFinished.connect(self.on_spinbox_if_gain_editing_finished)
        self.ui.spinBoxIFGain.valueChanged.connect(self.on_spinbox_if_gain_value_changed)
        self.ui.sliderIFGain.valueChanged.connect(self.on_slider_if_gain_value_changed)
        self.ui.spinBoxBasebandGain.editingFinished.connect(self.on_spinbox_baseband_gain_editing_finished)
        self.ui.spinBoxBasebandGain.valueChanged.connect(self.on_spinbox_baseband_gain_value_changed)
        self.ui.sliderBasebandGain.valueChanged.connect(self.on_slider_baseband_gain_value_changed)

        self.ui.spinBoxFreq.editingFinished.connect(self.on_spinbox_frequency_editing_finished)
        self.ui.spinBoxBandwidth.editingFinished.connect(self.on_spinbox_bandwidth_editing_finished)
        self.ui.spinBoxPort.editingFinished.connect(self.on_spinbox_port_editing_finished)
        self.ui.lineEditIP.editingFinished.connect(self.on_line_edit_ip_editing_finished)
        self.ui.lineEditDeviceArgs.editingFinished.connect(self.on_line_edit_device_args_editing_finished)

        self.ui.spinBoxFreqCorrection.editingFinished.connect(self.on_spinbox_freq_correction_editing_finished)
        self.ui.comboBoxDirectSampling.currentIndexChanged.connect(self.on_combobox_direct_sampling_index_changed)

        self.ui.cbDevice.currentIndexChanged.connect(self.on_selected_device_changed)
        self.ui.sliderYscale.valueChanged.connect(self.on_slider_y_scale_value_changed)

        self.ui.btnLockBWSR.clicked.connect(self.on_btn_lock_bw_sr_clicked)

        self.sync_gain_sliders()

    def _create_device_connects(self):
        self.device.stopped.connect(self.on_device_stopped)
        self.device.started.connect(self.on_device_started)
        self.device.sender_needs_restart.connect(self._restart_device_thread)

    def reset(self):
        self.ui.txtEditErrors.clear()
        self.device.current_index = 0
        self.device.current_iteration = 0
        self.ui.lSamplesCaptured.setText("0")
        self.ui.lSignalSize.setText("0")
        self.ui.lTime.setText("0")
        self.ui.lblCurrentRepeatValue.setText("-")
        self.scene_manager.set_text("")
        self.ui.progressBar.setValue(0)
        self.ui.btnClear.setEnabled(False)
        self.ui.btnSave.setEnabled(False)

    def init_device(self):
        pass

    def save_before_close(self):
        return True

    @pyqtSlot()
    def on_spinbox_sample_rate_editing_finished(self):
        self.device.sample_rate = self.ui.spinBoxSampleRate.value()
        if self.bw_sr_are_locked:
            self.ui.spinBoxBandwidth.setValue(self.ui.spinBoxSampleRate.value())
            self.device.bandwidth = self.ui.spinBoxBandwidth.value()

    @pyqtSlot()
    def on_spinbox_frequency_editing_finished(self):
        self.device.frequency = self.ui.spinBoxFreq.value()

    @pyqtSlot()
    def on_spinbox_bandwidth_editing_finished(self):
        self.device.bandwidth = self.ui.spinBoxBandwidth.value()
        if self.bw_sr_are_locked:
            self.ui.spinBoxSampleRate.setValue(self.ui.spinBoxBandwidth.value())
            self.device.sample_rate = self.ui.spinBoxSampleRate.value()

    @pyqtSlot()
    def on_line_edit_ip_editing_finished(self):
        self.device.ip = self.ui.lineEditIP.text()

    @pyqtSlot()
    def on_line_edit_device_args_editing_finished(self):
        self.device.device_args = self.ui.lineEditDeviceArgs.text()

    @pyqtSlot()
    def on_spinbox_port_editing_finished(self):
        self.device.port = self.ui.spinBoxPort.value()

    @pyqtSlot()
    def on_spinbox_freq_correction_editing_finished(self):
        self.device.freq_correction = self.ui.spinBoxFreqCorrection.value()

    @pyqtSlot(int)
    def on_combobox_direct_sampling_index_changed(self, index: int):
        self.device.direct_sampling_mode = index

    @pyqtSlot()
    def on_spinbox_gain_editing_finished(self):
        self.device.gain = self.ui.spinBoxGain.value()

    @pyqtSlot(int)
    def on_spinbox_gain_value_changed(self, value: int):
        dev_conf = self.get_config_for_selected_device()
        try:
            self.ui.sliderGain.setValue(dev_conf[self.rx_tx_prefix + "rf_gain"].index(value))
        except (ValueError, KeyError):
            pass

    @pyqtSlot(int)
    def on_slider_gain_value_changed(self, value: int):
        dev_conf = self.get_config_for_selected_device()
        self.ui.spinBoxGain.setValue(dev_conf[self.rx_tx_prefix + "rf_gain"][value])

    @pyqtSlot()
    def on_spinbox_if_gain_editing_finished(self):
        self.device.if_gain = self.ui.spinBoxIFGain.value()

    @pyqtSlot(int)
    def on_slider_if_gain_value_changed(self, value: int):
        dev_conf = self.get_config_for_selected_device()
        self.ui.spinBoxIFGain.setValue(dev_conf[self.rx_tx_prefix + "if_gain"][value])

    @pyqtSlot(int)
    def on_spinbox_if_gain_value_changed(self, value: int):
        dev_conf = self.get_config_for_selected_device()
        try:
            self.ui.sliderIFGain.setValue(dev_conf[self.rx_tx_prefix + "if_gain"].index(value))
        except (ValueError, KeyError):
            pass

    @pyqtSlot()
    def on_spinbox_baseband_gain_editing_finished(self):
        self.device.baseband_gain = self.ui.spinBoxBasebandGain.value()

    @pyqtSlot(int)
    def on_slider_baseband_gain_value_changed(self, value: int):
        dev_conf = self.get_config_for_selected_device()
        self.ui.spinBoxBasebandGain.setValue(dev_conf[self.rx_tx_prefix + "baseband_gain"][value])

    @pyqtSlot(int)
    def on_spinbox_baseband_gain_value_changed(self, value: int):
        dev_conf = self.get_config_for_selected_device()
        try:
            self.ui.sliderBasebandGain.setValue(dev_conf[self.rx_tx_prefix + "baseband_gain"].index(value))
        except (ValueError, KeyError):
            pass

    @pyqtSlot()
    def on_selected_device_changed(self):
        dev_name = self.ui.cbDevice.currentText()

        self.init_device()

        self.graphics_view.scene_manager = self.scene_manager
        self.graphics_view.setScene(self.scene_manager.scene)
        self.set_device_ui_items_visibility(dev_name)
        self.sync_gain_sliders()

        self.set_bandwidth_status()

    @pyqtSlot()
    def on_start_clicked(self):
        self.emit_editing_finished_signals()

    @pyqtSlot()
    def on_stop_clicked(self):
        self.device.stop("Stopped receiving: Stop button clicked")

    @pyqtSlot()
    def on_device_stopped(self):
        self.graphics_view.capturing_data = False
        self.set_device_ui_items_enabled(True)
        self.ui.btnStart.setEnabled(True)
        self.ui.btnStop.setEnabled(False)
        self.ui.btnClear.setEnabled(True)
        self.ui.btnSave.setEnabled(self.device.current_index > 0)

        self.timer.stop()
        self.scene_manager.set_text("")
        self.update_view()

    @pyqtSlot()
    def on_device_started(self):
        self.ui.txtEditErrors.clear()
        self.scene_manager.set_text("Waiting for device..")
        self.graphics_view.capturing_data = True
        self.ui.btnSave.setEnabled(False)
        self.ui.btnStart.setEnabled(False)

=======
        self.ui.btnSave.clicked.connect(self.on_save_clicked)
        self.device_thread.stopped.connect(self.on_device_thread_stopped)
        self.device_thread.started.connect(self.on_device_thread_started)
        self.device_thread.sender_needs_restart.connect(
            self.__restart_device_thread)
        self.timer.timeout.connect(self.update_view)
        self.ui.spinBoxSampleRate.editingFinished.connect(self.on_sample_rate_changed)
        self.ui.spinBoxGain.editingFinished.connect(self.on_gain_changed)
        self.ui.spinBoxFreq.editingFinished.connect(self.on_freq_changed)
        self.ui.spinBoxBandwidth.editingFinished.connect(self.on_bw_changed)
        self.ui.lineEditIP.editingFinished.connect(self.on_usrp_ip_changed)
        self.ui.cbDevice.currentIndexChanged.connect(self.on_selected_device_changed)
        self.ui.spinBoxNRepeat.editingFinished.connect(self.on_nrepeat_changed)
        self.ui.sliderYscale.valueChanged.connect(self.on_slideyscale_value_changed)

        self.ui.graphicsView.zoomed.connect(self.handle_signal_zoomed_or_scrolled)
        self.ui.graphicsView.horizontalScrollBar().valueChanged.connect(self.handle_signal_zoomed_or_scrolled)

    @property
    def has_empty_device_list(self):
        return self.ui.cbDevice.count() == 0

    @pyqtSlot()
    def on_sample_rate_changed(self):
        self.device_thread.sample_rate = self.ui.spinBoxSampleRate.value()

    @pyqtSlot()
    def on_freq_changed(self):
        self.device_thread.freq = self.ui.spinBoxFreq.value()
        if self.mode == Mode.spectrum:
            self.scene_creator.scene.center_freq = self.ui.spinBoxFreq.value()

    @pyqtSlot()
    def on_bw_changed(self):
        self.device_thread.bandwidth = self.ui.spinBoxBandwidth.value()

    @pyqtSlot()
    def on_usrp_ip_changed(self):
        self.device_thread.usrp_ip = self.ui.lineEditIP.text()

    @pyqtSlot()
    def on_gain_changed(self):
        self.device_thread.gain = self.ui.spinBoxGain.value()

    @pyqtSlot()
    def on_selected_device_changed(self):
        dev = self.ui.cbDevice.currentText()
        self.device_thread.device = dev
        self.ui.lineEditIP.setVisible(dev == "USRP")
        self.ui.labelIP.setVisible(dev == "USRP")

    @pyqtSlot()
    def on_start_clicked(self):
        if self.mode == Mode.send and self.ui.progressBar.value() >= self.ui.progressBar.maximum() - 1:
            self.on_clear_clicked()

        self.ui.spinBoxFreq.editingFinished.emit()
        self.ui.lineEditIP.editingFinished.emit()
        self.ui.spinBoxBandwidth.editingFinished.emit()
        self.ui.spinBoxSampleRate.editingFinished.emit()
        self.ui.spinBoxNRepeat.editingFinished.emit()

        self.device_thread.setTerminationEnabled(True)
        self.device_thread.terminate()
        time.sleep(0.1)

        self.device_thread.start()

    @pyqtSlot()
    def on_nrepeat_changed(self):
        if not self.ui.spinBoxNRepeat.isVisible():
            return

        if self.device_thread.max_repeats != self.ui.spinBoxNRepeat.value():
            self.device_thread.max_repeats = self.ui.spinBoxNRepeat.value()
            self.device_thread.current_iteration = 0
        self.device_thread.repeat_endless = self.ui.spinBoxNRepeat.value() == 0

    @pyqtSlot()
    def on_stop_clicked(self):
        self.device_thread.stop("Stopped receiving due to user interaction")

    @pyqtSlot()
    def on_device_thread_stopped(self):
        self.ui.graphicsView.capturing_data = False
        self.ui.btnStart.setEnabled(True)
        self.ui.btnStop.setEnabled(False)
        self.ui.btnClear.setEnabled(True)
        self.ui.btnSave.setEnabled(self.device_thread.current_index > 0)
        self.ui.spinBoxSampleRate.setEnabled(True)
        self.ui.spinBoxFreq.setEnabled(True)
        self.ui.lineEditIP.setEnabled(True)
        self.ui.spinBoxBandwidth.setEnabled(True)
        self.ui.spinBoxGain.setEnabled(True)
        self.ui.cbDevice.setEnabled(True)
        self.ui.spinBoxNRepeat.setEnabled(True)
        self.timer.stop()
        self.scene_creator.set_text("")
        self.update_view()

    @pyqtSlot()
    def on_device_thread_started(self):
        self.ui.txtEditErrors.clear()
        self.scene_creator.set_text("Waiting for device..")
        self.ui.graphicsView.capturing_data = True
        self.ui.btnSave.setEnabled(False)
        self.ui.btnStart.setEnabled(False)
>>>>>>> b1ae517... Inital Commit
        self.ui.btnClear.setEnabled(False)
        self.ui.spinBoxNRepeat.setEnabled(False)
        self.ui.btnStop.setEnabled(True)

<<<<<<< HEAD
        self.timer.start(self.update_interval)

    def update_view(self):
        self.ui.sliderYscale.setValue(int(self.graphics_view.transform().m22()))

        txt = self.ui.txtEditErrors.toPlainText()
        new_messages = self.device.read_messages()

        if "No devices found for" in new_messages:
            self.device.stop_on_error("Could not establish connection to USRP")
            Errors.usrp_found()

            self.on_clear_clicked()

        elif "FATAL: No supported devices found" in new_messages or \
                        "HACKRF_ERROR_NOT_FOUND" in new_messages or \
                        "HACKRF_ERROR_LIBUSB" in new_messages:
            self.device.stop_on_error("Could not establish connection to HackRF")
            Errors.hackrf_not_found()
            self.on_clear_clicked()

        elif "No module named gnuradio" in new_messages:
            self.device.stop_on_error("Did not find gnuradio.")
            Errors.gnuradio_not_installed()
            self.on_clear_clicked()

        elif "RTLSDR-open: Error Code: -1" in new_messages:
            self.device.stop_on_error("Could not open a RTL-SDR device.")
            self.on_clear_clicked()

        elif "Address already in use" in new_messages:
            self._restart_device_thread()

        if len(new_messages) > 1:
            self.ui.txtEditErrors.setPlainText(txt + new_messages)

        self.ui.progressBar.setValue(self.device.current_index)

        self.ui.lSamplesCaptured.setText("{0:n}".format(self.device.current_index))
        self.ui.lSignalSize.setText(locale.format_string("%.2f", (8 * self.device.current_index) / (1024 ** 2)))
        self.ui.lTime.setText(locale.format_string("%.2f", self.device.current_index / self.device.sample_rate))

        if self.is_rx and self.device.data is not None:
            self.ui.labelReceiveBufferFull.setText("{0}%".format(int(100 * self.device.current_index /
                                                                     len(self.device.data))))

        if self.device.current_index == 0:
            return False

        return True

    def _restart_device_thread(self):
        self.device.stop("Restarting with new port")
        QApplication.processEvents()

        if self.device.backend == Backends.grc:
            self.device.increase_gr_port()


        self.device.start()
=======
        if self.mode != Mode.spectrum:
            self.ui.spinBoxSampleRate.setDisabled(True)
            self.ui.spinBoxFreq.setDisabled(True)
            self.ui.spinBoxGain.setDisabled(True)
            self.ui.spinBoxBandwidth.setDisabled(True)

        self.ui.lineEditIP.setDisabled(True)
        self.ui.cbDevice.setDisabled(True)
        self.timer.start(self.update_interval)
        self.already_saved = False

    def update_view(self):
        txt = self.ui.txtEditErrors.toPlainText()
        new_errors = self.device_thread.read_errors()

        if "No devices found for" in new_errors:
            self.device_thread.stop("Could not establish connection to USRP")
            Errors.usrp_ip_not_found()

            self.on_clear_clicked()

        elif "FATAL: No supported devices found" in new_errors or \
                        "HACKRF_ERROR_NOT_FOUND" in new_errors or \
                        "HACKRF_ERROR_LIBUSB" in new_errors:
            self.device_thread.stop("Could not establish connection to HackRF")
            Errors.hackrf_not_found()
            self.on_clear_clicked()

        elif "No module named gnuradio" in new_errors:
            self.device_thread.stop("Did not find gnuradio.")
            Errors.gnuradio_not_installed()
            self.on_clear_clicked()

        elif "Address already in use" in new_errors:
            self.__restart_device_thread()

        if len(new_errors) > 1:
            self.ui.txtEditErrors.setPlainText(txt + new_errors)

        self.ui.progressBar.setValue(self.device_thread.current_index)

        self.ui.lSamplesCaptured.setText("{0:n}".format(self.device_thread.current_index))
        self.ui.lSignalSize.setText("{0:n}".format((8 * self.device_thread.current_index) / (1024 ** 2)))
        self.ui.lTime.setText(locale.format_string("%.2f", self.device_thread.current_index / self.device_thread.sample_rate))
        if self.device_thread.current_iteration is not None:
            self.ui.lblCurrentRepeatValue.setText(str(self.device_thread.current_iteration + 1))
        else:
            self.ui.lblCurrentRepeatValue.setText("Done")

        if self.device_thread.current_index == 0:
            return

        if self.mode == Mode.send or self.mode == Mode.receive:
            self.ui.graphicsView.horizontalScrollBar().blockSignals(True)
            self.scene_creator.end = self.device_thread.current_index
        elif self.mode == Mode.spectrum:
            x, y = self.device_thread.x, self.device_thread.y
            self.scene_creator.scene.frequencies = x
            self.scene_creator.plot_data = y
            if x is None or y is None:
                return

        self.scene_creator.init_scene()
        self.scene_creator.show_full_scene()
        self.ui.graphicsView.update()

    def __restart_device_thread(self):
        self.device_thread.stop("Restarting thread with new port")
        QApplication.processEvents()

        self.device_thread.port = random.randint(1024, 65536)
        print("Retry with port " + str(self.device_thread.port))
        self.device_thread.setTerminationEnabled(True)
        self.device_thread.terminate()
        time.sleep(1)

        self.device_thread.start()
>>>>>>> b1ae517... Inital Commit
        QApplication.processEvents()

    @pyqtSlot()
    def on_clear_clicked(self):
<<<<<<< HEAD
        pass

    def closeEvent(self, event: QCloseEvent):
        self.emit_editing_finished_signals()
        if self.device.backend == Backends.network:
            event.accept()
            return

        self.device.stop("Dialog closed. Killing recording process.")
        logger.debug("Device stopped successfully.")
        if not self.save_before_close():
            event.ignore()
            return

        time.sleep(0.1)
        if self.device.backend != Backends.none:
            # Backend none is selected, when no device is available
            logger.debug("Cleaning up device")
            self.device.cleanup()
            logger.debug("Successfully cleaned up device")
            self.recording_parameters.emit(str(self.device.name), dict(frequency=self.device.frequency,
                                                                       sample_rate=self.device.sample_rate,
                                                                       bandwidth=self.device.bandwidth,
                                                                       gain=self.device.gain,
                                                                       if_gain=self.device.if_gain,
                                                                       baseband_gain=self.device.baseband_gain,
                                                                       freq_correction=self.device.freq_correction
                                                                       ))

        event.accept()

    @pyqtSlot()
    def on_btn_lock_bw_sr_clicked(self):
        self.bw_sr_are_locked = self.ui.btnLockBWSR.isChecked()
        constants.SETTINGS.setValue("lock_bandwidth_sample_rate", self.bw_sr_are_locked)
        if self.bw_sr_are_locked:
            self.ui.btnLockBWSR.setIcon(QIcon(":/icons/data/icons/lock.svg"))
            self.ui.spinBoxBandwidth.setValue(self.ui.spinBoxSampleRate.value())
            self.ui.spinBoxBandwidth.editingFinished.emit()
        else:
            self.ui.btnLockBWSR.setIcon(QIcon(":/icons/data/icons/unlock.svg"))

    @pyqtSlot(int)
    def on_slider_y_scale_value_changed(self, new_value: int):
        # Scale Up = Top Half, Scale Down = Lower Half
        transform = self.graphics_view.transform()
        self.graphics_view.setTransform(QTransform(transform.m11(), transform.m12(), transform.m13(),
                                                   transform.m21(), new_value, transform.m23(),
                                                   transform.m31(), transform.m32(), transform.m33()))
=======
        if self.mode != Mode.spectrum:
            self.ui.txtEditErrors.clear()
            self.device_thread.clear_data()
            self.scene_creator.clear_path()
            self.device_thread.current_iteration = 0
            self.ui.graphicsView.repaint()
            self.ui.lSamplesCaptured.setText("0")
            self.ui.lSignalSize.setText("0")
            self.ui.lTime.setText("0")
            self.ui.lblCurrentRepeatValue.setText("-")
            self.scene_creator.set_text("")
            self.ui.progressBar.setValue(0)
            self.ui.btnClear.setEnabled(False)
            self.ui.btnSave.setEnabled(False)

    def on_save_clicked(self):
        data = self.device_thread.data[:self.device_thread.current_index]
        filename = FileOperator.save_data_dialog("recorded", data, parent=self)
        self.already_saved = True
        if filename is not None and filename not in self.recorded_files:
            self.recorded_files.append(filename)


    def closeEvent(self, QCloseEvent):
        self.device_thread.stop("Dialog closed. Killing recording process.")
        if self.mode == Mode.receive and not self.already_saved and self.device_thread.current_index > 0:
            reply = QMessageBox.question(self, self.tr("Save data?"),
                                         self.tr("Do you want to save the data you have captured so far?"),
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Abort)
            if reply == QMessageBox.Yes:
                self.on_save_clicked()
            elif reply == QMessageBox.Abort:
                QCloseEvent.ignore()
                return

        time.sleep(0.1)
        if self.mode == Mode.send:
            self.device_thread.socket.close()

        self.device_thread.data = None

        self.files_recorded.emit(self.recorded_files)
        self.recording_parameters.emit(str(self.device_thread.freq),
                                       str(self.device_thread.sample_rate),
                                       str(self.device_thread.bandwidth),
                                       str(self.device_thread.gain),
                                       str(self.device_thread.device))
        self.device_thread.quit()
        self.device_thread.deleteLater()

        QCloseEvent.accept()

    def handle_signal_zoomed_or_scrolled(self):
        if not self.ui.graphicsView.capturing_data:
            x1 = self.ui.graphicsView.view_rect().x()
            x2 = x1 + self.ui.graphicsView.view_rect().width()
            self.scene_creator.show_scene_section(x1, x2)

    @pyqtSlot(int)
    def on_slideyscale_value_changed(self, new_value: int):
        # Scale Up = Top Half, Scale Down = Lower Half
        middle = int((self.ui.sliderYscale.maximum() + 1 - self.ui.sliderYscale.minimum()) / 2)
        scale_up = new_value >= middle
        current_factor = self.ui.graphicsView.sceneRect().height() / self.ui.graphicsView.view_rect().height()
        scale_factor = (new_value + 1 - middle) / current_factor if scale_up else current_factor / new_value
        if scale_factor > 0:
            self.ui.graphicsView.scale(1, scale_factor)
>>>>>>> b1ae517... Inital Commit
