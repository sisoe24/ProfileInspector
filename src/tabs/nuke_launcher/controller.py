# coding: utf-8
from __future__ import print_function

import os
import re
import shlex
import logging
import platform

from textwrap import dedent

from PySide2.QtCore import QProcess
from PySide2.QtWidgets import QFileDialog

from ProfileInspector.src import nuke
from ProfileInspector.src.widgets import ErrorDialog

from .util import _bypass_filedialog, mac_nuke_exec

LOGGER = logging.getLogger('ProfileInspector.nuke_launch_controller')

nuke.root().name()


class LaunchNukeController():
    @_bypass_filedialog
    def __init__(self, view):

        self._view = view
        self.nuke_info = self._view.nuke_info

        self.output_dialog = self._view.output_dialog

        self.output_options = self._view.output_options

        self.optional_args = self.output_options.optional_arg.text()

        self.verbose_level = 0
        self.verbose_option = self.output_options.verbose_level
        self.verbose_option.valueChanged.connect(
            self._set_verbose_level
        )

        self.output_options.capture_output.toggled.connect(
            self._enable_capture
        )

        self.launch_float = self.output_options.launch_float

        # BUTTONS
        self.buttons = self._view.buttons
        self.buttons.select_app.clicked.connect(self.set_nuke_app)
        self.buttons.select_file.clicked.connect(self.set_export_file)
        self.buttons.select_project.clicked.connect(self.set_nuke_project)

        self.launch_app = self.buttons.launch_app
        self.launch_app.clicked.connect(self.execute_cmd)

        # NUKE APP
        self.nuke_app = nuke.env['ExecutablePath']
        self.nuke_app_name = os.path.basename(self.nuke_app)

        # CAPTURE OUT PROCESS
        self.process = QProcess()
        self.output_dialog.force_quit_btn.clicked.connect(
            self.process.terminate
        )

        self.process.readyRead.connect(self.dataReady)

        self.process.started.connect(lambda: self.launch_app.setEnabled(False))
        self.process.started.connect(
            lambda: LOGGER.debug('Nuke subprocess started')
        )

        self.process.finished.connect(lambda: self.launch_app.setEnabled(True))
        self.process.finished.connect(
            lambda: LOGGER.debug('Nuke subprocess finished')
        )

        self.process.stateChanged.connect(
            self._set_capture_status
        )

    def _set_capture_status(self, state):
        status = 'Process: %s' % state.name.decode('utf-8')
        timeout = 0
        if state.name == 'NotRunning':
            timeout = 5000
        self._view.show_message(status, timeout)

    def _set_verbose_level(self, value):
        self.verbose_level = value

    def _enable_capture(self, state):
        if state:
            self.process.readyRead.connect(self.dataReady)
        else:
            self.process.readyRead.disconnect(self.dataReady)

    def dataReady(self):
        self.output_dialog.show()
        cursor = self.output_dialog.output.textCursor()
        cursor.movePosition(cursor.End)

        raw_data = self.process.readAll()
        data = raw_data.data().decode('utf-8')

        cursor.insertText(data)
        self.output_dialog.output.ensureCursorVisible()

    def set_export_file(self):
        project_file, _ = os.path.splitext(nuke.root().name())
        project_file += project_file + '_profiling_report.xml'
        file, _ = QFileDialog.getSaveFileName(dir=project_file)

        self.nuke_info.file_label.setText(file)
        self.enable_launch()

    def set_nuke_project(self):
        project, _ = QFileDialog.getOpenFileName(dir='other', filter='*.nk')
        if not project:
            return
        self.nuke_info.project_label.setText(project)

    def set_nuke_app(self):
        app, _ = QFileDialog.getOpenFileName(dir='/Applications/Nuke13.0v1')

        if not app:
            return

        if not re.search(r'Nuke\d\d\.\d(\w\d(\.(app|exe))?)?$', app):
            q = ErrorDialog(self._view, 'Please select base Nuke application.')
            q.setDetailedText('Not valid: %s\n\n'
                              'Select base Nuke (eg: Nuke13.0v1)'
                              'and not derivates like NukeX, NukeStudio ecc' % app)
            q.exec_()
            return

        self.nuke_app = app
        self.nuke_app_name = os.path.basename(app)

        self.nuke_info.app_label.setText(self.nuke_app_name)
        self.enable_launch()

    def enable_launch(self):
        if self.nuke_info.app_label.text() and self.nuke_info.file_label.text():
            self.launch_app.setEnabled(True)

    def get_arg_opt(self):

        arg_opt = {
            'NukeX': '--nukex',
            'NukeStudio': '--nukestudio',
            'NukeAssist': '--nukeassist',
            'NukeIndie': '--nukeindie',
            'Non-commercial': '--nc',
        }

        return arg_opt.get(self.nuke_info.mode_label.currentText(), '')

    def _launch_float(self):
        if self.launch_float.isChecked():
            self._view.dock_widget.setFloating(True)

    def execute_cmd(self):
        self._launch_float()

        nuke_mode = self.get_arg_opt()
        project = self.nuke_info.project_label.text()

        xml_file = self.nuke_info.file_label.text()
        verbose_level = self.verbose_level

        optionals = self.output_options.optional_arg.text()

        args = shlex.split(
            '{mode} -V {level} {optionals} -Pf {file} {project}'.format(
                level=verbose_level,
                mode=nuke_mode,
                project=project,
                file=xml_file,
                optionals=optionals)
        )

        program = self.nuke_app

        if platform.system() == 'Darwin' and not '/Contents/MacOS' in self.nuke_app:
            program = mac_nuke_exec(self.nuke_app)
            if not program:
                q = ErrorDialog(self._view,
                                "Coulnd't find a valid nuke executable")
                q.setDetailedText(
                    'Try selecting it manually by going to:'
                    'App -> Show Contents -> Contents/MacOS')
                q.exec_()
                return

        elif platform.system() == 'Window':
            # TODO: need to check on windows
            program = self.nuke_app

        self.output_dialog.output.insertPlainText(
            dedent('''
            =================
            Profile Inspector

            %s %s

            =================

            ''').lstrip() % (program, ' '.join(args))
        )

        self.process.start(program, args)
