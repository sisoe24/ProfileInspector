# coding: utf-8
from __future__ import print_function
import traceback

from PySide2.QtWidgets import (
    QDialog,
    QLabel,
    QMessageBox,
    QVBoxLayout,
    QDialogButtonBox
)


class _ErrorDialog(QDialog):
    # TODO: this should be inline with the ErrorMessage Dialog Box
    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle('Profile Inspector - Xml Error')

        self._layout = QVBoxLayout()

        self._err_msg = QLabel('')
        self._help_msg = QLabel('')

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Help)
        buttons.accepted.connect(self.accept)

        buttons.helpRequested.connect(self.help_msg)

        self._layout.addWidget(buttons)

        self.setLayout(self._layout)

    def err_msg(self, msg):

        self._err_msg.setText(msg)
        self._layout.insertWidget(0, self._err_msg)

    def help_msg(self):
        msg = '''If you are parsing a report just made from your running Nuke application,
        you need to terminate the app in order to let Nuke complete the report.
        '''
        self._layout.insertWidget(0, self._help_msg)
        self._help_msg.setText(msg)


class ErrorDialog(QMessageBox):
    def __init__(self, parent, msg):
        # TODO: add buttons (report, copy text ecc)
        QMessageBox.__init__(self, parent)
        self.setWindowTitle('Profile Inspector')
        self.setIcon(QMessageBox.Warning)
        
        self.setStandardButtons(QMessageBox.Help | QMessageBox.Ok)

        self.setText('Profile Inspector error...')
        self.setInformativeText(msg)
        self.setDetailedText(traceback.format_exc())
