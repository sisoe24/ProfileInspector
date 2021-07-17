# coding: utf-8
from __future__ import print_function

import logging
from PySide2.QtCore import QSysInfo, __version__, QSettings

from PySide2.QtWidgets import (
    QCheckBox,
    QFormLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QWidget
)

from ProfileInspector.src import __version__ as plugin_version
from ProfileInspector.src import nuke

LOGGER = logging.getLogger('ProfileInspector.help_tab')


def get_log_handler(name):
    for handler in LOGGER.parent.handlers:
        if handler.name == name:
            return handler


class HelpForm(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        _layout = QFormLayout()

        _layout.addRow(QLabel('Profile Inspector:'), QLabel(plugin_version))
        _layout.addRow(QLabel('PySide2:'), QLabel(__version__))
        _layout.addRow(QLabel('Nuke:'), QLabel(nuke.NUKE_VERSION_STRING))

        self._machine_info = QLabel(QSysInfo().prettyProductName())
        _layout.addRow(QLabel('System:'), self._machine_info)

        self._enable_logging = QCheckBox()
        self._enable_logging.toggled.connect(self.enable_logger)
        _layout.addRow(QLabel('Show Console Logging'), self._enable_logging)

        _layout.addRow(QPushButton('Readme'), QPushButton('Changelog'))

        self.setLayout(_layout)

    def enable_logger(self, state):
        self._enable_logging.setChecked(state)
        console_handler = get_log_handler('Console')

        # XXX: not sure if outputing to Nukes internal script console
        # it might be too much text
        if state:
            # LOGGER.parent.propagate = True
            console_handler.setLevel(logging.DEBUG)
        else:
            # LOGGER.parent.propagate = False
            console_handler.setLevel(logging.WARNING)


class HelpTab(QMainWindow):
    def __init__(self, *args, **kwargs):
        QMainWindow.__init__(self)

        self.setCentralWidget(HelpForm())
