# coding: utf-8
import sys
import logging


from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
)

from NodeBox.src import main

LOGGER = logging.getLogger("NodeBox.app")


class MainWindow(QMainWindow):
    """Test Class for generating a main window for testing."""

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle('NodeBox')

        right_x, right_y = 3443.16015625, 25.3671875
        left_x, left_y = -1118.921875, 26.1171875

        self.setGeometry(right_x, right_y, 300, 300)
        # self.setGeometry(left_x, left_y, 300, 300)

        table_widget = main.MainWindow()

        self.setCentralWidget(table_widget)


APP = QApplication(sys.argv)

try:
    WINDOW = MainWindow()
except Exception as error:
    import traceback
    LOGGER.error('app.py error: %s - %s', error, traceback.format_exc())
else:
    WINDOW.show()
    APP.exec_()
