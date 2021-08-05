# coding: utf-8
from __future__ import print_function

import logging
from PySide2.QtCore import Qt
from PySide2.QtGui import QDesktopServices

from PySide2.QtWidgets import (
    QFormLayout,
    QLabel,
    QPushButton,
    QWidget
)

from ProfileInspector.src.about import about, about_links

LOGGER = logging.getLogger('ProfileInspector.help_tab')


class HelpWidget(QWidget):
    def __init__(self,):
        QWidget.__init__(self)

        self._layout = QFormLayout()
        self._layout.setFormAlignment(Qt.AlignHCenter | Qt.AlignTop)

        for key, value in about():
            self._layout.addRow(QLabel(key), QLabel(value))

        # TODO: would be nicer if button were left right instead of only
        for key, value in about_links():
            btn = self._create_btn(key, value)
            self._layout.addRow(QLabel(''), btn)

        self.setLayout(self._layout)

    @staticmethod
    def _create_btn(key, value):
        btn = QPushButton('Open ' + key)
        btn.clicked.connect(lambda: QDesktopServices.openUrl(value))
        return btn
