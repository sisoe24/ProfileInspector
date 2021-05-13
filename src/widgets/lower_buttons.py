# coding: utf-8
from __future__ import print_function

from PySide2.QtWidgets import (
    QGridLayout,
    QPushButton,
    QWidget
)


from NodeBox.src import util, nuke
from NodeBox.src.custom import user_buttons

# ! TODO: evaluate if this module should become a context menu based instead of buttons
# buttons will use too much space if there are many, while a menu is more
# compact

class ButtonsLayout(QGridLayout):
    def __init__(self):
        QGridLayout.__init__(self)

        btn_select = QPushButton('Select All')
        btn_select.clicked.connect(lambda: print('Press'))

        btn_disable = QPushButton('Disable Selected')
        btn_disable.clicked.connect(lambda: print('Press'))

        self.btn_rename = QPushButton('Rename')

        btn_find_write = QPushButton('Group Selected')

        self.addWidget(self.btn_rename, 0, 0)
        self.addWidget(btn_select, 0, 1)
        self.addWidget(btn_disable, 0, 2)
        self.addWidget(btn_find_write, 1, 1)

    def rename_button(self):
        return self.btn_rename


class ButtonSection(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        util.widget_color(self, 'blue')

        self._buttons_layout = ButtonsLayout()

        self._buttons_layout.setMargin(0)

        self.setLayout(self._buttons_layout)

    @property
    def rename(self):
        return self._buttons_layout.rename_button()
