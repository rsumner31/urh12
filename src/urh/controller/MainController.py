import copy
import os
<<<<<<<+HEAD
import traceback

from PyQt5.QtCore import QDir, Qt, pyqtSlot, QFileInfo, QTimer
from PyQt5.QtGui import QIcon, QCloseEvent
=======

from PyQt5.QtCore import pyqtSignal, QDir, Qt, pyqtSlot, QFileInfo, QTimer
from PyQt5.QtGui import QIcon, QResizeEvent, QCloseEvent
>>>>>>>-b1ae517
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QMainWindow, QUndoGroup, QActionGroup, QHeaderView, QAction, QFileDialog, \
    QMessageBox, QApplication

from urh import constants
from urh import version
from urh.controller.CompareFrameController import CompareFrameController
from urh.controller.DecoderWidgetController import DecoderWidgetController
from urh.controller.GeneratorTabController import GeneratorTabController
from urh.controller.OptionsController import OptionsController
from urh.controller.ProjectDialogController import ProjectDialogController
<<<<<<<+HEAD
from urh.controller.ProtocolSniffDialogController import ProtocolSniffDialogController
from urh.controller.ReceiveDialogController import ReceiveDialogController
from urh.controller.SignalFrameController import SignalFrameController
from urh.controller.SignalTabController import SignalTabController
from urh.controller.SpectrumDialogController import SpectrumDialogController
from urh.models.FileFilterProxyModel import FileFilterProxyModel
from urh.models.FileIconProvider import FileIconProvider
from urh.models.FileSystemModel import FileSystemModel
from urh.models.ParticipantLegendListModel import ParticipantLegendListModel
=======
from urh.controller.SendRecvDialogController import SendRecvDialogController, Mode
from urh.controller.SignalFrameController import SignalFrameController
from urh.controller.SignalTabController import SignalTabController
from urh.models.FileFilterProxyModel import FileFilterProxyModel
from urh.models.FileIconProvider import FileIconProvider
from urh.models.FileSystemModel import FileSystemModel
>>>>>>>-b1ae517
from urh.plugins.PluginManager import PluginManager
from urh.signalprocessing.ProtocolAnalyzer import ProtocolAnalyzer
from urh.signalprocessing.Signal import Signal
from urh.ui.WavFileDialog import WavFileDialog
from urh.ui.ui_main import Ui_MainWindow
from urh.util import FileOperator
from urh.util.Errors import Errors
<<<<<<<+HEAD
from urh.util.Logger import logger
=======
>>>>>>>-b1ae517
from urh.util.ProjectManager import ProjectManager


class MainController(QMainWindow):
<<<<<<<+HEAD
=======
    resized = pyqtSignal()

>>>>>>>-b1ae517
    def __init__(self, *args):
        super().__init__(*args)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

<<<<<<<+HEAD
        OptionsController.write_default_options()

=======
>>>>>>>-b1ae517
        self.project_save_timer = QTimer()
        self.project_manager = ProjectManager(self)
        self.plugin_manager = PluginManager()
        self.signal_tab_controller = SignalTabController(self.project_manager,
<<<<<<<+HEAD
                                                         parent=self.ui.tab_interpretation)
=======
                                                                         parent=self.ui.tab_interpretation)
>>>>>>>-b1ae517
        self.ui.tab_interpretation.layout().addWidget(self.signal_tab_controller)
        self.compare_frame_controller = CompareFrameController(parent=self.ui.tab_protocol,
                                                               plugin_manager=self.plugin_manager,
                                                               project_manager=self.project_manager)

        self.ui.tab_protocol.layout().addWidget(self.compare_frame_controller)

        self.generator_tab_controller = GeneratorTabController(self.compare_frame_controller,
                                                               self.project_manager,
<<<<<<<+HEAD
=======
                                                               self.compare_frame_controller.decodings,
>>>>>>>-b1ae517
                                                               parent=self.ui.tab_generator)

        self.undo_group = QUndoGroup()
        self.undo_group.addStack(self.signal_tab_controller.signal_undo_stack)
        self.undo_group.addStack(self.compare_frame_controller.protocol_undo_stack)
        self.undo_group.addStack(self.generator_tab_controller.generator_undo_stack)
        self.undo_group.setActiveStack(self.signal_tab_controller.signal_undo_stack)
        self.ui.progressBar.hide()

<<<<<<<+HEAD
        self.participant_legend_model = ParticipantLegendListModel(self.project_manager.participants)
        self.ui.listViewParticipants.setModel(self.participant_legend_model)
=======

>>>>>>>-b1ae517

        gtc = self.generator_tab_controller
        gtc.ui.splitter.setSizes([gtc.width() / 0.7, gtc.width() / 0.3])

        self.ui.tab_generator.layout().addWidget(self.generator_tab_controller)

        self.signal_protocol_dict = {}
        """:type: dict[SignalFrameController,ProtocolAnalyzer]"""
        self.signal_tab_controller.ui.lLoadingFile.setText("")

        self.ui.lnEdtTreeFilter.setClearButtonEnabled(True)

        group = QActionGroup(self)
        self.ui.actionFSK.setActionGroup(group)
        self.ui.actionOOK.setActionGroup(group)
        self.ui.actionNone.setActionGroup(group)
        self.ui.actionPSK.setActionGroup(group)

<<<<<<<+HEAD
=======
        self.update_confirm_dialogs_checkbox()
        self.set_hold_shift_checkbox()

        self.signal_tab_controller.ui.lCtrlStatus.clear()
>>>>>>>-b1ae517
        self.signal_tab_controller.ui.lShiftStatus.clear()

        self.recentFileActionList = []
        self.create_connects()
<<<<<<<+HEAD
        self.update_recent_action_list()
=======
        self.updateRecentActionList()

        OptionsController.write_default_options()
>>>>>>>-b1ae517

        self.filemodel = FileSystemModel(self)
        path = QDir.homePath()

        self.filemodel.setIconProvider(FileIconProvider())
        self.filemodel.setRootPath(path)
        self.file_proxy_model = FileFilterProxyModel(self)
        self.file_proxy_model.setSourceModel(self.filemodel)
        self.ui.fileTree.setModel(self.file_proxy_model)

        self.ui.fileTree.setRootIndex(self.file_proxy_model.mapFromSource(self.filemodel.index(path)))
        self.ui.fileTree.setToolTip(path)
        self.ui.fileTree.header().setSectionResizeMode(0, QHeaderView.Stretch)
        self.ui.fileTree.header().setSectionResizeMode(1, QHeaderView.Interactive)
        self.ui.fileTree.setFocus()

        self.generator_tab_controller.table_model.cfc = self.compare_frame_controller

        self.ui.actionConvert_Folder_to_Project.setEnabled(False)

        undo_action = self.undo_group.createUndoAction(self)
        undo_action.setIcon(QIcon.fromTheme("edit-undo"))
        undo_action.setShortcut(QKeySequence.Undo)
        self.ui.menuEdit.insertAction(self.ui.actionMinimize_all, undo_action)

        redo_action = self.undo_group.createRedoAction(self)
        redo_action.setIcon(QIcon.fromTheme("edit-redo"))
        redo_action.setShortcut(QKeySequence.Redo)

        self.ui.splitter.setSizes([0, 1])

        self.ui.menuEdit.insertAction(self.ui.actionMinimize_all, redo_action)
        self.refresh_main_menu()

        self.apply_default_view()
        self.project_save_timer.start(ProjectManager.AUTOSAVE_INTERVAL_MINUTES * 60 * 1000)

<<<<<<<+HEAD
        self.ui.actionProject_settings.setVisible(False)
        self.ui.actionSave_project.setVisible(False)

        # Disabled because never used
        self.ui.actionMinimize_all.setVisible(False)
        self.ui.actionMaximize_all.setVisible(False)

    def create_connects(self):
        self.ui.actionFullscreen_mode.setShortcut(QKeySequence.FullScreen)
        self.ui.actionOpen.setShortcut(QKeySequence(QKeySequence.Open))
        self.ui.actionOpen_directory.setShortcut(QKeySequence("Ctrl+Shift+O"))
        self.ui.actionMinimize_all.setShortcut("F10")
        self.ui.actionMaximize_all.setShortcut("F11")

        self.ui.actionNew_Project.triggered.connect(self.on_new_project_action_triggered)
        self.ui.actionProject_settings.triggered.connect(self.on_project_settings_action_triggered)
        self.ui.actionSave_project.triggered.connect(self.project_manager.saveProject)

        self.ui.actionAbout_AutomaticHacker.triggered.connect(self.on_show_about_clicked)
        self.ui.actionRecord.triggered.connect(self.on_show_record_dialog_action_triggered)

        self.ui.actionFullscreen_mode.triggered.connect(self.on_fullscreen_action_triggered)
        self.ui.actionSaveAllSignals.triggered.connect(self.signal_tab_controller.save_all)
        self.ui.actionClose_all.triggered.connect(self.on_close_all_action_triggered)
        self.ui.actionOpen.triggered.connect(self.on_open_file_action_triggered)
        self.ui.actionOpen_directory.triggered.connect(self.on_open_directory_action_triggered)
        self.ui.actionDecoding.triggered.connect(self.on_show_decoding_dialog_triggered)
        self.ui.actionSpectrum_Analyzer.triggered.connect(self.on_show_spectrum_dialog_action_triggered)
        self.ui.actionOptions.triggered.connect(self.show_options_dialog_action_triggered)
        self.ui.actionSniff_protocol.triggered.connect(self.show_proto_sniff_dialog)
        self.ui.actionAbout_Qt.triggered.connect(QApplication.aboutQt)

        self.ui.actionMinimize_all.triggered.connect(self.signal_tab_controller.minimize_all)
        self.ui.actionMaximize_all.triggered.connect(self.signal_tab_controller.maximize_all)
        self.signal_tab_controller.frame_closed.connect(self.close_signal_frame)
        self.signal_tab_controller.signal_created.connect(self.add_signal)
        self.signal_tab_controller.ui.scrollArea.files_dropped.connect(self.on_files_dropped)
        self.signal_tab_controller.files_dropped.connect(self.on_files_dropped)
        self.signal_tab_controller.frame_was_dropped.connect(self.set_frame_numbers)

        self.compare_frame_controller.show_interpretation_clicked.connect(
            self.show_protocol_selection_in_interpretation)
        self.compare_frame_controller.files_dropped.connect(self.on_files_dropped)
        self.compare_frame_controller.show_decoding_clicked.connect(self.on_show_decoding_dialog_triggered)
        self.compare_frame_controller.ui.treeViewProtocols.files_dropped_on_group.connect(
            self.on_files_dropped_on_group)
        self.compare_frame_controller.participant_changed.connect(self.signal_tab_controller.on_participant_changed)
        self.compare_frame_controller.ui.treeViewProtocols.close_wanted.connect(self.on_cfc_close_wanted)
        self.compare_frame_controller.show_config_field_types_triggered.connect(
            self.on_show_field_types_config_action_triggered)

        self.ui.lnEdtTreeFilter.textChanged.connect(self.on_file_tree_filter_text_changed)

        self.ui.tabWidget.currentChanged.connect(self.on_selected_tab_changed)
        self.project_save_timer.timeout.connect(self.project_manager.saveProject)

        self.ui.actionConvert_Folder_to_Project.triggered.connect(self.project_manager.convert_folder_to_project)
        self.project_manager.project_loaded_status_changed.connect(self.ui.actionProject_settings.setVisible)
        self.project_manager.project_loaded_status_changed.connect(self.ui.actionSave_project.setVisible)
        self.project_manager.project_loaded_status_changed.connect(self.ui.actionConvert_Folder_to_Project.setDisabled)
        self.project_manager.project_updated.connect(self.on_project_updated)

        self.ui.textEditProjectDescription.textChanged.connect(self.on_text_edit_project_description_text_changed)
        self.ui.tabWidget_Project.tabBarDoubleClicked.connect(self.on_project_tab_bar_double_clicked)

        self.ui.listViewParticipants.doubleClicked.connect(self.on_project_settings_action_triggered)
=======

    def create_connects(self):
        self.ui.menuView.aboutToShow.connect(self.on_menu_view_clicked)
        self.ui.actionNew_Project.triggered.connect(self.on_new_project_clicked)
        self.ui.actionShow_file_tree.triggered.connect(self.on_show_file_tree_clicked)
        self.ui.actionCommon_Zoom.setShortcut(QKeySequence(Qt.SHIFT + Qt.Key_Z))
        self.ui.actionShow_Confirm_Close_Dialog.triggered.connect(self.update_confirm_dialogs_settings)
        self.ui.actionHold_Shift_to_Drag.triggered.connect(self.set_hold_shift)
        self.ui.actionAbout_AutomaticHacker.triggered.connect(self.show_about)
        self.ui.actionRecord.triggered.connect(self.show_record_dialog)
        self.signal_tab_controller.frame_closed.connect(self.close_signal_frame)
        self.signal_tab_controller.not_show_again_changed.connect(self.update_confirm_dialogs_checkbox)
        self.signal_tab_controller.signal_created.connect(self.add_signal)
        self.compare_frame_controller.show_interpretation_clicked.connect(
            self.show_protocol_selection_in_interpretation)
        self.signal_tab_controller.ui.scrollArea.files_dropped.connect(self.handle_files_dropped)
        self.signal_tab_controller.files_dropped.connect(self.handle_files_dropped)
        self.compare_frame_controller.files_dropped.connect(self.handle_files_dropped)
        self.signal_tab_controller.frame_was_dropped.connect(self.set_frame_numbers)
        self.ui.actionMinimize_all.triggered.connect(self.minimize_all)
        self.ui.actionMaximize_all.triggered.connect(self.maximize_all)
        self.ui.actionSaveAllSignals.triggered.connect(self.signal_tab_controller.save_all)
        self.ui.actionClose_all.triggered.connect(self.close_all)
        self.ui.actionSeperate_Protocols_in_Compare_Frame.triggered.connect(self.handle_compare_frame_seperation_changed)
        self.ui.actionOpen.triggered.connect(self.open)
        self.ui.actionOpen.setShortcut(QKeySequence(QKeySequence.Open))
        self.ui.actionMinimize_all.setShortcut("F10")
        self.ui.actionMaximize_all.setShortcut("F11")
        self.ui.lnEdtTreeFilter.textChanged.connect(self.handle_filtetree_filter_text_changed)
        self.ui.actionSort_Frames_by_Name.triggered.connect(self.sort_frames_by_name)
        self.ui.actionConvert_Folder_to_Project.triggered.connect(self.project_manager.convert_folder_to_project)
        self.ui.actionDecoding.triggered.connect(self.show_decoding_dialog)
        self.compare_frame_controller.show_decoding_clicked.connect(self.show_decoding_dialog)
        self.ui.tabWidget.currentChanged.connect(self.on_selected_tab_changed)
        self.ui.actionSpectrum_Analyzer.triggered.connect(self.show_spectrum_dialog)
        self.ui.actionOptions.triggered.connect(self.show_options_dialog)
        self.project_save_timer.timeout.connect(self.project_manager.saveProject)
        self.ui.actionSniff_protocol.triggered.connect(
            self.compare_frame_controller.show_proto_sniff_dialog)

        self.compare_frame_controller.ui.treeViewProtocols.files_dropped_on_group.connect(
            self.handle_files_dropped)

>>>>>>>-b1ae517

        self.ui.menuFile.addSeparator()
        for i in range(constants.MAX_RECENT_FILE_NR):
            recentFileAction = QAction(self)
            recentFileAction.setVisible(False)
<<<<<<<+HEAD
            recentFileAction.triggered.connect(self.on_open_recent_action_triggered)
            self.recentFileActionList.append(recentFileAction)
            self.ui.menuFile.addAction(self.recentFileActionList[i])

    def add_protocol_file(self, filename):

        proto = self.compare_frame_controller.add_protocol_from_file(filename)
        if proto:
            sf = self.signal_tab_controller.add_empty_frame(filename, proto)
            self.signal_protocol_dict[sf] = proto
            self.set_frame_numbers()
            self.file_proxy_model.open_files.add(filename)

    def add_fuzz_profile(self, filename):
        self.ui.tabWidget.setCurrentIndex(2)
        self.generator_tab_controller.load_from_file(filename)

    def add_signalfile(self, filename: str, group_id=0):
        if not os.path.exists(filename):
            QMessageBox.critical(self, self.tr("File not Found"),
                                 self.tr("The file {0} could not be found. Was it moved or renamed?").format(
                                     filename))
=======
            recentFileAction.triggered.connect(self.openRecent)
            self.recentFileActionList.append(recentFileAction)
            self.ui.menuFile.addAction(self.recentFileActionList[i])

    @pyqtSlot()
    def update_confirm_dialogs_checkbox(self):
        settings = constants.SETTINGS
        try:
            not_show = settings.value('not_show_close_dialog', type=bool)
        except TypeError:
            not_show = False
        self.ui.actionShow_Confirm_Close_Dialog.setChecked(not not_show)

    @pyqtSlot()
    def update_confirm_dialogs_settings(self):
        settings = constants.SETTINGS
        settings.setValue('not_show_close_dialog', not self.ui.actionShow_Confirm_Close_Dialog.isChecked())

    @pyqtSlot()
    def on_menu_view_clicked(self):
        file_tree_shown = self.ui.splitter.sizes()[0] > 0
        self.ui.actionShow_file_tree.setChecked(file_tree_shown)

    @pyqtSlot()
    def on_show_file_tree_clicked(self):
        show = self.ui.actionShow_file_tree.isChecked()
        if show:
            self.ui.splitter.setSizes([1, 1])
        else:
            self.ui.splitter.setSizes([0, 1])


    def set_hold_shift_checkbox(self):
        settings = constants.SETTINGS
        if 'hold_shift_to_drag' in settings.allKeys():
            hold_shift = settings.value('hold_shift_to_drag', type=bool)
        else:
            hold_shift = True
            settings.setValue('hold_shift_to_drag', hold_shift)

        self.ui.actionHold_Shift_to_Drag.setChecked(hold_shift)

    @pyqtSlot()
    def set_hold_shift(self):
        hs = self.ui.actionHold_Shift_to_Drag.isChecked()
        constants.SETTINGS.setValue('hold_shift_to_drag', hs)

    @pyqtSlot()
    def open(self):
        fip = FileIconProvider()
        self.dialog = QFileDialog(self)
        #tree = self.dialog.findChild(QTreeView)
        #""":type: QTreeView """
        #tree.setRootIsDecorated(True)
        #tree.setItemsExpandable(True)

        # Damit SignalClick Behavior auch geht. Nachteil: Man muss immer den Open Button drücken
        #tree.blockSignals(True)
        self.dialog.setIconProvider(fip)
        self.dialog.setDirectory(FileOperator.RECENT_PATH)
        self.dialog.setWindowTitle("Open Folder")
        self.dialog.setFileMode(QFileDialog.ExistingFiles)
        self.dialog.setOptions(QFileDialog.DontUseNativeDialog | QFileDialog.DontResolveSymlinks)
        self.dialog.setViewMode(QFileDialog.Detail)
        self.dialog.setNameFilter(
            "All files (*);;Complex Files *.complex (*.complex);;Wav Files *.wav (*.wav);;Protocols *.txt (*.txt);;"
            "Tar Archives (*.tar *.tar.gz *.tar.bz2);;Zip Archives (*.zip)")

        self.dialog.currentChanged.connect(self.handle_dialog_selection_changed)

        if self.dialog.exec_():
            fileNames = self.dialog.selectedFiles()
            folders = [folder for folder in fileNames if os.path.isdir(folder)]

            if len(folders) > 0:
                folder = folders[0]
                for f in self.signal_tab_controller.signal_frames:
                    self.close_signal_frame(f)

                self.project_manager.set_project_folder(folder)
            else:
                fileNames = FileOperator.uncompress_archives(fileNames, QDir.tempPath())
                self.add_files(fileNames)

    @pyqtSlot(str)
    def handle_dialog_selection_changed(self, path: str):
        if os.path.isdir(path):
            self.dialog.setFileMode(QFileDialog.Directory)
            self.dialog.setNameFilter(
                "All files (*);;Complex Files *.complex (*.complex);;Wav Files *.wav (*.wav);;Protocols *.txt (*.txt);;"
                "Tar Archives (*.tar *.tar.gz *.tar.bz2);;Zip Archives (*.zip)")
        else:
            self.dialog.setFileMode(QFileDialog.ExistingFiles)
            self.dialog.setNameFilter(
                "All files (*);;Complex Files *.complex (*.complex);;Wav Files *.wav (*.wav);;Protocols *.txt (*.txt);;"
                "Tar Archives (*.tar *.tar.gz *.tar.bz2);;Zip Archives (*.zip)")


    def add_protocol_file(self, filename):

        protolist = self.compare_frame_controller.add_protocol_from_file(filename)
        protolist = protolist if protolist is not None else []

        for pa in protolist:
            sf = self.signal_tab_controller.add_empty_frame(filename, pa.decoded_proto_bits_str)
            self.signal_protocol_dict[sf] = pa
            self.set_frame_numbers()
            self.file_proxy_model.open_files.add(filename)

    def add_signalfile(self, filename: str, group_id=0):
        if not os.path.exists(filename):
            QMessageBox.critical(self, self.tr("File not Found"),
                                       self.tr("The file {0} could not be found. Was it moved or renamed?").format(
                                           filename))
>>>>>>>-b1ae517
           return

        alrdy_qad_demod = False
        if filename.endswith(".wav"):
            accept, alrdy_qad_demod = WavFileDialog.dialog(self)
            if not accept:
                return

        sig_name = os.path.splitext(os.path.basename(filename))[0]

        # Use default sample rate for signal
        # Sample rate will be overriden in case of a project later
        signal = Signal(filename, sig_name, wav_is_qad_demod=alrdy_qad_demod,
<                        sample_rate=self.project_manager.device_conf["sample_rate"])

        if self.project_manager.project_file is None:
            self.adjust_for_current_file(signal.filename)
>>>>>>>+HEAD
======
                         sample_rate=self.project_manager.sample_rate)

        if self.project_manager.project_file is None:
            self.adjustForCurrentFile(signal.filename)
>>>>>>>-b1ae517
        self.file_proxy_model.open_files.add(filename)
        self.add_signal(signal, group_id)

    def add_signal(self, signal, group_id=0):
        self.ui.progressBar.setMaximum(100)
        self.ui.progressBar.show()

        pa = ProtocolAnalyzer(signal)
        sframe = self.signal_tab_controller.add_signal_frame(pa)
        self.ui.progressBar.setValue(10)
        QApplication.processEvents()

        pa = self.compare_frame_controller.add_protocol(pa, group_id)
        self.ui.progressBar.setValue(20)
        QApplication.processEvents()

        signal.blockSignals(True)
        has_entry = self.project_manager.read_project_file_for_signal(signal)
        if not has_entry:
            signal.auto_detect()
        signal.blockSignals(False)
        self.ui.progressBar.setValue(50)
        QApplication.processEvents()

        self.ui.progressBar.setValue(70)
        QApplication.processEvents()

<>>>>>>>+HEAD
======
         #pa.protocol_labels = self.project_manager.read_labels_for_filename(signal.filename)
>>>>>>>-b1ae517
       self.signal_protocol_dict[sframe] = pa
        self.ui.progressBar.setValue(80)
        QApplication.processEvents()

        sframe.refresh(draw_full_signal=True)  # Hier wird das Protokoll ausgelesen
<        if self.project_manager.read_participants_for_signal(signal, pa.messages):
            sframe.ui.gvSignal.redraw_view()

        sframe.ui.gvSignal.auto_fit_view()
>>>>>>>+HEAD
======
         sframe.ui.gvSignal.autofit_view()
        self.resized.connect(sframe.redraw_after_resize)
>>>>>>>-b1ae517
       self.set_frame_numbers()
        self.ui.progressBar.setValue(99)
        QApplication.processEvents()

<        self.compare_frame_controller.filter_search_results()

>>>>>>>+HEAD
======
>>>>>>>>-b1ae517
       self.refresh_main_menu()
        self.ui.progressBar.hide()

    def close_signal_frame(self, signal_frame: SignalFrameController):
<        try:
            self.project_manager.write_signal_information_to_project_file(signal_frame.signal)
            try:
                proto = self.signal_protocol_dict[signal_frame]
            except KeyError:
                proto = None

            if proto is not None:
                self.compare_frame_controller.remove_protocol(proto)
                # Needs to be removed in generator also, otherwise program crashes,
                # if item from tree in generator is selected and corresponding signal is closed
                self.generator_tab_controller.tree_model.remove_protocol(proto)

                proto.destroy()
                del self.signal_protocol_dict[signal_frame]

            if self.signal_tab_controller.ui.scrlAreaSignals.minimumHeight() > signal_frame.height():
                self.signal_tab_controller.ui.scrlAreaSignals.setMinimumHeight(
                    self.signal_tab_controller.ui.scrlAreaSignals.minimumHeight() - signal_frame.height())

            if signal_frame.signal is not None:
                # Non-Empty Frame (when a signal and not a protocol is opended)
                self.file_proxy_model.open_files.discard(signal_frame.signal.filename)
                signal_frame.scene_manager.deleteLater()
                signal_frame.signal.destroy()
                signal_frame.signal.deleteLater()
                signal_frame.proto_analyzer.destroy()
            signal_frame.proto_analyzer = None
            signal_frame.close()
            QApplication.processEvents()
            signal_frame.destroy()
            QApplication.processEvents()

            self.compare_frame_controller.ui.treeViewProtocols.expandAll()
            self.set_frame_numbers()
            self.refresh_main_menu()
        except Exception as e:
            Errors.generic_error(self.tr("Failed to close"), str(e), traceback.format_exc())
            self.ui.progressBar.hide()
            self.unsetCursor()

    def update_recent_action_list(self):
        recent_file_paths = constants.SETTINGS.value("recentFiles")
        recent_file_paths = [p for p in recent_file_paths if os.path.exists(p)] if recent_file_paths else []
        it_end = len(recent_file_paths) if len(
            recent_file_paths) < constants.MAX_RECENT_FILE_NR else constants.MAX_RECENT_FILE_NR

        for i in range(it_end):
            suffix = " (Directory)" if os.path.isdir(recent_file_paths[i]) else ""
            stripped_name = QFileInfo(recent_file_paths[i]).fileName() + suffix
            self.recentFileActionList[i].setText(stripped_name)
            self.recentFileActionList[i].setData(recent_file_paths[i])
            self.recentFileActionList[i].setVisible(True)

        for i in range(it_end, constants.MAX_RECENT_FILE_NR):
            self.recentFileActionList[i].setVisible(False)

        constants.SETTINGS.setValue("recentFiles", recent_file_paths)
>>>>>>>+HEAD
======
         self.project_manager.write_signal_information_to_project_file(signal_frame.signal)
        try:
            proto = self.signal_protocol_dict[signal_frame]
        except KeyError:
            proto = None

        if proto is not None:
            self.compare_frame_controller.remove_protocol(proto)

            proto.destroy()
            del self.signal_protocol_dict[signal_frame]

        if self.signal_tab_controller.ui.scrlAreaSignals.minimumHeight() > signal_frame.height():
            self.signal_tab_controller.ui.scrlAreaSignals.setMinimumHeight(
                self.signal_tab_controller.ui.scrlAreaSignals.minimumHeight() - signal_frame.height())

        if signal_frame.signal is not None:
            # Non-Empty Frame (when a signal and not a protocol is opended)
            self.file_proxy_model.open_files.discard(signal_frame.signal.filename)
            signal_frame.scene_creator.deleteLater()
            signal_frame.signal.destroy()
            signal_frame.signal.deleteLater()
            signal_frame.proto_analyzer.destroy()
        signal_frame.close()
        QApplication.processEvents()
        signal_frame.destroy()
        QApplication.processEvents()

        self.set_frame_numbers()
        self.refresh_main_menu()

    def resizeEvent(self, event: QResizeEvent):
        event.accept()
        self.resized.emit()

    def updateRecentActionList(self):
        recentFilePaths = constants.SETTINGS.value("recentFiles")
        recentFilePaths = [p for p in recentFilePaths if os.path.exists(p)] if recentFilePaths else []
        itEnd = len(recentFilePaths) if len(
            recentFilePaths) < constants.MAX_RECENT_FILE_NR else constants.MAX_RECENT_FILE_NR

        for i in range(itEnd):
            suffix = " (Directory)" if os.path.isdir(recentFilePaths[i]) else ""
            strippedName = QFileInfo(recentFilePaths[i]).fileName() + suffix
            self.recentFileActionList[i].setText(strippedName)
            self.recentFileActionList[i].setData(recentFilePaths[i])
            self.recentFileActionList[i].setVisible(True)

        for i in range(itEnd, constants.MAX_RECENT_FILE_NR):
            self.recentFileActionList[i].setVisible(False)

        constants.SETTINGS.setValue("recentFiles", recentFilePaths)

    @pyqtSlot(str)
    def adjustForCurrentFile(self, filePath):
        if filePath in FileOperator.archives.keys():
            filePath = copy.copy(FileOperator.archives[filePath])

        settings = constants.SETTINGS
        recentFilePaths = settings.value("recentFiles")
        if recentFilePaths is None:
            recentFilePaths = []

        recentFilePaths = [p for p in recentFilePaths if p != filePath]
        recentFilePaths.insert(0, filePath)

        while len(recentFilePaths) > constants.MAX_RECENT_FILE_NR:
            recentFilePaths.pop()

        settings.setValue("recentFiles", recentFilePaths)

        self.updateRecentActionList()

    @pyqtSlot()
    def openRecent(self):
        action = self.sender()
        if os.path.isdir(action.data()):
            self.project_manager.set_project_folder(action.data())
        elif os.path.isfile(action.data()):
            self.add_files(FileOperator.uncompress_archives([action.data()], QDir.tempPath()))

    @pyqtSlot()
    def show_about(self):
        QMessageBox.about(self, self.tr("About"), self.tr("Version: {0}").format(version.VERSION))

    @pyqtSlot(CompareFrameController, int, int, int, int)
    def show_protocol_selection_in_interpretation(self, startblock, start, endblock, end):
        cfc = self.compare_frame_controller
        total_block = 0
        last_sig_frame = None
        for protocol in cfc.protocol_list:
            if not protocol.show:
                continue
            n = protocol.num_blocks
            view_type = cfc.ui.cbProtoView.currentIndex()
            blocks = [i - total_block for i in range(total_block, total_block + n) if startblock <= i <= endblock]
            if len(blocks) > 0:
                try:
                    signal_frame = next((sf for sf, pf in self.signal_protocol_dict.items() if pf == protocol))
                except StopIteration:
                    QMessageBox.critical(self, self.tr("Error"),
                                         self.tr("Could not find corresponding signal frame."))
                    return
                signal_frame.set_roi_from_protocol_analysis(min(blocks), start, max(blocks), end + 1, view_type)
                last_sig_frame = signal_frame
            total_block += n
        focus_frame = last_sig_frame
        if last_sig_frame is not None:
            self.signal_tab_controller.ui.scrollArea.ensureWidgetVisible(last_sig_frame, 0, 0)

        QApplication.processEvents()
        self.ui.tabWidget.setCurrentIndex(0)
        if focus_frame is not None:
            focus_frame.ui.txtEdProto.setFocus()

    def handle_files_dropped(self, files, group_id=0):
        """
        :type files: list of QtCore.QUrl
        """
        localfiles = [fileurl.path() for fileurl in files if fileurl.isLocalFile()]

        if len(localfiles) > 0:
            self.add_files(FileOperator.uncompress_archives(localfiles, QDir.tempPath()), group_id)
>>>>>>>-b1ae517
    def add_files(self, filepaths, group_id=0):
        num_files = len(filepaths)
        if num_files == 0:
            return

        for i, file in enumerate(filepaths):
            if not os.path.exists(file):
                continue

            if os.path.isdir(file):
                for f in self.signal_tab_controller.signal_frames:
                    self.close_signal_frame(f)

                FileOperator.RECENT_PATH = file
                self.project_manager.set_project_folder(file)
                return

<            _, file_extension = os.path.splitext(file)
>>>>>>>+HEAD
======
             _, fileExtension = os.path.splitext(file)
>>>>>>>-b1ae517
           FileOperator.RECENT_PATH = os.path.split(file)[0]

            self.signal_tab_controller.ui.lLoadingFile.setText(
                self.tr("Loading File {0:d}/{1:d}".format(i + 1, num_files)))
            QApplication.processEvents()

            QApplication.setOverrideCursor(Qt.WaitCursor)

<            if file_extension == ".complex":
                self.add_signalfile(file, group_id)
            elif file_extension == ".coco":
                self.add_signalfile(file, group_id)
            elif file_extension == ".proto":
                self.add_protocol_file(file)
            elif file_extension == ".wav":
                self.add_signalfile(file, group_id)
            elif file_extension == ".fuzz":
                self.add_fuzz_profile(file)
>>>>>>>+HEAD
======
             if fileExtension == ".complex":
                self.add_signalfile(file, group_id)
            elif fileExtension == ".coco":
                self.add_signalfile(file, group_id)
            elif fileExtension == ".txt":
                self.add_protocol_file(file)
            elif fileExtension == ".wav":
                self.add_signalfile(file, group_id)
>>>>>>>-b1ae517
           else:
                self.add_signalfile(file, group_id)

            QApplication.restoreOverrideCursor()
        self.signal_tab_controller.ui.lLoadingFile.setText("")

    def set_frame_numbers(self):
        self.signal_tab_controller.set_frame_numbers()

<    def closeEvent(self, event: QCloseEvent):
        self.project_manager.saveProject()
        event.accept()

    def close_all(self):
        self.filemodel.setRootPath(QDir.homePath())
        self.ui.fileTree.setRootIndex(self.file_proxy_model.mapFromSource(self.filemodel.index(QDir.homePath())))
        self.project_manager.saveProject()

        self.signal_tab_controller.close_all()
        self.compare_frame_controller.reset()
        self.generator_tab_controller.close_all()

        self.project_manager.project_path = ""
        self.project_manager.project_file = None
        self.signal_tab_controller.signal_undo_stack.clear()
        self.compare_frame_controller.protocol_undo_stack.clear()
        self.generator_tab_controller.generator_undo_stack.clear()

    def show_options_dialog_specific_tab(self, tab_index: int):
        op = OptionsController(self.plugin_manager.installed_plugins, parent=self)
        op.values_changed.connect(self.on_options_changed)
        op.ui.tabWidget.setCurrentIndex(tab_index)
        op.show()

    def refresh_main_menu(self):
        enable = len(self.signal_protocol_dict) > 0
        self.ui.actionSaveAllSignals.setEnabled(enable)
        self.ui.actionClose_all.setEnabled(enable)

    def apply_default_view(self):
        view_index = constants.SETTINGS.value('default_view', type=int)
        self.compare_frame_controller.ui.cbProtoView.setCurrentIndex(view_index)
        self.generator_tab_controller.ui.cbViewType.setCurrentIndex(view_index)
        for sig_frame in self.signal_tab_controller.signal_frames:
            sig_frame.ui.cbProtoView.setCurrentIndex(view_index)

    def show_project_settings(self):
        pdc = ProjectDialogController(new_project=False, project_manager=self.project_manager, parent=self)
        pdc.finished.connect(self.on_project_dialog_finished)
        pdc.show()

    def collapse_project_tab_bar(self):
        self.ui.tabParticipants.hide()
        self.ui.tabDescription.hide()
        self.ui.tabWidget_Project.setMaximumHeight(self.ui.tabWidget_Project.tabBar().height())

    def expand_project_tab_bar(self):
        self.ui.tabDescription.show()
        self.ui.tabParticipants.show()
        self.ui.tabWidget_Project.setMaximumHeight(9000)

    @pyqtSlot()
    def on_project_tab_bar_double_clicked(self):
        if self.ui.tabParticipants.isVisible():
            self.collapse_project_tab_bar()
        else:
            self.expand_project_tab_bar()

    @pyqtSlot()
    def on_project_updated(self):
        self.participant_legend_model.participants = self.project_manager.participants
        self.participant_legend_model.update()
        self.compare_frame_controller.refresh()
        self.ui.textEditProjectDescription.setText(self.project_manager.description)

    @pyqtSlot()
    def on_fullscreen_action_triggered(self):
        if self.ui.actionFullscreen_mode.isChecked():
            self.showFullScreen()
        else:
            self.showMaximized()

    @pyqtSlot(str)
    def adjust_for_current_file(self, file_path):
        if file_path in FileOperator.archives.keys():
            file_path = copy.copy(FileOperator.archives[file_path])

        settings = constants.SETTINGS
        recent_file_paths = settings.value("recentFiles", [])
        recent_file_paths = [p for p in recent_file_paths if p != file_path]
        recent_file_paths.insert(0, file_path)

        while len(recent_file_paths) > constants.MAX_RECENT_FILE_NR:
            recent_file_paths.pop()

        settings.setValue("recentFiles", recent_file_paths)

        self.update_recent_action_list()

    @pyqtSlot()
    def on_show_field_types_config_action_triggered(self):
        self.show_options_dialog_specific_tab(tab_index=3)

    @pyqtSlot()
    def on_open_recent_action_triggered(self):
        action = self.sender()
        try:
            if os.path.isdir(action.data()):
                self.project_manager.set_project_folder(action.data())
            elif os.path.isfile(action.data()):
                self.add_files(FileOperator.uncompress_archives([action.data()], QDir.tempPath()))
        except Exception as e:
            Errors.generic_error(self.tr("Failed to open"), str(e), traceback.format_exc())
            self.ui.progressBar.hide()
            self.unsetCursor()

    @pyqtSlot()
    def on_show_about_clicked(self):
        descr = "<b><h2>Universal Radio Hacker</h2></b>Version: {0}<br />" \
                "GitHub: <a href='https://github.com/jopohl/urh'>https://github.com/jopohl/urh</a><br /><br />" \
                "Contributors:<i><ul><li>" \
                "Johannes Pohl &lt;<a href='mailto:joahnnes.pohl90@gmail.com'>johannes.pohl90@gmail.com</a>&gt;</li>" \
                "<li>Andreas Noack &lt;<a href='mailto:andreas.noack@fh-stralsund.de'>andreas.noack@fh-stralsund.de</a>&gt;</li>" \
                "</ul></i>".format(version.VERSION)

        QMessageBox.about(self, self.tr("About"), self.tr(descr))

    @pyqtSlot(int, int, int, int)
    def show_protocol_selection_in_interpretation(self, start_message, start, end_message, end):
        cfc = self.compare_frame_controller
        msg_total = 0
        last_sig_frame = None
        for protocol in cfc.protocol_list:
            if not protocol.show:
                continue
            n = protocol.num_messages
            view_type = cfc.ui.cbProtoView.currentIndex()
            messages = [i - msg_total for i in range(msg_total, msg_total + n) if start_message <= i <= end_message]
            if len(messages) > 0:
                try:
                    signal_frame = next((sf for sf, pf in self.signal_protocol_dict.items() if pf == protocol))
                except StopIteration:
                    QMessageBox.critical(self, self.tr("Error"),
                                         self.tr("Could not find corresponding signal frame."))
                    return
                signal_frame.set_roi_from_protocol_analysis(min(messages), start, max(messages), end + 1, view_type)
                last_sig_frame = signal_frame
            msg_total += n
        focus_frame = last_sig_frame
        if last_sig_frame is not None:
            self.signal_tab_controller.ui.scrollArea.ensureWidgetVisible(last_sig_frame, 0, 0)

        QApplication.processEvents()
        self.ui.tabWidget.setCurrentIndex(0)
        if focus_frame is not None:
            focus_frame.ui.txtEdProto.setFocus()

    @pyqtSlot(str)
    def on_file_tree_filter_text_changed(self, text: str):
        if len(text) > 0:
            self.filemodel.setNameFilters(["*" + text + "*"])
        else:
            self.filemodel.setNameFilters(["*"])

    @pyqtSlot()
    def on_show_decoding_dialog_triggered(self):
>>>>>>>+HEAD
======
     @pyqtSlot()
    def minimize_all(self):
        self.signal_tab_controller.minimize_all()

    @pyqtSlot()
    def maximize_all(self):
        self.signal_tab_controller.maximize_all()

    @pyqtSlot()
    def handle_compare_frame_seperation_changed(self):
        show_seperation = self.ui.actionSeperate_Protocols_in_Compare_Frame.isChecked()
        self.compare_frame_controller.show_protocol_seperation = show_seperation

    @pyqtSlot()
    def handle_filtetree_filter_text_changed(self):
        text = self.ui.lnEdtTreeFilter.text()

        if len(text) > 0:
            self.filemodel.setNameFilters(["*"+text+"*"])
        else:
            self.filemodel.setNameFilters(["*"])



    def closeEvent(self, event: QCloseEvent):
        self.project_manager.saveProject()
        event.accept()

    @pyqtSlot()
    def sort_frames_by_name(self):
        sorted_frame_names = [frame.name for frame in self.compare_frame_controller.protocol_list]
        sorted_frame_names.sort()
        considered_frames = []
        for i, sorted_frame_name in enumerate(sorted_frame_names):
            cur_frame = self.compare_frame_controller.protocol_list[i]
            if cur_frame.name != sorted_frame_name:
                frame_should_be_here = next(f for f in self.compare_frame_controller.protocol_list
                                            if f not in considered_frames and f.name == sorted_frame_name)
                j = self.compare_frame_controller.protocol_list.index(frame_should_be_here)
                self.signal_tab_controller.swap_frames(j, i)

            considered_frames.append(self.compare_frame_controller.protocol_list[i])

        self.set_frame_numbers()

    @pyqtSlot()
    def show_decoding_dialog(self):
>>>>>>>-b1ae517
       signals = [sf.signal for sf in self.signal_tab_controller.signal_frames]
        decoding_controller = DecoderWidgetController(
            self.compare_frame_controller.decodings, signals,
            self.project_manager, parent=self)
        decoding_controller.finished.connect(self.update_decodings)
        decoding_controller.show()
        decoding_controller.decoder_update()

    @pyqtSlot()
    def update_decodings(self):
<        self.compare_frame_controller.load_decodings()
        self.compare_frame_controller.fill_decoding_combobox()
        self.compare_frame_controller.refresh_existing_encodings()

        self.generator_tab_controller.refresh_existing_encodings(self.compare_frame_controller.decodings)

    @pyqtSlot(int)
    def on_selected_tab_changed(self, index: int):
        if index == 0:
            self.undo_group.setActiveStack(self.signal_tab_controller.signal_undo_stack)
        elif index == 1:
            self.undo_group.setActiveStack(self.compare_frame_controller.protocol_undo_stack)
            self.compare_frame_controller.ui.tblViewProtocol.resize_columns()
            self.compare_frame_controller.ui.tblViewProtocol.resize_vertical_header()
        elif index == 2:
            self.undo_group.setActiveStack(self.generator_tab_controller.generator_undo_stack)

    @pyqtSlot()
    def on_show_record_dialog_action_triggered(self):
        pm = self.project_manager
        try:
            r = ReceiveDialogController(pm, parent=self)
        except OSError as e:
            logger.error(repr(e))
            return

>>>>>>>+HEAD
======
         self.compare_frame_controller.fill_decoding_combobox()

    @pyqtSlot()
    def on_selected_tab_changed(self):
        indx = self.ui.tabWidget.currentIndex()
        if indx == 0:
            self.undo_group.setActiveStack(self.signal_tab_controller.signal_undo_stack)
        elif indx == 1:
            self.undo_group.setActiveStack(self.compare_frame_controller.protocol_undo_stack)
            self.compare_frame_controller.ui.tblViewProtocol.resize_it()
        elif indx == 2:
            self.undo_group.setActiveStack(self.generator_tab_controller.generator_undo_stack)


    def close_all(self):
        self.filemodel.setRootPath(QDir.homePath())
        self.ui.fileTree.setRootIndex(self.file_proxy_model.mapFromSource(self.filemodel.index(QDir.homePath())))
        self.project_manager.saveProject()

        self.signal_tab_controller.close_all()
        self.compare_frame_controller.reset()
        self.generator_tab_controller.close_all()

        self.project_manager.project_path = ""
        self.project_manager.project_file = None
        self.signal_tab_controller.signal_undo_stack.clear()
        self.compare_frame_controller.protocol_undo_stack.clear()
        self.generator_tab_controller.generator_undo_stack.clear()

    @pyqtSlot()
    def show_record_dialog(self):
        pm = self.project_manager
        r = SendRecvDialogController(pm.frequency, pm.sample_rate,
                                     pm.bandwidth, pm.gain,
                                     pm.device, Mode.receive,
                                     parent=self)
>>>>>>>-b1ae517
       if r.has_empty_device_list:
            Errors.no_device()
            r.close()
            return

        r.recording_parameters.connect(pm.set_recording_parameters)
<        r.files_recorded.connect(self.on_signals_recorded)
        r.show()

    @pyqtSlot()
    def show_proto_sniff_dialog(self):
        pm = self.project_manager
        signal = None
        for proto in self.compare_frame_controller.protocol_list:
            signal = proto.signal
            if signal:
                break

        if signal:
            bit_len = signal.bit_len
            mod_type = signal.modulation_type
            tolerance = signal.tolerance
            noise = signal.noise_threshold
            center = signal.qad_center
        else:
            bit_len = 100
            mod_type = 1
            tolerance = 5
            noise = 0.001
            center = 0.02

        psd = ProtocolSniffDialogController(pm, noise, center, bit_len, tolerance, mod_type, parent=self)
        if psd.has_empty_device_list:
            Errors.no_device()
            psd.close()
        else:
            psd.protocol_accepted.connect(self.compare_frame_controller.add_sniffed_protocol_messages)
            psd.show()

    @pyqtSlot()
    def on_show_spectrum_dialog_action_triggered(self):
        pm = self.project_manager
        r = SpectrumDialogController(pm, parent=self)
>>>>>>>+HEAD
======
         r.files_recorded.connect(self.load_recorded_signals)
        r.show()

    @pyqtSlot()
    def show_spectrum_dialog(self):
        pm = self.project_manager
        r = SendRecvDialogController(pm.frequency, pm.sample_rate,
                                     pm.bandwidth, pm.gain, pm.device,
                                     Mode.spectrum, parent=self)
>>>>>>>-b1ae517
       if r.has_empty_device_list:
            Errors.no_device()
            r.close()
            return

        r.recording_parameters.connect(pm.set_recording_parameters)
        r.show()

    @pyqtSlot(list)
<    def on_signals_recorded(self, file_names: list):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        for filename in file_names:
>>>>>>>+HEAD
======
     def load_recorded_signals(self, filenames):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        for filename in filenames:
>>>>>>>-b1ae517
           self.add_signalfile(filename)
        QApplication.restoreOverrideCursor()

    @pyqtSlot()
<    def show_options_dialog_action_triggered(self):
        self.show_options_dialog_specific_tab(tab_index=0)

    @pyqtSlot()
    def on_new_project_action_triggered(self):
        pdc = ProjectDialogController(parent=self)
        pdc.finished.connect(self.on_project_dialog_finished)
        pdc.show()

    @pyqtSlot()
    def on_project_settings_action_triggered(self):
        self.show_project_settings()

    @pyqtSlot()
    def on_project_dialog_finished(self):
        if self.sender().committed:
            if self.sender().new_project:
                for f in self.signal_tab_controller.signal_frames:
                    self.close_signal_frame(f)

            self.project_manager.from_dialog(self.sender())

    @pyqtSlot()
    def on_open_file_action_triggered(self):
        self.show_open_dialog(directory=False)

    @pyqtSlot()
    def on_open_directory_action_triggered(self):
        self.show_open_dialog(directory=True)

    def show_open_dialog(self, directory=False):
        fip = FileIconProvider()
        self.dialog = QFileDialog(self)
        self.dialog.setIconProvider(fip)
        self.dialog.setDirectory(FileOperator.RECENT_PATH)
        self.dialog.setWindowTitle("Open Folder")
        if directory:
            self.dialog.setFileMode(QFileDialog.Directory)
        else:
            self.dialog.setFileMode(QFileDialog.ExistingFiles)
            self.dialog.setNameFilter(
                "All files (*);;Complex (*.complex);;Complex16 unsigned (*.complex16u);;Complex16 signed (*.complex16s);;Wave (*.wav);;Protocols (*.proto);;"
                "Fuzzprofiles (*.fuzz);;Tar Archives (*.tar *.tar.gz *.tar.bz2);;Zip Archives (*.zip)")

        self.dialog.setOptions(QFileDialog.DontResolveSymlinks)
        self.dialog.setViewMode(QFileDialog.Detail)

        if self.dialog.exec_():
            try:
                file_names = self.dialog.selectedFiles()
                folders = [folder for folder in file_names if os.path.isdir(folder)]

                if len(folders) > 0:
                    folder = folders[0]
                    for f in self.signal_tab_controller.signal_frames:
                        self.close_signal_frame(f)

                    self.project_manager.set_project_folder(folder)
                else:
                    file_names = FileOperator.uncompress_archives(file_names, QDir.tempPath())
                    self.add_files(file_names)
            except Exception as e:
                Errors.generic_error(self.tr("Failed to open"), str(e), traceback.format_exc())
                self.ui.progressBar.hide()
                QApplication.restoreOverrideCursor()

    @pyqtSlot()
    def on_close_all_action_triggered(self):
        self.close_all()

    @pyqtSlot(list)
    def on_files_dropped(self, files):
        """
        :type files: list of QtCore.QUrl
        """
        self.__add_urls_to_group(files, group_id=0)

    @pyqtSlot(list, int)
    def on_files_dropped_on_group(self, files, group_id: int):
        """
        :param group_id:
        :type files: list of QtCore.QUrl
        """
        self.__add_urls_to_group(files, group_id=group_id)

    def __add_urls_to_group(self, file_urls, group_id=0):
        local_files = [file_url.toLocalFile() for file_url in file_urls if file_url.isLocalFile()]
        if len(local_files) > 0:
            self.add_files(FileOperator.uncompress_archives(local_files, QDir.tempPath()), group_id=group_id)

    @pyqtSlot(list)
    def on_cfc_close_wanted(self, protocols: list):
        frames = [sframe for sframe, protocol in self.signal_protocol_dict.items() if protocol in protocols]
        if len(frames) != len(protocols):
            logger.error("failed to close {} protocols".format(len(protocols) - len(frames)))

        for frame in frames:
            self.close_signal_frame(frame)

    @pyqtSlot(dict)
>>>>>>>+HEAD
======
     def show_options_dialog(self):

        op = OptionsController(self.plugin_manager.installed_plugins, parent=self)
        op.values_changed.connect(self.on_options_changed)
        op.exec_()

>>>>>>>-b1ae517
   def on_options_changed(self, changed_options: dict):
        refresh_protocol_needed = False
        for key in changed_options.keys():
            if key == "rel_symbol_length":
                st = changed_options[key]
                constants.SETTINGS.setValue('rel_symbol_length', st)
                refresh_protocol_needed = True
            elif key == "show_pause_as_time":
                refresh_protocol_needed = True

        if refresh_protocol_needed:
            for sf in self.signal_tab_controller.signal_frames:
                sf.refresh_protocol()

<        self.compare_frame_controller.refresh_field_types_for_labels()
        self.compare_frame_controller.set_shown_protocols()
        self.generator_tab_controller.set_network_sdr_send_button_visibility()

        if "default_view" in changed_options.keys():
            self.apply_default_view()

    @pyqtSlot()
    def on_text_edit_project_description_text_changed(self):
        self.project_manager.description = self.ui.textEditProjectDescription.toPlainText()
>>>>>>>+HEAD
======
        self.apply_default_view()

    def refresh_main_menu(self):
        enable = len(self.signal_protocol_dict) > 0
        self.ui.actionSaveAllSignals.setEnabled(enable)
        self.ui.actionClose_all.setEnabled(enable)

    @pyqtSlot()
    def on_new_project_clicked(self):
        pdc = ProjectDialogController(parent=self)
        pdc.finished.connect(self.on_project_dialog_finished)
        pdc.show()

    @pyqtSlot()
    def on_project_dialog_finished(self):
        if self.sender().commited:
            for f in self.signal_tab_controller.signal_frames:
                self.close_signal_frame(f)
            self.project_manager.from_dialog(self.sender())

    def apply_default_view(self):
        view_index = constants.SETTINGS.value('default_view', type = int)
        self.compare_frame_controller.ui.cbProtoView.setCurrentIndex(view_index)
        self.generator_tab_controller.ui.cbViewType.setCurrentIndex(view_index)
>>>>>>> b1ae517... Inital Commit
