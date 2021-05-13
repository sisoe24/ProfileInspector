# coding: utf-8
from __future__ import print_function

import logging
import collections

from PySide2.QtCore import (
    Qt,
    QSettings,
    QCoreApplication,
    QSortFilterProxyModel,
)

from PySide2.QtGui import QStandardItem, QStandardItemModel

from PySide2.QtWidgets import (
    QErrorMessage,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QStackedLayout,
    QStackedWidget,
    QStatusBar,
    QTabWidget,
    QTableView,
    QToolButton,
    QVBoxLayout,
    QWidget
)


from NodeBox.src.widgets import (
    SearchBarWidget,
    ProfilingWidget,
    RenameDialogBox, parse_user_variables,
    ButtonSection,
    SettingsWidget,
    XmlInspector
)


from NodeBox.src import nuke
from NodeBox.src.tmp import *
from NodeBox.src.util import TimeFormatter, widget_color


LOGGER = logging.getLogger('NodeBox.main')

# TODO: need to handle errors al launch time in nuke
# currently it works by launching nuke from CLI


def callback():
    nuke.resetPerformanceTimers()
    LOGGER.debug('Callback Call')


def clear_callbacks(_dict, _dict_name=''):
    LOGGER.info('clearing callbacks for: %s', _dict_name)
    # updateUI actually starts empty and not with a asterisk
    if _dict.get('*', False):
        for index, func in enumerate(_dict['*']):
            if func[0].__name__ == callback.__name__:
                del _dict['*'][index]


def force_clean_callbacks():
    # XXX: temporary just to be sure user has the chance to clean callbacks
    clear_callbacks(nuke.callbacks.knobChangeds)
    clear_callbacks(nuke.callbacks.updateUIs)


def zoom_node(node):
    if nuke.nodesSelected():
        for _ in nuke.selectedNodes():
            _.setSelected(False)

    nuke.toNode(node).setSelected(True)
    nuke.zoomToFitSelected()


class NodesData():
    def __init__(self, profiling_type=nuke.PROFILE_ENGINE):
        self.profiling_type = profiling_type

        self.settings = QSettings()
        self._exclude_nodes = self.settings.value('exclude_nodes', [])

        self.nodes_list = self._create_list()

    def _create_list(self):
        node_dict = {}
        using_timers = nuke.usingPerformanceTimers()

        LOGGER.debug('nuke all nodes\n%s', [i.name() for i in nuke.allNodes()])

        for node in nuke.allNodes():
            if node.Class() in self._exclude_nodes:
                continue
            node_dict[node.name()] = {}
            node_dict[node.name()].update({'class': node.Class()})
            if using_timers:
                node_dict[node.name()].update(
                    {'timings': node.performanceInfo(self.profiling_type)})

        return collections.OrderedDict(sorted(node_dict.items()))


class TableModel(QStandardItemModel):
    def __init__(self, rows=1, columns=2):
        QStandardItemModel.__init__(self, rows, columns)

        self._profiling_type = nuke.PROFILE_ENGINE
        self.nodes_data = NodesData()

        self._time_format = 's:ms'

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

    @ profiling_type.setter
    def profiling_type(self, value):
        self._profiling_type = value

    @property
    def time_format(self):
        return self._time_format

    @ time_format.setter
    def time_format(self, value):
        self._time_format = value

    def flags(self, index):
        if index.column() == 1:
            return Qt.ItemIsEnabled
        if index.column() == 2:
            return Qt.ItemIsEditable | Qt.ItemIsEnabled

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def update_data(self):
        LOGGER.info('Update nodes data')
        self.nodes_data = NodesData(self.profiling_type)
        self.setRowCount(len(self.nodes_data.nodes_list.keys()))


class TableView(QTableView):
    # XXX: make table resizable?
    def __init__(self):
        QTableView.__init__(self)

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

    @ staticmethod
    def _zoom_by_arrows(current_selection, previous_selection):
        if current_selection.column() == 0:
            node = current_selection.data()
            zoom_node(node)

    def _double_clicked(self, item):
        if item.column() == 0:
            nuke.show(nuke.toNode(item.data()),
                      forceFloat=self.settings.value('force_float', False))

    def _update_profiling_type(self, index):
        self.table_model.profiling_type = index

    def _update_profiling_timings(self, time_format):
        self.table_model.time_format = time_format

    def _create_profiling_columns(self):
        # TODO: should see if hiding/unhiding is better
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
        LOGGER.info('Deleting profiling columns')
        nuke.stopPerformanceTimers()
        self.table_model.removeColumns(self.table_model.columnCount() - 3, 3)


class TabWidget(QTabWidget):
    def __init__(self):
        QTabWidget.__init__(self)

        self.settings = QSettings()
        self.setMovable(True)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.addTab(ProfilingWidget(), 'Profiling')
        self.addTab(SettingsWidget(), 'Settings')
        self.addTab(QWidget(), 'Rename')

        self._load_tab_index()
        self.currentChanged.connect(self._save_tabs_index)

        self.setCurrentIndex(0)

    def _load_tab_index(self):
        new_positions = []

        self.settings.beginReadArray('tabs')

        for widget_index in range(self.count()):
            self.settings.setArrayIndex(widget_index)

            tab = self.settings.value('tab')

            # if first launch then dont load
            if not tab:
                self.settings.endArray()
                return

            new_positions.append(tab)

        self.settings.endArray()

        # BUG: Cant set Rename - Profiling - Settings
        for widget_index in range(self.count()):
            tab_text = self.tabText(widget_index)
            self.tabBar().moveTab(widget_index, new_positions.index(tab_text))

    def _save_tabs_index(self):
        self.settings.beginWriteArray('tabs')
        for widget_index in range(self.count()):
            self.settings.setArrayIndex(widget_index)
            self.settings.setValue('tab', self.tabText(widget_index))

        self.settings.endArray()

    def get_tab(self, instance):
        for widget_index in range(self.count()):
            if isinstance(self.widget(widget_index), instance):
                return self.indexOf(self.widget(widget_index))

    @property
    def profiling(self):
        profile_tab = self.get_tab(ProfilingWidget)
        profiling_widget = self.widget(profile_tab)
        return profiling_widget

    @property
    def options(self):
        options_tab = self.get_tab(SettingsWidget)
        options_widget = self.widget(options_tab)
        return options_widget

    @property
    def user(self):
        return self.widget(2)


class StackSelector(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        _layout = QHBoxLayout()

        self._left = QToolButton()
        self._left.setArrowType(Qt.LeftArrow)

        self._right = QToolButton()
        self._right.setArrowType(Qt.RightArrow)

        self._widget_label = QLabel()
        # self._widget_label.setMaximumWidth(100)
        self._widget_label.setAlignment(Qt.AlignHCenter)

        _layout.addWidget(self._left)
        _layout.addWidget(self._widget_label)
        _layout.addWidget(self._right)

        self.setLayout(_layout)

    @property
    def left_button(self):
        return self._left

    @property
    def right_button(self):
        return self._right

    def set_label(self, value):
        return self._widget_label.setText(value)


class TableSection(QVBoxLayout):
    def __init__(self):
        QVBoxLayout.__init__(self)

        self.table_stack = QStackedLayout()

        # TABLE 1
        table1_group = QGroupBox('Search Nodes')
        table1_group.setObjectName('Node Inspector')
        table1_group_layout = QVBoxLayout()

        self.search_bar = SearchBarWidget()
        self.table_view = TableView()
        self.lower_buttons = ButtonSection()

        table1_group_layout.addWidget(self.search_bar)
        table1_group_layout.addWidget(self.table_view)
        table1_group_layout.addWidget(self.lower_buttons)
        table1_group.setLayout(table1_group_layout)

        # TABLE 2

        self.table_stack = QStackedWidget()
        self.table_stack.addWidget(table1_group)
        self.table_stack.addWidget(XmlInspector())

        self.table_stack.setCurrentIndex(1)

        self._stack_selector = StackSelector()
        self._stack_selector.left_button.clicked.connect(
            lambda: self.change_stack(0)
        )
        self._stack_selector.right_button.clicked.connect(
            lambda: self.change_stack(1)
        )

        self._stack_selector.set_label(
            self.table_stack.currentWidget().objectName()
        )

        self.addWidget(self._stack_selector)
        self.addWidget(self.table_stack)

    def change_stack(self, index):
        self.table_stack.setCurrentIndex(index)
        self._stack_selector.set_label(
            self.table_stack.currentWidget().objectName()
        )


class ProfilingController:
    def __init__(self, main_window):
        self.main_window = main_window
        self.profiling = self.main_window.tabs_section.profiling
        # self._toggle_profiling(True)

        # Live group
        self.profiling.toggled.connect(self._toggle_profiling)
        self.profiling.enable_live.toggled.connect(self._toggle_live)
        self.profiling.update_method_changed.connect(
            self._change_update_method
        )

        # Options groups
        self.profiling.type_changed.connect(self._update_profiling_type)
        self.profiling.format_time_changed.connect(self._update_format_timings)

        # Buttons
        self.profiling.start.toggled.connect(self._start_profiling)
        self.profiling.reset.clicked.connect(self._reset_timings)
        self.profiling.clear_callbacks.clicked.connect(force_clean_callbacks)

    def _toggle_profiling(self, state):
        LOGGER.info('Toggle Profiling: %s', state)
        if state is True:
            self.main_window.show_message('Profiling tab activated')
            self.main_window.table_view._create_profiling_columns()
        else:
            self.main_window.show_message('Profiling tab deactivated')
            self.main_window.table_view._delete_profiling_columns()

    def _toggle_live(self, state):
        self.main_window.show_message('Live update enabled')

        update_method = self.profiling.get_update_method()

        self.profiling.change_update.setEnabled(state)

        def toggle_updateUI(state):
            if state:
                nuke.addUpdateUI(callback)
            else:
                clear_callbacks(nuke.callbacks.updateUIs)

        def toggle_knobChanged(state):
            if state:
                nuke.addKnobChanged(callback)
            else:
                clear_callbacks(nuke.callbacks.knobChangeds)

        if update_method == 'updateUI':
            toggle_updateUI(state)
        elif update_method == 'knobChanged':
            toggle_knobChanged(state)

    def _change_update_method(self):
        update_method = self.profiling.get_update_method()
        self.main_window.show_message('Live update changed to: ')

        if update_method == 'updateUI':
            clear_callbacks(nuke.callbacks.knobChangeds, 'knobs')
            self._toggle_live(True)
        elif update_method == 'knobChanged':
            clear_callbacks(nuke.callbacks.updateUIs, 'updateUI')
            self._toggle_live(True)

    def _update_profiling_type(self, index):
        self.main_window.show_message('Profiling type updated: %s' % index)
        LOGGER.info('Profiling type updated: %s', index)
        self.main_window.table_view._update_profiling_type(index)
        self.main_window.table_view.refresh()

    def _update_format_timings(self, time_format):
        self.main_window.table_view._update_profiling_timings(time_format)
        self.main_window.show_message('Timings updated: %s' % time_format)
        LOGGER.info('Timings format updated: %s', time_format)
        self.main_window.table_view.refresh()

    def _start_profiling(self, clicked):

        self.main_window.show_message('Profiling Started')

        self.profiling.live_group.setEnabled(clicked)

        if clicked:
            nuke.startPerformanceTimers()
            self.profiling.start.setText('Stop Profiling')
        else:
            self.main_window.show_message('Profiling Stopped')
            nuke.stopPerformanceTimers()
            self.profiling.start.setText('Start Profiling')
            force_clean_callbacks()

    def _reset_timings(self):
        self.main_window.show_message('Timers Reseted')
        nuke.resetPerformanceTimers()
        self.main_window.table_view.refresh()


class SearchBarController():
    # TODO: add shortcut for focusing line edit
    def __init__(self, main_window):
        self.main_window = main_window

        self.table_model = self.main_window.table_view.table_model
        self.table_filter = self.main_window.table_view.filter_model()

        self.search_bar = self.main_window.search_bar

        self.search_bar_filter = self.table_filter.setFilterRegExp

        self.search_bar.case_sensitive.toggled.connect(self._set_filter_case)

        # self.search_bar.filter_type.connect(self._use_regex)

        self.search_bar.search_by_column.connect(
            self.table_filter.setFilterKeyColumn
        )

        self.search_bar.return_pressed.connect(
            self.main_window.table_view.setFocus
        )

        self.search_bar.whole_word.toggled.connect(self._set_whole_word)
        self.search_bar.text_changed.connect(self._search_node)

        # HACK: reset the selection or it will zoom at every change
        self.search_bar.text_changed.connect(
            self.main_window.table_view.selection_model().reset
        )

        self.search_bar.text_changed.connect(self._zoom_by_search)

    def _set_whole_word(self):
        self.search_bar.update_word_icon()
        self._search_node(self.search_bar.text())

    def _search_node(self, text):

        if self.search_bar.search_whole_word():
            self.search_bar_filter(r'\b' + text)
        else:
            self.search_bar_filter(text)

    def _zoom_by_search(self, text):
        if self.main_window.options.zoom_when_search:
            matches = self.table_model.findItems(text, Qt.MatchContains, 0)
            for match in matches:
                # TODO: if no match then it should deselect last node
                column, row = match.column(), match.row()
                node = self.table_model.index(row, column).data()
                zoom_node(node)
                return

    def _set_filter_case(self, state):
        self.search_bar.update_case_icon()
        case = Qt.CaseInsensitive
        if state:
            case = Qt.CaseSensitive

        self.table_filter.setFilterCaseSensitivity(case)

    def _use_regex(self, state):
        # TODO: should evaluate if this is still needed

        self.search_bar.update_regex_icon()
        filter_type = {
            'Regex': self.table_filter.setFilterRegExp,
            'Wildcard': self.table_filter.setFilterWildcard,
            'FixedString': self.table_filter.setFilterFixedString,
        }

        search_filter = filter_type['Regex']
        if not state:
            search_filter = filter_type['Wildcard']

        self.search_bar_filter = search_filter

        # update filter with current text
        # this will "reset" the search if filter changes from regex to string
        self._search_node(self.search_bar.text())


class MainWindowLayout(QVBoxLayout):
    def __init__(self):
        QVBoxLayout.__init__(self)

        # self.setSpacing(0)
        self.setMargin(0)

        self.tabs_section = TabWidget()
        self.table_section = TableSection()

        self.refresh_table_btn = QPushButton('Refresh Table')
        self.refresh_table_btn.clicked.connect(self.table_view.refresh)

        self.status_bar = QStatusBar()

        self.addWidget(self.tabs_section)
        # self.addWidget(DockWidget())
        self.addWidget(self.refresh_table_btn)
        self.addLayout(self.table_section)
        self.addWidget(self.status_bar)

    def show_message(self, message, timeout=5000):
        return self.status_bar.showMessage(message, timeout)

    @property
    def options(self):
        return self.tabs_section.options

    @property
    def search_bar(self):
        return self.table_section.search_bar

    @property
    def table_view(self):
        return self.table_section.table_view

    @property
    def table_model(self):
        return self.table_section.table_view.table_model


class MainWindow(QWidget):
    def __init__(self):
        # TODO: should merge this class with MainWindowLayout
        QWidget.__init__(self)

        # parse_user_variables()

        QSettings.setDefaultFormat(QSettings.IniFormat)
        QCoreApplication.setOrganizationName('virgilsisoe')
        # QCoreApplication.setOrganizationDomain('github.com')
        QCoreApplication.setApplicationName('NodeBox')

        self.main_window = MainWindowLayout()

        self.profiling = ProfilingController(self.main_window)
        self.search_bar = SearchBarController(self.main_window)

        self.main_window.table_section.lower_buttons.rename.clicked.connect(
            self._rename_node)

        self.setLayout(self.main_window)

    def _rename_node(self):
        # ! TODO: handle multiple nodes
        # TODO: this function shouldn't be here
        selected_node = self.main_window.table_view.selectedIndexes()

        if len(selected_node) > 1:
            q = QErrorMessage()
            q.showMessage('Renaming multiple nodes not yet supported')
            q.exec_()
            return

        current_name = selected_node[0].data()
        rename_dialog = RenameDialogBox(current_name)
        rename_dialog.exec_()

        if rename_dialog.result():
            node = nuke.toNode(current_name)
            new_name = rename_dialog.get_text()
            node.setName(new_name)

            LOGGER.info('from: %s to: %s', current_name, new_name)

            self.main_window.table_view.refresh()


# HACK: use directly this into nuke
try:
    import nukescripts
except ImportError as e:
    LOGGER.warning('Import error: %s\n', e)
else:
    nukescripts.panels.registerWidgetAsPanel(
        'NodeBox.src.main.MainWindow', 'NodeBox',
        'uk.co.thefoundry.MainWindow')
