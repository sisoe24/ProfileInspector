# coding: utf-8
from __future__ import print_function
import os
import sys


from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
)

import ProfileInspector

sys.dont_write_bytecode = True

os.environ['_TEST_ENV'] = '1'

screen_loc = {
    'hp': {
        'x': -1077.296875,
        'y': -5.31640625
    }
}


class MainWindow(QMainWindow):
    """Test Class for generating a main window in standalone."""

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle('Profile Inspector')

        self.setGeometry(screen_loc['hp']['x'],
                         screen_loc['hp']['y'],
                         1080, 1980)

        self.setCentralWidget(ProfileInspector.src.main.MainWindow())


APP = QApplication(sys.argv)
try:
    WINDOW = MainWindow()
    WINDOW.show()
except Exception as err:
    print('run app error ::', err)
else:
    APP.exec_()
