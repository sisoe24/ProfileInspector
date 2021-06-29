# coding: utf-8
from __future__ import print_function

import logging

from PySide2.QtCore import Qt, Signal
from PySide2.QtWidgets import QDockWidget

LOGGER = logging.getLogger('ProfileInspector.dockable_widget')


class DockableWindow(QDockWidget):

    close_event = Signal()

    def __init__(self, title):
        QDockWidget.__init__(self, title)
        self._delete_children = None

    def delete_children(self):
        for children in self.children():
            if children.objectName() == self._delete_children:
                children.deleteLater()

    def closeEvent(self, event):
        self.delete_children()

        if self.isFloating():
            self.setFloating(False)

        LOGGER.debug('Re docking widget')
        event.ignore()

        # self.close_event.emit()

    def changeEvent(self, event):
        """ if window is undocked add min max buttons window """
        if event.type().name == 'ActivationChange' and self.isFloating():
            self.setWindowFlag(Qt.WindowMinMaxButtonsHint)
            self.show()
