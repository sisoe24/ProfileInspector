# coding: utf-8
from __future__ import print_function

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QToolBar


class ToolBar(QToolBar):
    def __init__(self):
        QToolBar.__init__(self)

        self.setStyleSheet('''
            color: white;
        ''')

        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.setMovable(False)
