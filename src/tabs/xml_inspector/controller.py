import re
import logging

from .report_parser import XmlData

LOGGER = logging.getLogger('ProfileInspector.xml_read_controller')


class FileInspectorController:
    def __init__(self, view):
        xml_reader = view

        _upper_layout = xml_reader.top_layout
        self.search_bar = xml_reader.search_bar
        self._table = xml_reader.table
        self._model = self._table._table_model
        self._table_filter = self._table.filter_model()

        self._frame_section = _upper_layout.frame_section()
        self._frame_box = self._frame_section
        self._frame_box.value.valueChanged.connect(self.column_range)

        self._frame_box.value.valueChanged.connect(
            self._frame_box.update_max_labels
        )

        self._frame_box.custom_range.textChanged.connect(self.column_range)
        self._frame_box.custom_range.textChanged.connect(
            self._frame_box.update_max_labels
        )

        self._timings_section = _upper_layout.timings_section()
        self._timings_section.call_type.currentTextChanged.connect(
            self.update_filter_type
        )

        self._timings_section.profiling_type.currentTextChanged.connect(
            self.update_profile_type
        )

        self._timings_section.timings_format.currentTextChanged.connect(
            self.update_time_format
        )

        self.case_insensitive = True

        self.search_bar.filter_node().textChanged.connect(self.filter_nodes)

        self.filter_column = 'Name'
        self.search_bar.search_by_column.connect(self._set_filter_column)

        self.search_bar.case_sensitive.toggled.connect(self._set_filter_case)

        self.column_range()

    def _set_filter_column(self, value):
        key_column = {0: 'Name', 1: 'Type', 2: 'Mix'}

        set_filter = key_column[value]

        self.filter_column = set_filter
        self._model.update_row_viewer(set_filter)

        self.filter_nodes(self.search_bar.text())

    def _set_filter_case(self, state):
        LOGGER.debug('Set case sensitivity to: %s', state)
        self.search_bar.update_case_icon()
        self.case_insensitive = not state
        self.filter_nodes(self.search_bar.text())

    def filter_nodes(self, text):
        for i in range(self._model.rowCount()):

            header_label = self._model.verticalHeaderItem(i).text()

            if self.case_insensitive:
                text = r'(?i)' + text

            # FIXME: when using invalid regex will complain regex error but still work
            if self.filter_column in ('Name', 'Type'):
                if re.match(text, header_label):
                    self._table.setRowHidden(i, False)
                else:
                    self._table.setRowHidden(i, True)

            elif self.filter_column == 'Mix':
                node_class = XmlData().node_class(header_label)
                if re.match(text, header_label) or re.match(text, node_class):
                    self._table.setRowHidden(i, False)
                else:
                    self._table.setRowHidden(i, True)

    def _filter_nodes(self, text):
        for header_index in range(self._model.rowCount()):
            if self.filter_column == 'Name':

                header_label = self._model.verticalHeaderItem(
                    header_index).text()

                if self.case_insensitive:
                    header_label = header_label.lower()

                if header_label.startswith(text):
                    self._table.setRowHidden(header_index, False)
                else:
                    self._table.setRowHidden(header_index, True)

            if self.filter_column == 'Type':
                node_class = XmlData().node_class(header_label)

                if self.case_insensitive:
                    node_class = node_class.lower()

                if node_class.startswith(text):
                    self._table.setRowHidden(header_index, False)
                else:
                    self._table.setRowHidden(header_index, True)

    def update_time_format(self, value):
        self._model.time_format = value
        self._table.reset()

    def update_profile_type(self, value):
        self._frame_section._profiling_type = value
        self._frame_section.update_max_labels()

        self._model.profile_type = value
        self._table.reset()

    def update_filter_type(self, value):
        self._model.timings_type = value
        self._table.reset()

    def column_range(self):
        for i in range(self._model.columnCount()):
            if i in self._frame_box.frame_range():

                self._table.setColumnHidden(i, False)
            else:
                self._table.setColumnHidden(i, True)
