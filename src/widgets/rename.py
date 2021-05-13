# coding: utf-8
from __future__ import print_function

import re
from pprint import pprint
from collections import OrderedDict

# XXX: getargspec is deprecated but it works for python2
from inspect import getargspec, getmembers, isfunction

from PySide2.QtCore import Qt

from PySide2.QtWidgets import (
    QDialog,
    QFormLayout,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QDialogButtonBox
)

from NodeBox.src.custom import user_variables
from NodeBox.src.custom.user_variables import USER_VARIABLES
from NodeBox.src import nuke


class UserFunctions:
    def __init__(self, function=""):
        self._function = function
        self._symbol = ""
        self._description = ""
        self._user_variables = {}

    def _extract_data(self):
        for func_name, func in getmembers(user_variables):
            if func_name.startswith('_nb'):
                yield func

    @property
    def symbol(self):
        self.set_symbol()
        return self._symbol

    @property
    def description(self):
        self.set_description()
        return self._description

    def set_description(self):
        description = re.search(
            r'(?<=:description:\s).+', self._function.func_doc)
        if description:
            self._description = description.group()
        else:
            self._description = ""

    def set_symbol(self):
        match = re.search(r'(?<=:symbol:\s).+', self._function.func_doc)

        if not match:
            return

        self._symbol = match.group()

    def __iter__(self):
        for function in self._extract_data():
            yield (UserFunctions(function))


def parse_user_variables():
    for function in UserFunctions():
        print(function.symbol)
        print(function.description)


def _parse_user_variables():
    _user_variables = {}

    for func_name, func in getmembers(user_variables):
        if func_name.startswith('_nb'):

            symbol = re.search(r'(?<=:symbol:\s).+', func.func_doc)
            if not symbol:
                print('function: %s has no symbol!' % func_name)
                continue

            description = re.search(r'(?<=:description:\s).+', func.func_doc)
            if description:
                description = description.group()
            else:
                description = ""

            _user_variables[symbol.group()] = {
                'description': description,
                'exec': func
            }

    pprint(_user_variables)


class PlaceholderTable(QTableWidget):
    def __init__(self, columns=3, rows=2):
        QTableWidget.__init__(self, rows, columns)
        self.setHidden(True)
        self.sortByColumn(0)

        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setHorizontalHeaderLabels(
            ['Placeholder', 'Content', 'Description'])

        self._placeholders = {}

    def refresh_table(self):

        self.setRowCount(len(self._placeholders.keys()))

        ordered_dict = OrderedDict(sorted(self._placeholders.items()))

        for index, _dict in enumerate(ordered_dict.items()):
            placeholder = str(_dict[0])
            content = str(_dict[1])

            self.setItem(index, 0, QTableWidgetItem(placeholder))
            if callable(_dict[1]):
                content = ' '.join(content.split(' ')[:2]).replace('<', '', 1)
            self.setItem(index, 1, QTableWidgetItem(content))

    @property
    def placeholders(self):
        return self._placeholders

    @placeholders.setter
    def placeholders(self, placeholders_dict):
        self._placeholders = placeholders_dict


class NamesLayout(QFormLayout):
    def __init__(self, node_name):
        QFormLayout.__init__(self)
        self.setFormAlignment(Qt.AlignLeft)

        self.new_name = QLabel()

        self.addRow(QLabel('Current name:'),  QLabel(node_name))
        self.addRow(QLabel('New name:'), self.new_name)


class RenameDialogBox(QDialog):
    def __init__(self, node_name):
        QDialog.__init__(self)
        self.setWindowTitle('Rename Node')

        self.user_vars = OrderedDict(sorted(USER_VARIABLES.items()))
        # print("➡ self.user_vars :", self.user_vars)

        _layout = QVBoxLayout()

        self._node_name = node_name
        self.rename_layout = NamesLayout(node_name)

        self.line_edit = QLineEdit()
        self.line_edit.textChanged.connect(self.fill_name)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.Help
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        # XXX: not sure about showing the table with help
        buttons.helpRequested.connect(self.show_table)

        self._table = PlaceholderTable()
        _layout.addWidget(self._table)
        _layout.addLayout(self.rename_layout)
        _layout.addWidget(self.line_edit)
        _layout.addWidget(buttons)

        self.setLayout(_layout)

    def fill_name(self, text):
        self.rename_layout.new_name.setText(self._parse_and_replace(text))

    def show_table(self):
        self._parse_functions()
        self._smart_rename()
        self._table.placeholders = self.user_vars
        self._table.refresh_table()
        self._table.resizeColumnsToContents()
        self._table.setFixedSize(
            self._table.horizontalHeader().length() +
            self._table.verticalHeader().width() + 2,
            self._table.verticalHeader().length() +
            self._table.horizontalHeader().height() + 2
        )
        self._table.setHidden(False)

    def get_text(self):
        return self._parse_and_replace()

    def _smart_rename(self):
        self.user_vars['$_'] = self._node_name
        name_splitted = self._node_name.split('_')

        if len(name_splitted) <= 1:
            return

        for index, match in enumerate(name_splitted):
            self.user_vars['$%d' % index] = match

    def _parse_functions(self):
        for symbol, replace in self.user_vars.items():

            if callable(replace):

                defaults = getargspec(replace).defaults
                if defaults and defaults[0] != '*':
                    if nuke.toNode(self._node_name).Class() != defaults[0]:
                        print('DELETING')
                        del self.user_vars[symbol]

    def _parse_and_replace(self, text=''):
        # TODO: add regex substitution
        line = text if text else self.line_edit.text()

        if not line:
            return

        self._smart_rename()
        self._parse_functions()

        for symbol, replace in self.user_vars.items():
            # XXX: not sure about callable. could try:
            # import types.FunctionType; isinstance(f, types.FunctionType)
            # but then what happens if is not a function but a callable class?
            if callable(replace):

                if getargspec(replace).args or getargspec(replace).varargs:
                    replace = replace(nuke.toNode(self._node_name))
                else:
                    replace = replace()

            line = line.replace(symbol, replace)

        line = '_'.join(line.split(' '))
        line = re.sub(r'[^a-z_0-9\s]', '_', line, flags=re.I)
        line = re.sub(r'_{1,}', '_', line)

        return line


# if __name__ == '__main__':
#     user_variables()
