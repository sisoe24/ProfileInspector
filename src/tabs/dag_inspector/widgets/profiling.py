# coding: utf-8
from __future__ import print_function

import logging


from PySide2.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QFormLayout,
    QLabel,
    QComboBox,
    QCheckBox,
    QPushButton,
    QWidget,
    QGridLayout,
)

from ProfileInspector.src.util import widget_color, doc_file
from ProfileInspector.src.widgets import TimingsGroup

LOGGER = logging.getLogger('ProfileInspector.dag_profiling')


class LiveGroup(QGroupBox):
    @widget_color
    def __init__(self, title='Live Updates (Experimental)'):
        QGroupBox.__init__(self, title)
        self.setWhatsThis(doc_file('dag_live_update'))

        _layout = QVBoxLayout()

        layout_form = QFormLayout()

        self._toggle_live_update = QCheckBox()
        self._toggle_live_update.setToolTip('Enable/Disable live update')

        self._update_by_items = QComboBox()
        self._update_by_items.setToolTip('Change live update method')
        self._update_by_items.addItems(['updateUI', 'knobChanged'])
        self._update_by_items.setEnabled(True)

        layout_form.addRow(QLabel('Enable'), self._toggle_live_update)
        layout_form.addRow(QLabel('Update by:'), self._update_by_items)

        _layout.addLayout(layout_form)

        self.setLayout(_layout)

    #     self._hover = None

    # @property
    # def hover(self):
    #     return self._hover

    # @hover.setter
    # def hover(self, value):
    #     self._hover = value

    # def enterEvent(self, event):
    #     self.hover._show()

    # def leaveEvent(self, event):
    #     self.hover.close()

    def get_update_method(self):
        return self._update_by_items

    def clear_callbacks(self):
        return self._clean_callbacks_button


class ButtonsLayout(QGridLayout):
    def __init__(self):
        QGridLayout.__init__(self)
        self.setMargin(0)

        self._toggle_profiling_button = QPushButton('Start Profiling')
        self._toggle_profiling_button.setToolTip('Start/Stop profiling timers')
        self._toggle_profiling_button.setCheckable(True)

        self.addWidget(self._toggle_profiling_button, 0, 1, 1, 1)

    def start_profiling(self):
        return self._toggle_profiling_button

    def reset_timings(self):
        return self._reset_button


class ProfilingGroupsLayout(QHBoxLayout):
    def __init__(self):
        QHBoxLayout.__init__(self)

        self.live_group = LiveGroup()
        self.addWidget(self.live_group)

        self.options_group = TimingsGroup()
        self.addWidget(self.options_group)


class ProfilingGroup(QGroupBox):

    def __init__(self, title='Activate Profiling Section'):
        QGroupBox.__init__(self, title)
        self.setAlignment(4)

        self.setCheckable(True)
        self.setChecked(False)

        _layout = QVBoxLayout()

        self.groups = ProfilingGroupsLayout()
        _layout.addLayout(self.groups)

        self.buttons = ButtonsLayout()
        _layout.addLayout(self.buttons)

        self.setLayout(_layout)


class ProfilingWidget(QWidget):

    @ widget_color
    def __init__(self):
        QWidget.__init__(self)

        _layout = QVBoxLayout()
        _layout.setMargin(0)

        self._profiling_group = ProfilingGroup()
        self._options_group = self._profiling_group.groups.options_group
        self._live_group = self._profiling_group.groups.live_group

        self._buttons = self._profiling_group.buttons

        _layout.addWidget(self._profiling_group)
        self.setLayout(_layout)

    @ property
    def format_time_changed(self):
        return self._options_group.combobox_timings_format.currentTextChanged

    @ property
    def type_changed(self):
        return self._options_group.profiling_type.currentIndexChanged

    @ property
    def live_group(self):
        return self._live_group

    @ property
    def options_group(self):
        return self._options_group

    @ property
    def start(self):
        return self._buttons.start_profiling()

    @ property
    def reset(self):
        return self._buttons.reset_timings()

    @ property
    def change_update(self):
        return self._live_group._update_by_items

    def get_update_method(self):
        return self._live_group._update_by_items.currentText()

    @ property
    def update_method_changed(self):
        return self._live_group._update_by_items.currentIndexChanged

    @ property
    def enable_live(self):
        return self._live_group._toggle_live_update

    @ property
    def toggled(self):
        return self._profiling_group.toggled
