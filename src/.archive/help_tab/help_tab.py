# coding: utf-8
from __future__ import print_function

import logging

from PySide2.QtWidgets import (
    QCheckBox,
    QLabel,
    QMainWindow,
)

from ProfileInspector.src.widgets import AboutWidget

LOGGER = logging.getLogger('ProfileInspector.help_tab')


def get_log_handler(name):
    for handler in LOGGER.parent.handlers:
        if handler.name == name:
            return handler


class _AboutWidget(AboutWidget):
    def __init__(self,):
        AboutWidget.__init__(self)
        # XXX: dont think I am going to include the show logger

        self._enable_logging = QCheckBox()
        self._enable_logging.toggled.connect(self.enable_logger)
        self._layout.addRow(QLabel('Show Console Logging'),
                            self._enable_logging)

    def enable_logger(self, state):
        # self._enable_logging.setChecked(state)
        console_handler = get_log_handler('Console')

        # XXX: not sure if outputing to Nukes internal script console
        # it might be too much text
        if state:
            LOGGER.parent.propagate = True
            console_handler.setLevel(logging.DEBUG)
        else:
            LOGGER.parent.propagate = False
            console_handler.setLevel(logging.WARNING)


class HelpTab(QMainWindow):
    def __init__(self, *args, **kwargs):
        QMainWindow.__init__(self)

        self.setCentralWidget(_AboutWidget())
