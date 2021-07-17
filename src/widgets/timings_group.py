# coding: utf-8
from __future__ import print_function

from textwrap import dedent


from PySide2.QtWidgets import (
    QGroupBox,
    QFormLayout,
    QLabel,
    QComboBox,
)


from ProfileInspector.src.util import widget_color, doc_file

TIMINGS_PROFILING_TYPE = '''
<b>Change profiling type</b><br>
store - store the values the user has selected on its knobs.<br>
validate - this is where the node tells Nuke about the output it produces. <br>
request - his is where the node works out what data it will need from its inputs in order to produce its output.<br>
engine - this is where the node does most of its work, and actually generates its output.<br>
'''

TIMINGS_FORMAT_TYPE = '''
<b> Convert table timings </b> <br>
ms - milliseconds <br>
s:ms - seconds, milliseconds <br>
m:s - minutes, seconds <br>
m:s:ms - minutes, seconds, milliseconds <br>
'''


class TimingsGroup(QGroupBox):
    @widget_color
    def __init__(self, title='Timings'):
        QGroupBox.__init__(self, title)
        self.setWhatsThis(doc_file('timings'))

        self.form_layout = QFormLayout()

        self.combobox_profiling_type = QComboBox()
        self.combobox_profiling_type.setToolTip('Change table profiling type')

        self.combobox_profiling_type.addItems(
            ['Store', 'Validate', 'Request', 'Engine']
        )
        self.combobox_profiling_type.setCurrentIndex(3)

        self.combobox_timings_format = QComboBox()
        self.combobox_timings_format.setToolTip('Convert table timings.')
        self.combobox_timings_format.addItems(
            ['m:s:ms', 'm:s', 's:ms', 'ms']
        )
        self.combobox_timings_format.setCurrentIndex(3)

        self.form_layout.addRow(QLabel('Profiling type'),
                                self.combobox_profiling_type)
        self.form_layout.addRow(QLabel('Timings format'),
                                self.combobox_timings_format)

        # TODO: add round by ms

        self.setLayout(self.form_layout)

    @ property
    def timings_format(self):
        return self.combobox_timings_format

    @ property
    def profiling_type(self):
        return self.combobox_profiling_type
