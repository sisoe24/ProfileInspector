# coding: utf-8
from __future__ import print_function

import sys
import logging

from ProfileInspector.src import logger
from ProfileInspector.src import resources
from ProfileInspector.src.version import __version__

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
