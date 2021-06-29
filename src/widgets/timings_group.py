# coding: utf-8
from __future__ import print_function

from PySide2.QtWidgets import (
    QGroupBox,
    QFormLayout,
    QLabel,
    QComboBox,
)

from ProfileInspector.src.util import widget_color


class TimingsGroup(QGroupBox):
    @widget_color
    def __init__(self, title='Timings'):
        QGroupBox.__init__(self, title)

        self.form_layout = QFormLayout()

        self.combobox_profiling_type = QComboBox()
        self.combobox_profiling_type.addItems(
            ['Store', 'Validate', 'Request', 'Engine']
        )
        self.combobox_profiling_type.setCurrentIndex(3)

        self.combobox_timings_format = QComboBox()
        self.combobox_timings_format.addItems(
            ['m:s:ms', 'm:s', 's:ms', 'ms']
        )
        self.combobox_timings_format.setCurrentIndex(3)

        self.form_layout.addRow(QLabel('Profiling type'),
                                self.combobox_profiling_type)
        self.form_layout.addRow(QLabel('Timings format'),
                                self.combobox_timings_format)

        # TODO: add round by ms
        # self.form_layout.addRow(QLabel('Round ms by'), QSpinBox())

        self.setLayout(self.form_layout)

    @ property
    def timings_format(self):
        return self.combobox_timings_format

    @ property
    def profiling_type(self):
        return self.combobox_profiling_type
