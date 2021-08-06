# coding: utf-8
from __future__ import print_function
import logging

from ProfileInspector.src import nuke
LOGGER = logging.getLogger('ProfileInspector.profiling_controller')


def callback():
    nuke.resetPerformanceTimers()
    LOGGER.debug('Callback Call')


def clear_callbacks(_dict, _dict_name=''):
    LOGGER.debug('clearing callbacks for: %s', _dict_name)
    # XXX: updateUI actually starts empty and not with a asterisk
    if _dict.get('*', False):
        for index, func in enumerate(_dict['*']):
            if func[0].__name__ == callback.__name__:
                del _dict['*'][index]


def force_clean_callbacks():
    # XXX: temporary just to be sure user has the chance to clean callbacks
    clear_callbacks(nuke.callbacks.knobChangeds)
    clear_callbacks(nuke.callbacks.updateUIs)


class ProfilingController:
    def __init__(self, main_window):
        self.main_window = main_window
        self.profiling_section = self.main_window.profiling_section

        # Live group
        self.profiling_section.toggled.connect(self._toggle_profiling)
        self.profiling_section.enable_live.toggled.connect(self._toggle_live)
        self.profiling_section.update_method_changed.connect(
            self._change_update_method
        )

        # Options groups
        self.profiling_section.type_changed.connect(
            self._update_profiling_type)
        self.profiling_section.format_time_changed.connect(
            self._update_format_timings)

        # Buttons
        self.profiling_section.start.toggled.connect(self._start_profiling)
        # self.profiling_section.reset.clicked.connect(self._reset_timings)
        self.main_window.toolbar.reset_timings.triggered.connect(
            self._reset_timings)
        self.main_window.toolbar.clear_callbacks.triggered.connect(
            force_clean_callbacks)

    def _toggle_profiling(self, state):
        LOGGER.debug('Toggle Profiling: %s', state)
        if state is True:
            self.main_window.show_message('Profiling tab activated')
            self.main_window.table_view._create_profiling_columns()
        else:
            self.main_window.show_message('Profiling tab deactivated')
            self.main_window.table_view._delete_profiling_columns()

    def _toggle_live(self, state):
        self.main_window.show_message('Live update enabled')

        update_method = self.profiling_section.get_update_method()

        self.profiling_section.change_update.setEnabled(state)

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
        update_method = self.profiling_section.get_update_method()
        self.main_window.show_message('Live update changed to: ')

        if update_method == 'updateUI':
            clear_callbacks(nuke.callbacks.knobChangeds, 'knobs')
            self._toggle_live(True)
        elif update_method == 'knobChanged':
            clear_callbacks(nuke.callbacks.updateUIs, 'updateUI')
            self._toggle_live(True)

    def _update_profiling_type(self, index):
        self.main_window.show_message('Profiling type updated: %s' % index)
        LOGGER.debug('Profiling type updated: %s', index)

        self.main_window.table_view._update_profiling_type(index)
        self.main_window.table_view.refresh()

    def _update_format_timings(self, time_format):
        self.main_window.table_view._update_profiling_timings(time_format)

        self.main_window.show_message('Timings updated: %s' % time_format)
        LOGGER.debug('Timings format updated: %s', time_format)

        self.main_window.table_view.refresh()

    def _start_profiling(self, clicked):

        self.main_window.show_message('Profiling Started')

        self.profiling_section.live_group.setEnabled(clicked)

        if clicked:
            nuke.startPerformanceTimers()
            self.profiling_section.start.setText('Stop Profiling')
        else:
            self.main_window.show_message('Profiling Stopped')
            nuke.stopPerformanceTimers()
            self.profiling_section.start.setText('Start Profiling')
            force_clean_callbacks()

    def _reset_timings(self):
        self.main_window.show_message('Timers Reseted')
        nuke.resetPerformanceTimers()
        self.main_window.table_view.refresh()
