# coding: utf-8
from __future__ import print_function


from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt

from PySide2.QtWidgets import (
    QHBoxLayout,
    QWidget,
    QAction,
    QToolButton,
    QPushButton,
    QLineEdit,
    QHBoxLayout
)

from ProfileInspector.src import util


class ReplaceNode(QWidget):
    # ! TODO: implement this section by itself or with the rename section
    def __init__(self):
        QWidget.__init__(self)
        util.widget_color(self, 'blue')

        self.setHidden(True)
        replace_icon = QAction('Search', self)
        replace_icon.setIcon(QIcon(":/icons/replace"))

        _layout = QHBoxLayout()
        _layout.setMargin(0)

        _layout.addSpacing(35)

        # _layout.addWidget(QLabel('Replace'))
        q = QLineEdit()
        q.setPlaceholderText('Replace')
        q.addAction(replace_icon, QLineEdit.LeadingPosition)
        _layout.addWidget(q)

        t1 = QToolButton()
        t1.setArrowType(Qt.LeftArrow)
        _layout.addWidget(t1)

        t2 = QToolButton()
        t2.setArrowType(Qt.RightArrow)
        _layout.addWidget(t2)

        _layout.addWidget(QPushButton('Replace'))
        _layout.addWidget(QPushButton('Replace All'))

        self.setLayout(_layout)
