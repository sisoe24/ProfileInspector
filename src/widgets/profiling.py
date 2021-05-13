# coding: utf-8
from __future__ import print_function

import logging

from PySide2.QtWidgets import (
    QSpinBox,
    QSizePolicy,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QFormLayout,
    QLabel,
    QComboBox,
    QCheckBox,
    QPushButton,
    QWidget,
    QGridLayout
)

from NodeBox.src import util

LOGGER = logging.getLogger('NodeBox.profiling')


class ExportGroup(QGroupBox):
    def __init__(self, title='Export'):
        QGroupBox.__init__(self, title)


class OptionGroup(QGroupBox):
    def __init__(self, title='Options'):
        QGroupBox.__init__(self, title)
        util.widget_color(self, 'red')

        form_layout = QFormLayout()

        self.combobox_profiling_type = QComboBox()
        self.combobox_profiling_type.addItems(
            ['Store', 'Validate', 'Requests', 'Engine']
        )
        self.combobox_profiling_type.setCurrentIndex(3)

        self.combobox_timings_format = QComboBox()
        self.combobox_timings_format.addItems(
            ['m:s:ms', 'm:s', 's:ms', 'ms']
        )
        self.combobox_timings_format.setCurrentIndex(2)

        form_layout.addRow(QLabel('Profiling Type'),
                           self.combobox_profiling_type)
        form_layout.addRow(QLabel('Timings format'),
                           self.combobox_timings_format)
        # form_layout.addRow(QLabel('Round ms by'),   QSpinBox())

        self.setLayout(form_layout)

    @property
    def timings_format(self):
        return self.combobox_timings_format

    @property
    def profiling_type(self):
        return self.combobox_profiling_type


class LiveGroup(QGroupBox):
    def __init__(self, title='Live Updates (Experimental)'):
        QGroupBox.__init__(self, title)
        # util.widget_color(self, 'red')
        # self.setCheckable(True)
        self.setEnabled(False)


        _layout = QVBoxLayout()

        layout_form = QFormLayout()

        self._toggle_live_update = QCheckBox()

        self._update_by_items = QComboBox()
        self._update_by_items.addItems(['updateUI', 'knobChanged'])
        self._update_by_items.setEnabled(False)

        layout_form.addRow(QLabel('Enable/Disable'), self._toggle_live_update)
        layout_form.addRow(QLabel('Update by:'), self._update_by_items)

        _layout.addLayout(layout_form)

        self.setLayout(_layout)

    def get_update_method(self):
        return self._update_by_items


class ButtonsLayout(QGridLayout):
    def __init__(self):
        QGridLayout.__init__(self)
        # self.setSpacing(0)
        self.setMargin(0)

        self._toggle_profiling_button = QPushButton('Start Profiling')
        self._toggle_profiling_button.setCheckable(True)
        self._clean_callbacks_button = QPushButton('Clean Callbacks')

        self._reset_button = QPushButton('Reset timings')

        self.addWidget(self._clean_callbacks_button, 0, 0)
        self.addWidget(self._toggle_profiling_button, 1, 0, 1, 2)
        self.addWidget(self._reset_button, 0, 1)

    def start_profiling(self):
        return self._toggle_profiling_button

    def reset_timings(self):
        return self._reset_button

    def clear_callbacks(self):
        return self._clean_callbacks_button


class ProfilingGroupsLayout(QHBoxLayout):
    def __init__(self):
        QHBoxLayout.__init__(self)

        self.live_group = LiveGroup()
        self.addWidget(self.live_group)

        self.options_group = OptionGroup()
        self.addWidget(self.options_group)

        self.export_group = ExportGroup()
        self.addWidget(self.export_group)


class ProfilingGroup(QGroupBox):

    def __init__(self, title='Activate'):
        QGroupBox.__init__(self, title)

        self.setCheckable(True)
        self.setChecked(False)

        _layout = QVBoxLayout()

        self.groups = ProfilingGroupsLayout()
        _layout.addLayout(self.groups)

        self.buttons = ButtonsLayout()
        _layout.addLayout(self.buttons)

        self.setLayout(_layout)


class ProfilingWidget(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        util.widget_color(self, 'pink')

        _layout = QVBoxLayout()
        _layout.setSpacing(0)
        _layout.setMargin(0)

        self._profiling_group = ProfilingGroup()
        self._options_group = self._profiling_group.groups.options_group
        self._live_group = self._profiling_group.groups.live_group

        self._buttons = self._profiling_group.buttons

        _layout.addWidget(self._profiling_group)
        self.setLayout(_layout)

    @property
    def format_time_changed(self):
        return self._options_group.combobox_timings_format.currentTextChanged

    @property
    def type_changed(self):
        return self._options_group.profiling_type.currentIndexChanged

    @property
    def live_group(self):
        return self._live_group

    @property
    def start(self):
        return self._buttons.start_profiling()

    @property
    def clear_callbacks(self):
        return self._buttons.clear_callbacks()

    @property
    def reset(self):
        return self._buttons.reset_timings()

    @property
    def change_update(self):
        return self._live_group._update_by_items

    def get_update_method(self):
        return self._live_group._update_by_items.currentText()

    @property
    def update_method_changed(self):
        return self._live_group._update_by_items.currentIndexChanged

    @property
    def enable_live(self):
        return self._live_group._toggle_live_update

    @property
    def toggled(self):
        return self._profiling_group.toggled
