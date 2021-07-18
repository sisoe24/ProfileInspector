# coding: utf-8
from __future__ import print_function

import logging
from PySide2.QtCore import Qt
from PySide2.QtGui import QDesktopServices

from PySide2.QtWidgets import (
    QCheckBox,
    QFormLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QWidget
)

from ProfileInspector.src import __about__

LOGGER = logging.getLogger('ProfileInspector.help_tab')


def get_log_handler(name):
    for handler in LOGGER.parent.handlers:
        if handler.name == name:
            return handler


class HelpForm(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        _layout = QFormLayout()
        _layout.setFormAlignment(Qt.AlignHCenter | Qt.AlignTop)

        _layout.addRow(QLabel('Profile Inspector:'),
                       QLabel(__about__['ProfileInspector']))

        _layout.addRow(QLabel('PySide2:'), QLabel(__about__['PySide2']))
        _layout.addRow(QLabel('Nuke:'), QLabel(__about__['Nuke']))

        self._machine_info = QLabel(__about__['machine'])
        _layout.addRow(QLabel('System:'), self._machine_info)

        self._enable_logging = QCheckBox()
        self._enable_logging.toggled.connect(self.enable_logger)
        _layout.addRow(QLabel('Show Console Logging'), self._enable_logging)

        open_readme = QPushButton('Readme')
        open_readme.clicked.connect(lambda: self.open_link(open_readme.text()))

        open_changelog = QPushButton('Changelog')
        open_changelog.clicked.connect(
            lambda: self.open_link(open_changelog.text()))
        _layout.addRow(open_readme, open_changelog)

        open_issue = QPushButton('Report Issues')
        open_issue.clicked.connect(
            lambda: self.open_link(open_issue.text()))

        open_nukepedia = QPushButton('Nukepedia')
        open_nukepedia.clicked.connect(
            lambda: self.open_link(open_nukepedia.text()))

        _layout.addRow(open_issue, open_nukepedia)

        self.setLayout(_layout)

    def open_link(self, link):
        gitweb = 'https://github.com/sisoe24/ProfileInspector'

        links = {
            'Readme': gitweb + '/blob/main/README.md',
            'Changelog': gitweb + '/blob/main/CHANGELOG.md',
            'Report Issues':  gitweb + '/issues',
            'Nukepedia': ''
        }

        QDesktopServices.openUrl(links[link])

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
