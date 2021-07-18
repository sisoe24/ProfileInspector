# coding: utf-8
from __future__ import print_function

import sys
import logging

from PySide2.QtCore import QSysInfo, __version__

from ProfileInspector.src import logger
from ProfileInspector.src import resources
# from ProfileInspector.src.version import _about

LOGGER = logging.getLogger('ProfileInspector.init')
try:
    import nuke
except ImportError as error:
    LOGGER.warning('%s: app is standalone' % error)
    try:
        from . import _nuke as nuke
    except Exception as error:
        LOGGER.critical(error, exc_info=True)
        sys.exit()

__about__ = {
    'ProfileInspector': '0.0.1',
    'PySide2': __version__,
    'Nuke': nuke.NUKE_VERSION_STRING,
    'machine': QSysInfo().prettyProductName()
}
