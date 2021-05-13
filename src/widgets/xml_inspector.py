# coding: utf-8
from __future__ import print_function

import os
import xml.etree.ElementTree as ET

from PySide2.QtCore import QSortFilterProxyModel, Qt, QRegExp
from PySide2.QtGui import QRegExpValidator, QStandardItemModel

from PySide2.QtWidgets import (
    QCheckBox,
    QComboBox,
    QErrorMessage,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QTableView,
    QVBoxLayout,
    QWidget
)

from NodeBox.src import nuke


def _bypass_filedialog(func):
    """developlement only function.

    bypass asking user for filedialog.
    """
    def inner_wrapper(*args, **kwargs):
        status = None
        if os.getenv('USER') == 'virgil':
            file = 'log/example_profiling_log.xml'
            file = 'log/example_profiling_simple.xml'
            status = XmlData.load_file(file)

        self = args[0]
        func(self)

        if status:
            self._show_table()

    return inner_wrapper


class XmlData:
    xml = ""

    # XXX: not sure about this
    @classmethod
    def load_file(cls, file):
        status = None
        try:
            cls.xml = ET.parse(file).getroot()
        except ET.ParseError:
            # TODO: xml file might have some unclosed tags
            # usually Frame and PerformanceProfile. Should try to fix it automatically
            status = 'XML file might have syntax errors!'
        else:
            if cls.xml.tag != 'PerformanceProfile':
                status = 'Not a valid PerformanceProfile file.'

        if status:
            q = QErrorMessage()
            q.showMessage(status)
            q.exec_()
            return False

        return True

    @property
    def root(self):
        return self.xml

    def num_threads(self):
        return self.root.findtext('NumThreads')

    def script_name(self):
        return self.root.findtext('ScriptName')

    def time_stored(self):
        return self.root.findtext('TimeStored')

    def machine_info(self):
        return self.root.findtext('MachineInfo/OS')

    def frames_element(self):
        return self.root.findall('Frame')

    def frame_count(self):
        return len(self.frames_element())

    def nodes_elements(self):
        first_frame = self.root.find('Frame')
        return first_frame.findall('Node')

    def node_count(self):
        return len(self.nodes_elements())

    def nodes_name(self):
        return [n.findtext('Name') for n in self.nodes_elements()]

    def node_class(self, node_name):
        for node in self.nodes_elements():
            if node.findtext('Name') == node_name:
                return node.findtext('Class')


class InfoBox(QGroupBox):
    def __init__(self, title='Info'):
        QGroupBox.__init__(self, title)
        self.setMaximumWidth(300)

        _layout = QFormLayout()
        xml = XmlData()

        _layout.addRow(QLabel('TotalFrames:'), QLabel(str(xml.frame_count())))

        _layout.addRow(QLabel('NumThreads:'), QLabel(xml.num_threads()))

        _layout.addRow(QLabel('ScriptName:'), QLabel(xml.script_name()))

        _layout.addRow(QLabel('TimeStored:'), QLabel(xml.time_stored()))

        _layout.addRow(QLabel('Machine Info:'), QLabel(xml.machine_info()))

        self.setLayout(_layout)


class FramesBox(QGroupBox):
    def __init__(self, title='Frames'):
        QGroupBox.__init__(self, title)
        self.setMaximumWidth(300)

        # fixed range
        self._frame_box = QSpinBox()
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
        self._custom_line.setReadOnly(True)

        # TODO: Should limit numbers to maximum frames of file
        self._custom_line.setValidator(
            QRegExpValidator(QRegExp('[1-9]*[0-9]*-[1-9][0-9]*'))
        )

        _layout = QFormLayout()
        _layout.addRow(QLabel('Range:'), self._frame_box)
        _layout.addRow(self._enable_custom, self._custom_line)
        _layout.addRow(QLabel('Max Call:'), QLabel('sample'))
        _layout.addRow(QLabel('Max CPU:'), QLabel('sample'))
        _layout.addRow(QLabel('Max Wall:'), QLabel('sample'))

        self.setLayout(_layout)

    def _set_custom_range(self, value):
        self._custom_line.setReadOnly(not value)
        self._frame_box.setReadOnly(value)

    @property
    def value(self):
        return self._frame_box

    @property
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


class UpperLayout(QHBoxLayout):
    def __init__(self):
        QHBoxLayout.__init__(self)

        self._frame_widget = FramesBox()
        self.addWidget(self._frame_widget)
        self.addWidget(InfoBox())
        self.addSpacing(500)

    def frame_section(self):
        return self._frame_widget


class MiddleSection(QHBoxLayout):
    def __init__(self):
        QHBoxLayout.__init__(self)

        self.addWidget(QLabel('Filter nodes'))
        self._filter_nodes = QLineEdit()
        self.addWidget(self._filter_nodes)

        self._filter_items = QComboBox()
        self._filter_items.addItems(
            ['callCount', 'timeTakenWall', 'timeTakenCPU'])

        self.addWidget(QLabel('Filter by:'))
        self.addWidget(self._filter_items)

        # self.addWidget(QLabel('Profile type:'))
        # self.addWidget(QComboBox())

    def filter_type(self):
        return self._filter_items

    def filter_node(self):
        return self._filter_nodes


class XmlTableModel(QStandardItemModel):
    def __init__(self, rows=2, columns=2):
        QStandardItemModel.__init__(self, rows, columns)
        self._xml_data = XmlData()

        self._filter_type = 'callCount'

        self.setColumnCount(self._xml_data.frame_count())
        self.setRowCount(self._xml_data.node_count())
        self.setVerticalHeaderLabels(self._xml_data.nodes_name())

    def data(self, index, role):
        frames = self._xml_data.frames_element()

        if role == Qt.DisplayRole:
            nodes = frames[index.column()].findall('Node')
            timings = nodes[index.row()].find(
                'ProfileEngine/%s' % self.filter_type).text
            return int(timings)

    @ property
    def filter_type(self):
        return self._filter_type

    @ filter_type.setter
    def filter_type(self, value):
        self._filter_type = value


class XmlTableView(QTableView):
    def __init__(self):
        QTableView.__init__(self)
        self.setSortingEnabled(True)
        self._table_model = XmlTableModel()

        self._filter_proxy = QSortFilterProxyModel()
        self._filter_proxy.setSourceModel(self._table_model)

        self.setModel(self._filter_proxy)


class XmlInspectorController(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setHidden(True)

        self._layout = QVBoxLayout()

        _upper_layout = UpperLayout()

        self._frame_section = _upper_layout.frame_section()
        self._frame_box = self._frame_section
        self._frame_box.value.valueChanged.connect(self.column_range)
        self._frame_box.custom_range.textChanged.connect(self.column_range)

        self._table = XmlTableView()
        self._model = self._table._table_model

        _middle_layout = MiddleSection()

        _middle_layout.filter_type().currentTextChanged.connect(
            self.update_filter_type
        )

        _middle_layout.filter_node().textChanged.connect(
            self.filter_nodes
        )

        self._layout.addLayout(_upper_layout)
        self._layout.addLayout(_middle_layout)
        self._layout.addWidget(self._table)

        self.setLayout(self._layout)

        self.column_range()

    def filter_nodes(self, text):
        for i in range(self._model.rowCount()):

            header_label = self._model.verticalHeaderItem(i).text()
            node_class = XmlData().node_class(header_label)

            if header_label.startswith(text) or node_class.startswith(text):
                self._table.setRowHidden(i, False)
            else:
                self._table.setRowHidden(i, True)

    def update_filter_type(self, value):
        self._model.filter_type = value
        self._table.reset()

    def column_range(self):
        for i in range(self._model.columnCount()):
            if i in self._frame_box.frame_range():
                self._table.setColumnHidden(i, False)
            else:
                self._table.setColumnHidden(i, True)


class XmlInspector(QWidget):
    @ _bypass_filedialog
    def __init__(self):
        QWidget.__init__(self)
        self.setObjectName('XML Inspector')

        self._layout = QVBoxLayout()

        self._load_xml = QPushButton('Load XML file')
        self._load_xml.clicked.connect(self._open_file)
        self._layout.addWidget(self._load_xml)

        self.setLayout(self._layout)

    def _open_file(self):
        file, _ = QFileDialog.getOpenFileName(filter="*.xml")

        if not file:
            return

        status = XmlData.load_file(file)
        if status:
            self._show_table()

    def _show_table(self):
        _table = XmlInspectorController()

        self._layout.addWidget(_table)
        self._layout.addWidget(self._load_xml)

        _table.setHidden(False)
