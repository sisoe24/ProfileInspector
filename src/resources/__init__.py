from PySide2.QtCore import QFile, QIODevice
from . import resources


def whats_this_doc(alias):
    file = QFile(':/docs/%s' % alias)

    file.open(QIODevice.ReadOnly)
    text = file.readAll()
    file.close()

    return text.data().decode('utf-8')
