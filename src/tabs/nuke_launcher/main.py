# coding: utf-8
from __future__ import print_function

import os
import logging


from PySide2.QtCore import Qt

from PySide2.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFormLayout,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QSpinBox,
    QStatusBar,
    QToolBar,
    QVBoxLayout,
    QWidget,

)

from ProfileInspector.src import nuke
from ProfileInspector.src.util import widget_color
from ProfileInspector.src.widgets import DockableWindow, ToolBar

from .widgets import CaptureStdoutDialog
from .controller import LaunchNukeController

LOGGER = logging.getLogger('ProfileInspector.xml_report')


class QHLine(QFrame):
    def __init__(self):
        QFrame.__init__(self,)

        self.setMinimumWidth(150)
        self.setFixedHeight(20)
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)


class NukeInfoGroup(QGroupBox):
    @widget_color
    def __init__(self, title='Nuke Info'):
        QGroupBox.__init__(self, title)

        nuke_exec = nuke.env['ExecutablePath']
        self.app_label = QLabel(os.path.basename(nuke_exec))
        self.app_label.setToolTip(nuke_exec)

        # TODO:file path could be too long
        self.file_label = QLabel('')

        self.mode_label = QComboBox()
        self.mode_label.setMinimumWidth(150)
        self.mode_label.addItems(
            ['', 'NukeX', 'NukeStudio', 'NukeIndie', 'NukeAssist',
             'Non-commercial']
        )

        self.project_label = QLabel(nuke.root().name())

        _layout = QFormLayout()
        _layout.setFormAlignment(Qt.AlignLeft)
        _layout.addRow(QLabel('Nuke Executable:'), self.app_label)
        _layout.addRow(QLabel('Nuke Project:'), self.project_label)
        _layout.addRow(QLabel('Report File:'), self.file_label)
        _layout.addRow(QLabel('Mode:'), self.mode_label)

        self.setLayout(_layout)


class OutputOptionsGroup(QGroupBox):
    @widget_color
    def __init__(self, title='Output Options'):
        QGroupBox.__init__(self, title)

        self.setMaximumWidth(250)

        self.capture_output = QCheckBox('')
        self.capture_output.setChecked(True)

        self.launch_float = QCheckBox('')
        # self.launch_float.setChecked(True)

        self.optional_arg = QLineEdit()

        self.verbose_level = QSpinBox()
        self.verbose_level.setRange(0, 3)

        _layout = QFormLayout()
        _layout.addRow(QLabel('Capture output:'), self.capture_output)
        # _layout.addRow(QLabel('Launch float:'), self.launch_float)
        _layout.addRow(QLabel('Optional args:'), self.optional_arg)
        _layout.addRow(QLabel('Verbose level:'), self.verbose_level)

        self.setLayout(_layout)


class UpperWidgets(QWidget):
    @widget_color
    def __init__(self):
        QWidget.__init__(self)
        self.setMaximumHeight(150)

        _layout = QHBoxLayout()

        self.nuke_info = NukeInfoGroup()
        self.output_options = OutputOptionsGroup()

        _layout.addWidget(self.nuke_info)
        _layout.addWidget(self.output_options)

        self.setLayout(_layout)


class ButtonSection(QWidget):
    @widget_color
    def __init__(self):
        QWidget.__init__(self)
        self.setMaximumHeight(100)

        self._select_app = QPushButton('Change Nuke executable')
        self._select_project = QPushButton('Change Nuke Project')
        self._select_file = QPushButton('Save Report to...')
        self._launch_app = QPushButton('Launch Nuke Application')
        self._launch_app.setEnabled(False)

        _layout = QGridLayout()
        _layout.addWidget(self._select_app, 0, 0)
        _layout.addWidget(self._select_project, 0, 1)
        _layout.addWidget(self._select_file, 0, 2)
        _layout.addWidget(self._launch_app, 1, 0, 1, 3)

        self.setLayout(_layout)

    @property
    def select_app(self):
        return self._select_app

    @property
    def select_project(self):
        return self._select_project

    @property
    def select_file(self):
        return self._select_file

    @property
    def launch_app(self):
        return self._launch_app


class CaptureOutput(DockableWindow):
    def __init__(self):
        DockableWindow.__init__(self, title='Capture Output')

        self.capture_output = CaptureStdoutDialog()
        self.setWidget(self.capture_output)


class LauncherMainGroup(QGroupBox):
    def __init__(self, title='Nuke Launcher'):
        QGroupBox.__init__(self, title)
        self.setMaximumHeight(300)
        self.setAlignment(4)

        self._upper_widgets = UpperWidgets()
        self._buttons = ButtonSection()

        _layout = QVBoxLayout()
        _layout.addWidget(self._upper_widgets)
        _layout.addWidget(self._buttons)

        self.setLayout(_layout)


class NukeLauncherToolBar(ToolBar):
    def __init__(self, *args, **kwargs):
        ToolBar.__init__(self)


class NukeLauncher(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # toolbar = NukeLauncherToolBar()
        # self.addToolBar(toolbar)

        self._launcher_group = LauncherMainGroup()
        self.setCentralWidget(self._launcher_group)

        self._output_dialog = CaptureOutput()
        self.addDockWidget(Qt.BottomDockWidgetArea, self._output_dialog)

        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)

        self._controller = LaunchNukeController(self)

    def show_message(self, msg, timeout=5000):
        self.status_bar.showMessage(msg, timeout)

    @property
    def dock_widget(self):
        return self._output_dialog

    @property
    def output_dialog(self):
        return self._output_dialog.capture_output

    @property
    def buttons(self):
        return self._launcher_group._buttons

    @property
    def nuke_info(self):
        return self._launcher_group._upper_widgets.nuke_info

    @property
    def output_options(self):
        return self._launcher_group._upper_widgets.output_options
