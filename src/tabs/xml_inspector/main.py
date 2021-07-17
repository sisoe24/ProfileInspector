# coding: utf-8
from __future__ import print_function

import os
import logging


from PySide2.QtCore import QSortFilterProxyModel, Qt, QRegExp
from PySide2.QtGui import QIcon, QRegExpValidator, QStandardItemModel

from PySide2.QtWidgets import (
    QAction,
    QCheckBox,
    QComboBox,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QSizePolicy,
    QSpinBox,
    QStatusBar,
    QTableView,
    QVBoxLayout,
    QWidget,
    QFileDialog
)


from .util import _bypass_filedialog
from .controller import FileInspectorController
from .report_parser import XmlData

from ProfileInspector.src import nuke
from ProfileInspector.src.util import TimeFormatter, widget_color, doc_file
from ProfileInspector.src.widgets import (
    SearchBarWidget,
    ErrorDialog,
    TimingsGroup,
    DockableWindow,
    ToolBar,
)

LOGGER = logging.getLogger('ProfileInspector.file_inspector')


class InfoBox(QGroupBox):
    @widget_color
    def __init__(self, title='Info'):
        QGroupBox.__init__(self, title)
        self.setToolTip('XML header information')
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        _layout = QFormLayout()
        xml = XmlData()

        _layout.addRow(QLabel('TotalFrames:'), QLabel(str(xml.frame_count())))

        _layout.addRow(QLabel('NumThreads:'), QLabel(xml.num_threads()))

        script_path = xml.script_name()
        script_name = QLabel(os.path.basename(script_path))
        script_name.setToolTip(script_path)

        _layout.addRow(QLabel('ScriptName:'), script_name)

        _layout.addRow(QLabel('TimeStored:'), QLabel(xml.time_stored()))

        _layout.addRow(QLabel('Machine Info:'), QLabel(xml.machine_info()))

        self.setLayout(_layout)


class FramesBox(QGroupBox):
    """Frame widget."""
    @widget_color
    def __init__(self, title='Frames'):
        QGroupBox.__init__(self, title)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.setWhatsThis(doc_file('xml_frames'))

        # fixed range
        self._frame_box = QSpinBox()
        self._frame_box.setToolTip('Set fixed frame range for table view ')

        self._frame_box.lineEdit().setReadOnly(True)
        self._frame_box.setRange(1, 9999)

        self._frame_init_value = 11
        self._frame_box.setValue(self._frame_init_value)

        self._frame_step = 10
        self._frame_box.setSingleStep(self._frame_step)

        self._frame_box.setPrefix('1-')
        self._frame_box.valueChanged.connect(self._increment_prefix)

        # custom range

        self._enable_custom = QCheckBox('Custom Range:')
        self._enable_custom.toggled.connect(self._set_custom_range)

        self._custom_line = QLineEdit()
        self._custom_line.setToolTip(
            'Set custom frame range for table view: e.g. 1-23'
        )
        self._custom_line.setReadOnly(True)

        # TODO: Should limit numbers to maximum frames of file?
        self._custom_line.setValidator(
            QRegExpValidator(QRegExp('[1-9]*[0-9]*-[1-9][0-9]*'))
        )

        _layout = QFormLayout()
        _layout.addRow(QLabel('Range:'), self._frame_box)
        _layout.addRow(self._enable_custom, self._custom_line)

        self._xml_data = XmlData()

        self._max_call = QLabel('')
        self._max_cpu = QLabel('')
        self._max_wall = QLabel('')
        self._profiling_type = 'Engine'

        self.update_max_labels()

        _layout.addRow(QLabel('Max Call:'), self._max_call)
        _layout.addRow(QLabel('Max CPU:'), self._max_cpu)
        _layout.addRow(QLabel('Max Wall:'), self._max_wall)

        self.setLayout(_layout)

    def update_max_labels(self):
        self._max_call.setText(self.find_max('callCount'))
        self._max_cpu.setText(self.find_max('timeTakenCPU'))
        self._max_wall.setText(self.find_max('timeTakenWall'))

    def find_max(self, call_type):
        frames = self._xml_data.frames_element()
        frames_count = self._xml_data.frame_count()
        nodes = self._xml_data.nodes_name()

        max_time = {}
        for index, node_name in enumerate(nodes):
            max_time[node_name] = []
            for frame_range in self.frame_range():
                if frame_range >= frames_count:
                    continue

                nodes = frames[frame_range].findall('Node')

                match_timings = 'Profile%s/' % self._profiling_type + call_type

                # TODO: should be nice to also add the frame where is max
                # TODO: when more than has the same max will shown only 1
                time = nodes[index].find(match_timings).text
                max_time[node_name].append(int(time))

        has_data = [i for i in max_time.values() if i]
        if not has_data:
            return

        biggest = 0
        max_node = ""

        for k, v in max_time.items():
            if max(v) > biggest:
                biggest = max(v)
                max_node = k

        return max_node

    def _set_custom_range(self, value):
        # TODO: when enabling/disabling should update search
        self._custom_line.setReadOnly(not value)
        self._frame_box.setReadOnly(value)

    @ property
    def value(self):
        return self._frame_box

    @ property
    def custom_range(self):
        return self._custom_line

    def frame_range(self):
        # TODO: should split this function
        if self._enable_custom.isChecked():
            custom_value = self._custom_line.text().split('-')
            if len(custom_value) == 2 and custom_value[1]:
                start, end = custom_value
            else:
                start, end = 1, 1
        else:
            prefix = self._frame_box.prefix().split('-')[0]
            start, end = prefix, self._frame_box.value()
        return range(int(start) - 1, int(end))

    def _increment_prefix(self, value):
        if value < self._frame_init_value:
            self._frame_box.setValue(self._frame_init_value)
            return
        prefix = value - self._frame_step
        self._frame_box.setPrefix("%d-" % prefix)


class DisplayTimings(TimingsGroup):
    def __init__(self):
        TimingsGroup.__init__(self)
        self.setMaximumWidth(300)

        self._call_type = QComboBox()
        self._call_type.setToolTip('Change table call type display')
        self._call_type.addItems(
            ['callCount', 'timeTakenWall', 'timeTakenCPU'])

        self.form_layout.insertRow(1, QLabel('Call type:'), self._call_type)

    @ property
    def call_type(self):
        return self._call_type


class UpperLayout(QHBoxLayout):
    """Frames and info layout."""

    def __init__(self):
        QHBoxLayout.__init__(self)

        self._frame_widget = FramesBox()
        self.addWidget(self._frame_widget)

        self._timings = DisplayTimings()
        self.addWidget(self._timings)

        self.addWidget(InfoBox())

    def timings_section(self):
        return self._timings

    def frame_section(self):
        return self._frame_widget


class SearchSection(SearchBarWidget):
    def __init__(self):
        SearchBarWidget.__init__(self)
        self._show_advance_menu.setHidden(True)

    def filter_node(self):
        return self._search_bar


class XmlTableModel(QStandardItemModel):
    def __init__(self, rows=2, columns=2):
        QStandardItemModel.__init__(self, rows, columns)
        self._xml_data = XmlData()

        self._timings_type = 'callCount'
        self._profile_type = 'Engine'
        self._time_format = 'ms'

        self.setColumnCount(self._xml_data.frame_count())
        self.setRowCount(self._xml_data.node_count())
        self.setVerticalHeaderLabels(self._xml_data.nodes_name())

    def data(self, index, role):
        frames = self._xml_data.frames_element()

        if role == Qt.DisplayRole:
            nodes = frames[index.column()].findall('Node')
            match_timings = 'Profile%s/%s' % (self.profile_type,
                                              self.timings_type)
            time = nodes[index.row()].find(match_timings).text

            # return int(time)

            # TODO: when returning time object, table could not sort properly
            # because numbers are string
            return TimeFormatter(int(time), self.time_format).str()

        if role == Qt.ToolTipRole:
            node_name = self._xml_data._nodes[index.row()]
            return node_name

    @ property
    def time_format(self):
        return self._time_format

    @ time_format.setter
    def time_format(self, value):
        LOGGER.debug('setting time format to: %s', value)
        self._time_format = value

    @ property
    def profile_type(self):
        return self._profile_type

    @ profile_type.setter
    def profile_type(self, value):
        LOGGER.debug('setting profile type to: %s', value)
        self._profile_type = value

    @ property
    def timings_type(self):
        return self._timings_type

    @ timings_type.setter
    def timings_type(self, value):
        LOGGER.debug('setting timings type to: %s', value)
        self._timings_type = value

    def update_row_viewer(self, view):
        if view == 'Type':
            self.setVerticalHeaderLabels(self._xml_data.nodes_class())
        elif view in ('Name', 'Mix'):
            self.setVerticalHeaderLabels(self._xml_data.nodes_name())


class XmlTableView(QTableView):
    def __init__(self):
        QTableView.__init__(self)
        self.setSortingEnabled(True)

        self.setWhatsThis(doc_file('xml_table'))
        self._table_model = XmlTableModel()

        self._filter_proxy = QSortFilterProxyModel()
        self._filter_proxy.setSourceModel(self._table_model)

        self.setModel(self._filter_proxy)

    def filter_model(self):
        return self._filter_proxy


class FileInspectorLayout(QWidget):
    @widget_color
    def __init__(self):
        QWidget.__init__(self)
        self.setObjectName('file_inspector_layout')

        _layout = QVBoxLayout()

        self.top_layout = UpperLayout()
        self.search_bar = SearchSection()
        self.table = XmlTableView()

        _layout.addLayout(self.top_layout)
        _layout.addWidget(self.search_bar)
        _layout.addWidget(self.table)

        self.setLayout(_layout)

        self.file_inspector_controller = FileInspectorController(self)


class DockableWidget(DockableWindow):
    def __init__(self):
        DockableWindow.__init__(self, title='XML Inspector')

        self._delete_children = 'file_inspector_layout'


class FileInspectorToolBar(ToolBar):
    def __init__(self):
        ToolBar.__init__(self)

        self.load_xml = QAction(QIcon(':/icons/folder'), 'Open file...', self)
        self.load_xml.setStatusTip('Load XML report file to analyze')

        self.addAction(self.load_xml)
        self.addAction(self._help_button)


class FileInspectorWidget(QMainWindow):
    @_bypass_filedialog
    def __init__(self):
        QMainWindow.__init__(self)
        self.setObjectName('XML Inspector')

        toolbar = FileInspectorToolBar()
        toolbar.load_xml.triggered.connect(self._open_file)
        self.addToolBar(toolbar)

        self._dockable_widget = DockableWidget()
        self.addDockWidget(Qt.BottomDockWidgetArea, self._dockable_widget)

        self.setStatusBar(QStatusBar(self))

    def _open_file(self):
        file = nuke.getFilename('Open xml file', '*.xml')

        if not file:
            return

        LOGGER.debug('Parsing xml file: %s', file)

        try:
            XmlData.load_file(file, self)
        except ValueError as err:
            msg = 'XML data is invalid'

            err_dialog = ErrorDialog(self, msg)
            err_dialog.setDetailedText(str(err))
            err_dialog_btn = err_dialog.exec_()

            # TODO: dont like this
            if err_dialog_btn == QMessageBox.Help:
                help_msg = QMessageBox(self)
                help_msg.setIcon(QMessageBox.Information)
                help_msg.setInformativeText(
                    'If you are parsing a report just made from your currently running '
                    'Nuke application, you need to terminate the app in order '
                    'to let Nuke complete the report.'
                )
                help_msg.show()

            LOGGER.error('XML data is invalid%s', err)
            return

        self._show_inspector()

    def _show_inspector(self):

        _file_inspector = FileInspectorLayout()
        self._dockable_widget.setWidget(_file_inspector)
