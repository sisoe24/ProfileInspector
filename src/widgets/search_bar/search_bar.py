# coding: utf-8
from __future__ import print_function

import logging

from textwrap import dedent

from PySide2.QtGui import QIcon
from PySide2.QtCore import QSettings, Qt


from PySide2.QtWidgets import (
    QAction,
    QToolButton,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
)

from ProfileInspector.src.util import widget_color, doc_file
from ..hover_popup import HoverHelper


from .search_bar_settings import SearchBarSettingsWidget

LOGGER = logging.getLogger('ProfileInspector.search')


class SearchNode(QLineEdit):
    def __init__(self):
        QLineEdit.__init__(self)
        # XXX: add completition/suggestion?

        self.setPlaceholderText('Find')
        self.setClearButtonEnabled(True)

        self.search_icon = QAction('Search', self)
        self.search_icon.setIcon(QIcon(":/icons/search"))

        self.case_sensitive_action = QAction('Match Case', self)
        self.case_sensitive_action.setIcon(QIcon(":/icons/case-sensitive-off"))
        self.case_sensitive_action.setCheckable(True)
        self.case_sensitive_action.setChecked(False)

        self.whole_word_action = QAction('Match Whole Word', self)
        self.whole_word_action.setIcon(QIcon(":/icons/whole-word-off"))
        self.whole_word_action.setCheckable(True)
        self.whole_word_action.setChecked(False)

        self.addAction(self.search_icon, QLineEdit.LeadingPosition)
        self.addAction(self.case_sensitive_action, QLineEdit.TrailingPosition)
        self.addAction(self.whole_word_action, QLineEdit.TrailingPosition)

    def update_icon(self, action, icon_name):
        if action.isChecked():
            action.setIcon(QIcon(":/icons/%s-on" % icon_name))
        else:
            action.setIcon(QIcon(":/icons/%s-off" % icon_name))

    def update_regex_icon(self):
        self.update_icon(self.regex_action, 'regex')

    def update_case_icon(self):
        self.update_icon(self.case_sensitive_action, 'case-sensitive')

    def update_word_icon(self):
        self.update_icon(self.whole_word_action, 'whole-word')

    def toggle_case_sensitive(self):
        return self.case_sensitive_action

    def toggle_word_match(self):
        return self.whole_word_action

    def search_whole_word(self):
        return self.whole_word_action.isChecked()


class SearchBarLayout(QHBoxLayout):
    def __init__(self):
        QHBoxLayout.__init__(self)

        # self.setMargin(0)

        self.search_bar = SearchNode()

        self.search_type = QComboBox()
        self.search_type.setToolTip(
            '''<nobr><b>Filter nodes by</b><br>
            Name: name of the node<br>
            Type: type (class) of the node<br>
            Mix: both name and type</nobr>''')

        self.search_type.addItems(['Name', 'Type', 'Mix'])
        self.search_type.setFixedWidth(100)

        self._show_advance_menu = QToolButton()
        self._show_advance_menu.setStatusTip('Show/Hide extra options')

        self._show_advance_menu.setArrowType(Qt.RightArrow)
        self._show_advance_menu.setCheckable(True)
        self.addWidget(self._show_advance_menu)

        self.addWidget(self.search_bar)
        self.addWidget(QLabel("Filter by:"))
        self.addWidget(self.search_type)


class SearchBarWidget(QWidget):
    @widget_color
    def __init__(self):
        QWidget.__init__(self)
        self.setWhatsThis('''
        <p>
        The search bar allows you to filter the nodes present in the Node Graph,
        with real time feedback of the result.<br>
        It also accepts regular expression patterns.
        </p>''')

        self._layout = QVBoxLayout()
        # self._layout.setMargin(0)

        search_bar_layout = SearchBarLayout()

        self._search_bar = search_bar_layout.search_bar
        self._search_column = search_bar_layout.search_type

        self._layout.addLayout(search_bar_layout)

        self._show_advance_menu = search_bar_layout._show_advance_menu
        self._show_advance_menu.toggled.connect(self.show_advance_menu)

        self.advance_settings = SearchBarSettingsWidget()
        self._layout.addWidget(self.advance_settings)

        self.setLayout(self._layout)

    def show_advance_menu(self, state):
        if state:
            arrow = Qt.DownArrow
        else:
            arrow = Qt.RightArrow

        self.advance_settings.setHidden(not state)
        self._show_advance_menu.setArrowType(arrow)

    def text(self):
        return self._search_bar.text()

    def clear(self):
        self._search_bar.clear()

    @ property
    def search_by_column(self):
        return self._search_column.currentIndexChanged

    @ property
    def return_pressed(self):
        return self._search_bar.returnPressed

    @ property
    def text_changed(self):
        return self._search_bar.textChanged

    def update_regex_icon(self):
        self._search_bar.update_regex_icon()

    def update_case_icon(self):
        self._search_bar.update_case_icon()

    def update_word_icon(self):
        self._search_bar.update_word_icon()

    def search_whole_word(self):
        return self._search_bar.search_whole_word()

    @ property
    def whole_word(self):
        return self._search_bar.toggle_word_match()

    @ property
    def case_sensitive(self):
        return self._search_bar.toggle_case_sensitive()

    @ property
    def rename(self):
        return self.btn_section.rename()
