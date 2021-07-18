# coding: utf-8
from __future__ import print_function, with_statement

import logging
import traceback

from PySide2.QtGui import QClipboard, QDesktopServices
from PySide2.QtWidgets import QMessageBox


from ProfileInspector.src import __about__

LOGGER = logging.getLogger('ProfileInspector.error_dialog')


def append_machine_info(machine):

    for i in LOGGER.parent.handlers:
        if i.name == 'Critical':

            with open(i.baseFilename, 'r+') as f:
                content = f.read()
                f.seek(0, 0)
                f.write(machine + '\n' + content)


def machine_info_string():
    machine = ''
    for k, v in __about__.items():
        machine += '%s: %s\n' % (k, v)
    append_machine_info(machine)
    return machine


def generate_report(trace):
    report = machine_info_string() + trace
    return report


class ErrorDialog(QMessageBox):
    def __init__(self, parent, msg):
        QMessageBox.__init__(self, parent)
        self.setWindowTitle('Profile Inspector')
        self.setIcon(QMessageBox.Warning)

        self.setStandardButtons(QMessageBox.Help | QMessageBox.Ok)

        self.addButton('Report bug', QMessageBox.ActionRole)

        self.buttonClicked.connect(self.click_event)

        self.setText('Profile Inspector error...')
        self.setInformativeText(msg)

        self.traceback_msg = traceback.format_exc()
        self.setDetailedText(self.traceback_msg)

    def click_event(self, button):
        if button.text() == 'Report bug':
            q = QMessageBox()
            q.setIcon(QMessageBox.Information)
            q.setText('Report Bug')
            q.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
            q.setInformativeText('Report bug via github')
            q.setDetailedText(
                'The machine info and traceback will be copied into your clipboard when you press Ok. '
                'Alternatively it can be found inside the ProfileInspector/log/errors.log')
            q.exec_()

            clipboard = QClipboard()
            clipboard.setText(generate_report(self.traceback_msg))

            QDesktopServices.openUrl(
                'https://github.com/sisoe24/ProfileInspector/issues/new?assignees=sisoe24&labels=&template=bug_report.md&title= ')

        elif button.text() == 'Help':
            pass
