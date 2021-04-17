from __future__ import print_function


from random import randint

from PySide2.QtCore import QSortFilterProxyModel, Qt, qRegisterResourceData
from PySide2.QtGui import QKeyEvent, QStandardItem, QStandardItemModel

from PySide2.QtWidgets import (
    QHBoxLayout, QLineEdit,
    QPushButton, QTableView, QVBoxLayout, QWidget
)


def nodes():
    nodes_list = ["Grade1", "Write1", "Grade3", "Roto1", "Grade2", "Shuffle1",
                  "CornerPin2D1", "Camera1", "Axis2", "Axis1", "ColorWheel1",
                  "Axis5", "Axis4", "Axis3", "Roto2", "Colorspace1", "Viewer2",
                  "Grade8", "Grade6", "Grade4", "Viewer1"
                  ]
    return nodes_list


class NodesModel(QStandardItemModel):
    def __init__(self, rows=1, columns=3):
        QStandardItemModel.__init__(self, rows, columns)

        self.setHorizontalHeaderLabels(['Nodes', 'Size', 'Shortcut'])

        for index, node in enumerate(nodes()):

            size = QStandardItem(str(randint(1, 99)).zfill(2))
            names = QStandardItem(node + ' ' + size.text())
            shortcut = QStandardItem(names.text()[0] + names.text()[-1])

            self.setItem(index, 0, names)
            self.setItem(index, 1, size)
            self.setItem(index, 2, shortcut)

    def flags(self, index):
        if index.column() == 1:
            return Qt.ItemIsEnabled
        if index.column() == 2:
            return Qt.ItemIsEditable | Qt.ItemIsEnabled

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable


class TableView(QTableView):
    def __init__(self):
        QTableView.__init__(self)

        self.setSortingEnabled(True)
        self.nodes_model = NodesModel()

        self.filter_proxy = QSortFilterProxyModel()

        self.filter_proxy.setSourceModel(self.nodes_model)
        self.filter_proxy.setFilterKeyColumn(0)
        self.filter_proxy.setFilterCaseSensitivity(Qt.CaseInsensitive)

        self.setModel(self.filter_proxy)

        self.clicked.connect(self.get_item)
        self.activated.connect(lambda: print('activated'))
        self.entered.connect(lambda: print('entered'))

    def get_item(self, value):
        if value.column() == 0:
            item = self.filter_proxy.itemData(value)
            print('clicked:', item[0])


class ButtonSection(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.__layout = QHBoxLayout()

        self.btn_select = QPushButton("Select All")
        self.btn_select.clicked.connect(lambda: print('Press'))
        self.__layout.addWidget(self.btn_select)

        self.btn_disable = QPushButton("Disable Selected")
        self.btn_disable.clicked.connect(lambda: print('Press'))
        self.__layout.addWidget(self.btn_disable)

        self.setLayout(self.__layout)


class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.table = TableView()

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText('Search Node')
        self.search_bar.returnPressed.connect(self.return_pressed)
        self.search_bar.textChanged.connect(self.highlight_name)
        self.search_bar.textChanged.connect(
            self.table.filter_proxy.setFilterRegExp
        )

        self.btn_section = ButtonSection()

        self.__layout = QVBoxLayout()
        self.__layout.addWidget(self.search_bar)
        self.__layout.addWidget(self.btn_section)
        self.__layout.addWidget(self.table)

        self.setLayout(self.__layout)

    def return_pressed(self, ):
        self.table.setFocus()
        print('return pressed')

    def highlight_name(self, e):
        print('Search bar text: ', e)
        # XXX: future version should use Qt.MatchRegularExpression instead
        match = self.table.nodes_model.findItems(e, Qt.MatchRegExp)


try:
    import nuke
    import nukescripts
except ImportError as e:
    print(e)
    pass
else:
    nukescripts.panels.registerWidgetAsPanel(
        'MainWindow', 'Select Node', 'uk.co.thefoundry.MainWindow')
