# coding: utf-8
from __future__ import print_function

from PySide2.QtCore import QFile, QIODevice


def doc_file(alias):
    file = QFile(':/docs/%s' % alias)

    file.open(QIODevice.ReadOnly)
    text = file.readAll()
    file.close()

    return text.data().decode('utf-8')
