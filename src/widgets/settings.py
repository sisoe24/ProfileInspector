# coding: utf-8
from __future__ import print_function
from PySide2.QtCore import QSettings

from PySide2.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget
)


class TableOptions(QGroupBox):
    def __init__(self, title='Table'):
        QGroupBox.__init__(self, title)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.settings = QSettings()

        _layout = QFormLayout()

        self._exclude_class = QLineEdit()
        self._exclude_class.setPlaceholderText(
            'Node Class delimiteted by comma')
        self._exclude_class.setText(self.settings.value('exclude_nodes', ''))
        self._exclude_class.textChanged.connect(self._update_exclude_class)

        self._force_float = QCheckBox()
        self._force_float.setChecked(
            self.settings.value('force_float', False) == "true"
        )
        self._force_float.clicked.connect(self._update_force_float)

        _layout.addRow(QLabel('Exclude node class'), self._exclude_class)
        _layout.addRow(QLabel('Force Floating Properties'),  self._force_float)

        self.setLayout(_layout)

    def _update_exclude_class(self, text):
        self.settings.setValue('exclude_nodes', text)

    def _update_force_float(self):
        self.settings.setValue('force_float', self._force_float.isChecked())
        self.settings.sync()


class SearchBarOptions(QGroupBox):
    def __init__(self, title='SearchBar'):
        QGroupBox.__init__(self, title)

        self.settings = QSettings()

        _layout = QFormLayout()
        self._zoom_when_search = QCheckBox()

        self._zoom_when_search.setChecked(
            self.settings.value('zomm_search', True) == "true"
        )

        self._zoom_when_search.clicked.connect(self.update_zoom_search)

        _layout.addRow(QLabel('Zoom when search'), self._zoom_when_search)

        self.setLayout(_layout)

    def update_zoom_search(self):
        self.settings.setValue(
            'zomm_search', self._zoom_when_search.isChecked())
        self.settings.sync()

    def is_zoom_enabled(self):
        return self._zoom_when_search.isChecked()


class SettingsWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        _layout = QHBoxLayout()

        self._options = SearchBarOptions()

        _layout.addWidget(self._options)
        _layout.addWidget(TableOptions())

        self.setLayout(_layout)

    @property
    def zoom_when_search(self):
        return self._options.is_zoom_enabled()
