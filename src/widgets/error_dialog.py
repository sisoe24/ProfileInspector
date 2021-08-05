# coding: utf-8
from __future__ import print_function, with_statement

import logging
import traceback

from PySide2.QtGui import QClipboard, QDesktopServices
from PySide2.QtWidgets import QMessageBox


from src.about import about_to_string, get_about_key


LOGGER = logging.getLogger('ProfileInspector.error_dialog')


def prepare_report(about_str):
    """Prepare report when user wants to report bug to github and
    insert about information to log critical file.

    Args:
        about (str): package/machine information from package.src.about
    """
    for logger in LOGGER.parent.handlers:
        if logger.name == 'Critical':

            with open(logger.baseFilename, 'r+') as file:
                content = file.read()
                file.seek(0, 0)
                file.write(about_str + '\n' + content)

    report = about_to_string()
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
            clipboard.setText(prepare_report(self.traceback_msg))

            QDesktopServices.openUrl(get_about_key('Issues'))

        elif button.text() == 'Help':
            pass
