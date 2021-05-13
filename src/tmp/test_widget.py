# coding: utf-8
from __future__ import print_function
from PySide2.QtCore import QLine
from PySide2.QtGui import QIcon

from PySide2.QtWidgets import (
    QAction,
    QLineEdit,
    QToolBar,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QCheckBox,
    QDockWidget
)


class DockWidget(QDockWidget):
    def __init__(self):
        QDockWidget.__init__(self)

        _layout = QVBoxLayout()

        _button = QPushButton('Click me')
        _layout.addWidget(_button)

        self.setLayout(_layout)


class LineEdit(QLineEdit):

    def __init__(self, ):
        QLineEdit.__init__(self)
        icon_path = 'other/vscode-icons-main/icons'
        icon = 'regex.svg'

        self.dark = QIcon(icon_path + '/dark/' + icon)
        self.light = QIcon(icon_path + '/light/' + icon)

        icon = QIcon(self.dark)

        self.action = QAction('Use Regex/Wildcard', self)
        self.action.setIcon(icon)
        self.action.setCheckable(True)

        self.addAction(self.action, QLineEdit.TrailingPosition)

        self.action.triggered.connect(self.toggle_regex)

    def toggle_regex(self, state):
        if state is True:
            self.action.setIcon(self.dark)
        else:
            self.action.setIcon(self.light)


class TestWidget(QWidget):
    """DUMMY code for testing stuff."""

    def __init__(self, ):
        QWidget.__init__(self)

        layout = QVBoxLayout()
        l = LineEdit()

        layout.addWidget(l)
        self.setLayout(layout)
