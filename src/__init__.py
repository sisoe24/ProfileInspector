# coding: utf-8
from __future__ import print_function

import sys
import logging


from . import logger
from . import resources

LOGGER = logging.getLogger('ProfileInspector.init')
try:
    import nuke
except ImportError as error:
    LOGGER.warning('%s: app is standalone' % error)
    try:
        import _nuke as nuke
        nuke.set_logger(logger.LOG_PATH)

    except Exception as error:
        LOGGER.critical(error, exc_info=True)
        sys.exit()
else:
    from . import main
