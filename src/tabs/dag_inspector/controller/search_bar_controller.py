# coding: utf-8
from __future__ import print_function

from PySide2.QtCore import Qt, QSettings

from ProfileInspector.src.util.nuke_util import zoom_node


class SearchBarController():
    # TODO: add shortcut for focusing line edit
    def __init__(self, main_window):
        self.settings = QSettings()

        self.main_window = main_window

        self.table_model = self.main_window.table_view.table_model
        self.table_filter = self.main_window.table_view.filter_model()

        self.search_bar = self.main_window.search_bar

        self.search_bar_filter = self.table_filter.setFilterRegExp

        self.search_bar.case_sensitive.toggled.connect(self._set_filter_case)

        self.search_bar.search_by_column.connect(self._set_filter_column)

        self.search_bar.return_pressed.connect(
            self.main_window.table_view.setFocus
        )

        self.search_bar.whole_word.toggled.connect(self._set_whole_word)
        self.search_bar.text_changed.connect(self._search_node)

        # HACK: reset the selection or it will zoom at every change
        self.search_bar.text_changed.connect(
            self.main_window.table_view.selection_model().reset
        )

        self.search_bar.text_changed.connect(self._zoom_by_search)

    def _set_filter_column(self, value):
        value = -1 if value == 2 else value
        self.table_filter.setFilterKeyColumn(value)

    def _set_whole_word(self):
        self.search_bar.update_word_icon()
        self._search_node(self.search_bar.text())

    def _search_node(self, text):

        if self.search_bar.search_whole_word():
            self.search_bar_filter(r'\b' + text)
        else:
            self.search_bar_filter(text)

    def _zoom_by_search(self, text):

        if self.settings.value('zoom_search') in (True, 'true'):
            matches = self.table_model.findItems(text, Qt.MatchContains, 0)
            for match in matches:
                # TODO: if no match then it should deselect last node
                column, row = match.column(), match.row()
                node = self.table_model.index(row, column).data()
                zoom_node(node)
                return

    def _set_filter_case(self, state):
        self.search_bar.update_case_icon()
        case = Qt.CaseInsensitive
        if state:
            case = Qt.CaseSensitive

        self.table_filter.setFilterCaseSensitivity(case)
