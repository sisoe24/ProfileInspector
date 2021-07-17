# coding: utf-8
from __future__ import print_function

import logging

from PySide2.QtGui import QIcon, QStandardItem, QStandardItemModel
from PySide2.QtCore import Qt, QSettings, QSortFilterProxyModel

from PySide2.QtWidgets import (
    QAction,
    QMainWindow,
    QPushButton,
    QStatusBar,
    QTableView,
    QVBoxLayout,
    QWidget
)

from .controller import (
    SearchBarController,
    ProfilingController
)
from .widgets import ProfilingWidget
from .dag_nodes import DagNodes

from ProfileInspector.src import nuke
from ProfileInspector.src.util.nuke_util import zoom_node
from ProfileInspector.src.widgets import SearchBarWidget, ToolBar
from ProfileInspector.src.util import TimeFormatter, widget_color, doc_file


LOGGER = logging.getLogger('ProfileInspector.dag_inspector')


class TableModel(QStandardItemModel):
    def __init__(self, rows=1, columns=2):
        QStandardItemModel.__init__(self, rows, columns)

        self._profiling_type = nuke.PROFILE_ENGINE
        self.nodes_data = DagNodes()

        self._time_format = 'ms'

        self.setHorizontalHeaderLabels(['Name', 'Type'])

    def data(self, index, role):
        node_list = self.nodes_data.nodes_list

        # python 3 dict.keys doesnt' return a list anymore
        nodes_name = list(node_list.keys())

        self.setRowCount(len(nodes_name))

        if role == Qt.DisplayRole:
            node_row = nodes_name[index.row()]

            if index.column() == 0:
                return node_row

            if index.column() == 1:
                return node_list[node_row]['class']

            # FIXME: column index shouldnt be fixed. also UGLY
            timings = node_list[node_row]['timings']
            if index.column() == 2:
                return timings['callCount']

            if index.column() == 3:
                time = timings['timeTakenWall']
                return TimeFormatter(time, self.time_format).str()

            if index.column() == 4:
                time = timings['timeTakenCPU']
                return TimeFormatter(time, self.time_format).str()

    @property
    def profiling_type(self):
        return self._profiling_type

    @profiling_type.setter
    def profiling_type(self, value):
        self._profiling_type = value

    @property
    def time_format(self):
        return self._time_format

    @time_format.setter
    def time_format(self, value):
        self._time_format = value

    def flags(self, index):
        if index.column() == 1:
            return Qt.ItemIsEnabled
        if index.column() == 2:
            return Qt.ItemIsEditable | Qt.ItemIsEnabled

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def update_data(self):
        LOGGER.debug('Update nodes data')
        self.nodes_data = DagNodes(self.profiling_type)
        self.setRowCount(len(self.nodes_data.nodes_list.keys()))


class TableView(QTableView):
    def __init__(self):
        QTableView.__init__(self)
        self.setWhatsThis(doc_file('dag_table'))

        self.settings = QSettings()

        self.setSortingEnabled(True)
        self._table_model = TableModel()

        self._filter_proxy = QSortFilterProxyModel()
        self._filter_proxy.setSortCaseSensitivity(Qt.CaseInsensitive)
        self._filter_proxy.setSourceModel(self._table_model)
        self._filter_proxy.setFilterKeyColumn(0)
        self._filter_proxy.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.setModel(self._filter_proxy)

        self._selection_model = self.selectionModel()
        self._selection_model.currentChanged.connect(self._zoom_by_arrows)

        self.doubleClicked.connect(self._double_clicked)

        for column in range(2):
            self.setColumnWidth(column, 150)

    def selection_model(self):
        return self.selectionModel()

    def filter_model(self):
        return self._filter_proxy

    @property
    def table_model(self):
        return self.model().sourceModel()

    def refresh(self):
        # XXX: not sure about refreshing profiling timers always
        # TODO: find a better way to refresh table instead of reset
        if nuke.usingPerformanceTimers():
            self.table_model.update_data()
            self.reset()
        else:
            nuke.startPerformanceTimers()
            self.table_model.update_data()
            self.reset()
            nuke.stopPerformanceTimers()

    @staticmethod
    def _zoom_by_arrows(current_selection, previous_selection):
        if current_selection.column() == 0:
            node = current_selection.data()
            zoom_node(node)

    def _double_clicked(self, item):
        if item.column() == 0:

            force_float = self.settings.value(
                'force_float', False) in (True, 'true')

            LOGGER.debug('Show panel for: %s - floating window: %s',
                         item.data(), force_float)

            nuke.show(nuke.toNode(item.data()), forceFloat=force_float)

    def _update_profiling_type(self, index):
        self.table_model.profiling_type = index

    def _update_profiling_timings(self, time_format):
        self.table_model.time_format = time_format

    def _create_profiling_columns(self):
        # TODO: should see if hiding/un hiding is better
        nuke.startPerformanceTimers()
        self.table_model.update_data()

        profiling_columns = ['callCount', 'timeTakenWall', 'timeTakenCPU']
        column_count = self.table_model.columnCount()

        for index, column in enumerate(profiling_columns, column_count):

            LOGGER.debug('Adding column %s at %s', column, index)
            self.table_model.setHorizontalHeaderItem(
                index, QStandardItem(column))

        nuke.stopPerformanceTimers()

    def _delete_profiling_columns(self):
        LOGGER.debug('Deleting profiling columns')
        nuke.stopPerformanceTimers()
        self.table_model.removeColumns(self.table_model.columnCount() - 3, 3)


class DagPageLayout(QWidget):
    @widget_color
    def __init__(self):
        QWidget.__init__(self)

        self.profiling_section = ProfilingWidget()
        self.search_bar = SearchBarWidget()
        self.table_view = TableView()

        self.refresh_table_btn = QPushButton('Refresh Table')
        self.refresh_table_btn.setWhatsThis(doc_file('dag_refresh_table'))
        self.refresh_table_btn.setToolTip(
            'Refresh table by reloading nodes data'
        )
        self.refresh_table_btn.clicked.connect(self.table_view.refresh)

        _layout = QVBoxLayout()
        _layout.addWidget(self.profiling_section)
        _layout.addWidget(self.refresh_table_btn)
        _layout.addWidget(self.search_bar)
        _layout.addWidget(self.table_view)

        self.setLayout(_layout)


class DagToolBar(ToolBar):
    def __init__(self):
        ToolBar.__init__(self)

        self.reset_timings = QAction(
            QIcon(':/icons/stopwatch'), 'Reset Timings', self)
        self.reset_timings.setStatusTip(
            'Reset profiling timings. Equivalent to: nuke.resetProfilingTimers()')

        self.clear_callbacks = QAction(
            QIcon(':/icons/clear-all'), 'Clear Callbacks', self)
        self.clear_callbacks.setStatusTip(
            'Force cleaning possible leftover callbacks created from the Live profiling'
        )

        self.addAction(self.reset_timings)
        self.addAction(self.clear_callbacks)
        self.addAction(self._help_button)


class DagInspector(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.toolbar = DagToolBar()
        self.addToolBar(self.toolbar)

        self.dag_page = DagPageLayout()
        self.setCentralWidget(self.dag_page)

        self._profiling = ProfilingController(self)
        self._search_bar = SearchBarController(self)

        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)

    def show_message(self, message, timeout=5000):
        return self.status_bar.showMessage(message, timeout)

    @ property
    def profiling_section(self):
        return self.dag_page.profiling_section

    @ property
    def search_bar(self):
        return self.dag_page.search_bar

    @ property
    def table_view(self):
        return self.dag_page.table_view

    @ property
    def table_model(self):
        return self.dag_page.table_view.table_model
