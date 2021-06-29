# coding: utf-8
from __future__ import print_function

from PySide2.QtCore import QSysInfo, __version__

from PySide2.QtWidgets import (
    QFormLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QWidget
)

from ProfileInspector.src import __version__ as plugin_version
from ProfileInspector.src import nuke


class HelpForm(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        _layout = QFormLayout()

        _layout.addRow(QLabel('Profile Inspector:'), QLabel(plugin_version))

        _layout.addRow(QLabel('PySide2:'), QLabel(__version__))

        _layout.addRow(QLabel('Nuke:'), QLabel(nuke.NUKE_VERSION_STRING))

        self._machine_info = QLabel(QSysInfo().prettyProductName())
        _layout.addRow(QLabel('System:'), self._machine_info)
        _layout.addRow(QPushButton('Report Bug'), QPushButton('Readme'))
        _layout.addRow(QPushButton('Open Logs'), QPushButton('Changelog'))

        self.setLayout(_layout)


class HelpTab(QMainWindow):
    def __init__(self, *args, **kwargs):
        QMainWindow.__init__(self)

        self.setCentralWidget(HelpForm())
