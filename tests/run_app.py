"""Not properly a test but it works for now."""
# coding: utf-8
from __future__ import print_function

import sys

from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
)


from src.main import MainWindow


# personal screen where I test the app view
screen_loc = {
    'hp': {
        'x': -1077.296875,
        'y': -5.31640625
    }
}


class TestMainWindow(QMainWindow):
    """Test Class for generating a main window in standalone."""

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle('Profile Inspector')

        self.setGeometry(screen_loc['hp']['x'],
                         screen_loc['hp']['y'],
                         1080, 1980)

        app = MainWindow()
        self.setCentralWidget(app)

        # Start app in specific page
        # 0 Dag Page
        # 1 Xml Inspector
        # 2 Nuke Launcher
        # 3 About
        app.main_window._tabs.setCurrentIndex(1)


APP = QApplication(sys.argv)
try:
    WINDOW = TestMainWindow()
    WINDOW.show()
except Exception as err:
    print('run app error ::', err)
else:
    APP.exec_()
