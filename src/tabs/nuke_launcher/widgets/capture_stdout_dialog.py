# coding: utf-8
from __future__ import print_function

from PySide2.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
    QPlainTextEdit
)

from ProfileInspector.src.util import doc_file


class CaptureStdoutDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        # self.setWhatsThis(doc_file('launcher_capture_output'))

        self.setWindowTitle('Profile Inspector - Capture stdout')
        self.setMinimumSize(600, 300)

        self.setStyleSheet('''
            QPlainTextEdit {
                background-color: rgb(33, 33, 33);
                color: white;
                font-family: Courier
            }''')

        self.output = QPlainTextEdit()
        self.output.setReadOnly(True)

        self.clear_text_btn = QPushButton('Clear Text')
        self.clear_text_btn.setToolTip('Clear output text')

        self.force_quit_btn = QPushButton('Force Quit')
        self.force_quit_btn.setToolTip('Force quit process')

        _buttons_layout = QHBoxLayout()
        _buttons_layout.addWidget(self.clear_text_btn)
        _buttons_layout.addWidget(self.force_quit_btn)

        self.clear_text_btn.clicked.connect(self.clear_text)

        _layout = QVBoxLayout()
        _layout.addWidget(self.output)
        _layout.addLayout(_buttons_layout)
        # _layout.addWidget(self.clear_text_btn)
        # _layout.addWidget(self.force_quit_btn)

        self.setLayout(_layout)

    def clear_text(self):
        self.output.clear()
