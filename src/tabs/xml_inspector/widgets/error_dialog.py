# coding: utf-8
from __future__ import print_function
import traceback

from PySide2.QtWidgets import QMessageBox

# XXX: add buttons report, copy text ecc?


class ErrorDialog(QMessageBox):
    def __init__(self, parent, msg):
        QMessageBox.__init__(self, parent)
        self.setWindowTitle('Profile Inspector')
        self.setIcon(QMessageBox.Warning)

        self.setStandardButtons(QMessageBox.Help | QMessageBox.Ok)

        self.setText('Profile Inspector error...')
        self.setInformativeText(msg)
        self.setDetailedText(traceback.format_exc())
