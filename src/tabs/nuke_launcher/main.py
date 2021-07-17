# coding: utf-8
from __future__ import print_function

import logging


from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon

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
    QToolButton,
    QVBoxLayout,
    QWhatsThis,
    QWidget,

)

from ProfileInspector.src import nuke
from ProfileInspector.src.util import widget_color, doc_file
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
    def __init__(self, title='New Nuke instance'):
        QGroupBox.__init__(self, title)

        self.setStyleSheet('''
            QToolButton {
                border: none;
            }
            QLabel {
                qproperty-alignment: AlignRight;
            }
            ''')

        self._layout = QGridLayout()
        self._layout.setAlignment(Qt.AlignLeft)

        self.app_label = QLineEdit()
        self.select_exec = QToolButton()
        self.set_nuke_exec()

        self.nuke_comp = QLineEdit()
        self.select_comp = QToolButton()
        self.set_nuke_comp()

        self.file_label = QLineEdit()
        self.select_file = QToolButton()
        self.set_nuke_file()

        self.mode_label = QComboBox()
        self.set_modes()

        self._layout.addWidget(QLabel('Nuke Mode'), 3, 0)
        self._layout.addWidget(self.mode_label, 3, 1)

        self.setLayout(self._layout)

    def set_nuke_exec(self):
        self.app_label.setToolTip('Nuke executable path')
        self.app_label.setText(nuke.env['ExecutablePath'])

        self._layout.addWidget(QLabel('Nuke Executable'), 0, 0)
        self._layout.addWidget(self.app_label, 0, 1)

        self.select_exec.setIcon(QIcon(':/icons/folder'))
        self.select_exec.setToolTip('Select Nuke executable')

        self._layout.addWidget(self.select_exec, 0, 2)

    def set_nuke_comp(self):
        self.nuke_comp.setToolTip('Nuke composition')

        self._layout.addWidget(QLabel('Nuke Comp'), 1, 0)
        self._layout.addWidget(self.nuke_comp, 1, 1)

        self.select_comp.setIcon(QIcon(':/icons/folder'))

        self._layout.addWidget(self.select_comp, 1, 2)

    def set_nuke_file(self):
        self.file_label.setToolTip('Nuke export xml file')

        self._layout.addWidget(QLabel('Export file'), 2, 0)
        self._layout.addWidget(self.file_label, 2, 1)

        self.select_file.setIcon(QIcon(':/icons/folder'))

        self._layout.addWidget(self.select_file, 2, 2)

    def set_modes(self):
        self.mode_label.setMaximumWidth(150)
        self.mode_label.setToolTip(
            'Set Nuke mode when launching a new instance')
        self.mode_label.addItems(
            ['', 'NukeX', 'NukeStudio', 'NukeIndie', 'NukeAssist',
             'Non-commercial']
        )


class OutputOptionsGroup(QGroupBox):
    @widget_color
    def __init__(self, title='Output Options'):
        QGroupBox.__init__(self, title)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        self.capture_output = QCheckBox('')
        self.capture_output.setToolTip(
            "Enable/Disable capturing Nuke's output when launching a new instance")
        self.capture_output.setChecked(True)

        self.optional_arg = QLineEdit()
        self.optional_arg.setToolTip(
            'Optionals arguments to be added when launching a new instance')

        self.verbose_level = QSpinBox()
        self.verbose_level.setToolTip('Verbose level for output')
        self.verbose_level.setRange(0, 3)

        _layout = QFormLayout()
        _layout.addRow(QLabel('Capture output:'), self.capture_output)
        _layout.addRow(QLabel('Optional args:'), self.optional_arg)
        _layout.addRow(QLabel('Verbose level:'), self.verbose_level)

        self.setLayout(_layout)


class UpperWidgets(QWidget):
    @widget_color
    def __init__(self):
        QWidget.__init__(self)

        _layout = QHBoxLayout()

        self.nuke_info = NukeInfoGroup()
        self.output_options = OutputOptionsGroup()

        _layout.addWidget(self.nuke_info)
        _layout.addWidget(self.output_options)

        self.setLayout(_layout)


class CaptureOutput(DockableWindow):
    def __init__(self):
        DockableWindow.__init__(self, title='Capture Output')
        self.setWhatsThis(doc_file('launcher_capture_output'))

        self.capture_output = CaptureStdoutDialog()
        self.setWidget(self.capture_output)


class LauncherMainGroup(QGroupBox):
    def __init__(self, title='Nuke Launcher'):
        QGroupBox.__init__(self, title)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        self.setAlignment(4)

        self._upper_widgets = UpperWidgets()
        self._launch_app = QPushButton('Launch Nuke Application')
        self._launch_app.setToolTip('Launch new Nuke instance')

        _layout = QVBoxLayout()
        _layout.addWidget(self._upper_widgets)
        _layout.addWidget(self._launch_app)

        self.setLayout(_layout)


class NukeLauncherToolBar(ToolBar):
    def __init__(self, *args, **kwargs):
        ToolBar.__init__(self)
        self.addAction(self._help_button)


class NukeLauncher(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setFocusPolicy(Qt.NoFocus)
        self.setWhatsThis(doc_file('launcher_capture_output'))

        toolbar = NukeLauncherToolBar()
        self.addToolBar(toolbar)

        self._launcher_group = LauncherMainGroup()
        self.setCentralWidget(self._launcher_group)

        self._output_dialog = CaptureOutput()
        self.addDockWidget(Qt.BottomDockWidgetArea, self._output_dialog)

        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)

        self._controller = LaunchNukeController(self)

    def show_message(self, msg, timeout=5000):
        self.status_bar.showMessage(msg, timeout)

    @ property
    def dock_widget(self):
        return self._output_dialog

    @ property
    def output_dialog(self):
        return self._output_dialog.capture_output

    @ property
    def launch_app(self):
        return self._launcher_group._launch_app

    @ property
    def nuke_info(self):
        return self._launcher_group._upper_widgets.nuke_info

    @ property
    def output_options(self):
        return self._launcher_group._upper_widgets.output_options
