import sys

from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
)

import table_model


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle('Nuke Nodes')

        table_widget = table_model.MainWindow()

        self.setCentralWidget(table_widget)


app = QApplication(sys.argv)

window = MainWindow()
window.show()


app.exec_()
