# coding: utf-8
from __future__ import print_function
""" OLD TABS WIDGET."""

from PySide2.QtWidgets import (
    QTabWidget,
    QSizePolicy
)

from PySide2.QtCore import (
    QSettings,
)


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
