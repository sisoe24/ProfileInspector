# coding: utf-8
from __future__ import print_function

from PySide2.QtCore import Qt, QSettings
from PySide2.QtGui import QColor, QPainter, QPalette

from PySide2.QtWidgets import (
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from ProfileInspector.src.util import doc_file

BG_COLOR = QColor(30, 30, 30, 150)


class HoverText(QTextEdit):
    def __init__(self):
        QTextEdit.__init__(self)
        self.setReadOnly(True)

        self.setStyleSheet('''
            QTextEdit {
                font-size: 12px;
                background-color: rgb(%s, %s, %s, %s);
            }
            ''' % (BG_COLOR.red(), BG_COLOR.blue(), BG_COLOR.green(), BG_COLOR.alpha())
        )


class HoverHelper(QWidget):
    def __init__(self, parent, file):
        QWidget.__init__(self, parent)
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowTransparentForInput |
            Qt.WindowDoesNotAcceptFocus
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self._file = file

        # self.penColor = QColor("#333333")
        self.fill_color = BG_COLOR

        _layout = QVBoxLayout()

        self._hover_text = HoverText()
        _layout.addWidget(self._hover_text)

        self.setLayout(_layout)

    def mouseMoveEvent(self, event):
        print("➡ event :", event)

    def paintEvent(self, event):
        size = self.size()

        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing, True)
        # qp.setPen(self.penColor)
        qp.setBrush(self.fill_color)
        qp.drawRect(0, 0, size.width(), size.height())
        qp.end()

    def set_text(self, text):
        self._hover_text.setHtml(text.decode('utf-8'))

    def _show(self):
        settings = QSettings()

        show_helper = settings.value('Helpers/dag_helper')

        if show_helper in (True, 'true'):

            self.set_text(doc_file(self._file))

            screen_position = self.parent().geometry()

            self.move(screen_position.x(), screen_position.y())

            parent_size = self.parent().size()
            self.resize(parent_size.width(), parent_size.height())

            self.show()


class TestClass(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self)
        self._hover = HoverHelper(self, 'test')

    @property
    def hover(self):
        return self._hover

    @hover.setter
    def hover(self, value):
        self._hover = value

    def enterEvent(self, event):
        self.hover._show()

    def leaveEvent(self, event):
        self.hover.close()
