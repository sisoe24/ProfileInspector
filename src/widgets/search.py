# coding: utf-8
from __future__ import print_function

import logging

from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt


from PySide2.QtWidgets import (
    QAction,
    QPushButton,
    QToolButton,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QGroupBox
)

from NodeBox.src import nuke, util, resources
from NodeBox.src.widgets import ButtonSection

LOGGER = logging.getLogger('NodeBox.search')


class SearchNode(QLineEdit):
    def __init__(self):
        QLineEdit.__init__(self)
        # XXX: add completition/suggestion?
        self.setPlaceholderText('Find')
        self.setClearButtonEnabled(True)

        self.search_icon = QAction('Search', self)
        self.search_icon.setIcon(QIcon(":/icons/search"))

        # self.regex_action = QAction('Use Regex/Wildcard', self)
        # # self.regex_action.setIcon(QIcon(':/icons/regex-on'))
        # self.regex_action.setCheckable(True)
        # self.regex_action.setChecked(True)
        # self.regex_action.setEnabled(False)

        self.case_sensitive_action = QAction('Use case sensitivty', self)
        self.case_sensitive_action.setIcon(QIcon(":/icons/case-sensitive-off"))
        self.case_sensitive_action.setCheckable(True)
        self.case_sensitive_action.setChecked(False)

        self.whole_word_action = QAction('Match whole word', self)
        self.whole_word_action.setIcon(QIcon(":/icons/whole-word-off"))
        self.whole_word_action.setCheckable(True)
        self.whole_word_action.setChecked(False)

        self.addAction(self.search_icon, QLineEdit.LeadingPosition)
        # self.addAction(self.regex_action, QLineEdit.TrailingPosition)
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

    # def toggle_regex(self):
    #     return self.regex_action.triggered

    def toggle_case_sensitive(self):
        return self.case_sensitive_action

    def toggle_word_match(self):
        return self.whole_word_action

    def search_whole_word(self):
        return self.whole_word_action.isChecked()


class ReplaceNode(QWidget):
    # ! TODO: implement this section by itself or with the rename section
    def __init__(self):
        QWidget.__init__(self)
        util.widget_color(self, 'blue')

        self.setHidden(True)
        replace_icon = QAction('Search', self)
        replace_icon.setIcon(QIcon(":/icons/replace"))

        _layout = QHBoxLayout()
        _layout.setMargin(0)

        _layout.addSpacing(35)

        # _layout.addWidget(QLabel('Replace'))
        q = QLineEdit()
        q.setPlaceholderText('Replace')
        q.addAction(replace_icon, QLineEdit.LeadingPosition)
        _layout.addWidget(q)

        t1 = QToolButton()
        t1.setArrowType(Qt.LeftArrow)
        _layout.addWidget(t1)

        t2 = QToolButton()
        t2.setArrowType(Qt.RightArrow)
        _layout.addWidget(t2)

        _layout.addWidget(QPushButton('Replace'))
        _layout.addWidget(QPushButton('Replace All'))

        self.setLayout(_layout)


class SearchBarLayout(QHBoxLayout):
    def __init__(self):
        QHBoxLayout.__init__(self)

        self.setMargin(0)

        self.search_bar = SearchNode()

        self._show_replace = QToolButton()
        self._show_replace.setArrowType(Qt.RightArrow)
        self._show_replace.setCheckable(True)

        # XXX: should add search in all columns?
        self.search_type = QComboBox()
        self.search_type.addItems(['Name', 'Type'])
        self.addWidget(self._show_replace)
        self.addWidget(self.search_bar)
        self.addWidget(QLabel("Search by:"))
        self.addWidget(self.search_type)


class SearchBarWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        util.widget_color(self, 'red')

        _layout = QVBoxLayout()
        _layout.setMargin(0)

        search_bar_layout = SearchBarLayout()
        self._show_replace = search_bar_layout._show_replace
        self._show_replace.toggled.connect(self.show_replace_menu)

        self.replace_bar = ReplaceNode()

        self._search_bar = search_bar_layout.search_bar
        self._search_column = search_bar_layout.search_type

        _layout.addLayout(search_bar_layout)
        _layout.addWidget(self.replace_bar)

        self.setLayout(_layout)

    def show_replace_menu(self, state):
        if state:
            arrow = Qt.DownArrow
        else:
            arrow = Qt.RightArrow

        self.replace_bar.setHidden(not state)
        self._show_replace.setArrowType(arrow)

    def text(self):
        return self._search_bar.text()

    def clear(self):
        self._search_bar.clear()

    @property
    def search_by_column(self):
        return self._search_column.currentIndexChanged

    @property
    def return_pressed(self):
        return self._search_bar.returnPressed

    @property
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

    @property
    def whole_word(self):
        return self._search_bar.toggle_word_match()

    @property
    def case_sensitive(self):
        return self._search_bar.toggle_case_sensitive()

    # @property
    # def filter_type(self):
    #     return self._search_bar.toggle_regex()

    @property
    def rename(self):
        return self.btn_section.rename()
