# coding: utf-8
from __future__ import print_function

from PySide2.QtCore import QRegExp, QSettings, Qt
from PySide2.QtGui import QRegExpValidator

from PySide2.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QSizePolicy,
    QVBoxLayout,
    QWidget
)


class UpperSettings(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        self.settings = QSettings()

        _layout = QHBoxLayout()
        _layout.setMargin(0)

        self._zoom_when_search = QCheckBox('Zoom when searching')
        self._zoom_when_search.setToolTip(
            'When performing a search, it will automatically zoom on the first node that matches the search pattern.')
        self._zoom_when_search.setChecked(
            self.settings.value('zoom_search', True) == "true"
        )
        self._zoom_when_search.clicked.connect(self.update_zoom_search)

        self._force_float = QCheckBox('Force floating proprieties')
        self._force_float.setToolTip(
            'When double-clicking on a node name, the proprieties will be opened in a floating window rather than inside Proprieties panel'
        )

        self._force_float.setChecked(
            self.settings.value('force_float', False) == "true"
        )

        self._force_float.clicked.connect(self._update_force_float)
        _layout.addWidget(self._zoom_when_search)
        _layout.addWidget(self._force_float)

        self.setLayout(_layout)

    def update_zoom_search(self):
        self.settings.setValue(
            'zoom_search', self._zoom_when_search.isChecked())
        self.settings.sync()

    def is_zoom_enabled(self):
        return self._zoom_when_search.isChecked()

    def _update_force_float(self):
        self.settings.setValue('force_float', self._force_float.isChecked())
        self.settings.sync()


class ExcludeSettings(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.settings = QSettings()

        _layout = QHBoxLayout()
        _layout.setMargin(0)

        self._exclude_class = QLineEdit()
        self._exclude_class.setToolTip(
            '<nobr>Node Types(class) to be hidden in the table view.</nobr> <br>'
            'Names should be delimited by comma.'
        )
        self._exclude_class.setClearButtonEnabled(True)
        # self._exclude_class.setValidator(
        #     QRegExpValidator(QRegExp('[A-Z].+'))
        # )
        self._exclude_class.setPlaceholderText(
            'Node types to exclude delimited by comma')
        self._exclude_class.setText(self.settings.value('exclude_nodes', ''))
        self._exclude_class.textChanged.connect(self._update_exclude_class)

        _layout.addWidget(QLabel('Exclude nodes'))
        _layout.addWidget(self._exclude_class)

        self.setLayout(_layout)

    def _update_exclude_class(self, text):
        self.settings.setValue('exclude_nodes', text.title())


class SearchBarSettingsWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setHidden(True)

        _layout = QVBoxLayout()
        _layout.setMargin(0)

        self._upper_settings = UpperSettings()
        self._exclude_settings = ExcludeSettings()

        _layout.addWidget(self._upper_settings)
        _layout.addWidget(self._exclude_settings)

        self.setLayout(_layout)

    @property
    def zoom_when_search(self):
        return self._upper_settings.is_zoom_enabled()
