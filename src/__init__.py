# coding: utf-8
from __future__ import print_function

# FIXME: something wrong happens here when there is an error loading a module
try:
    import nuke
except ImportError as error:
    print('%s\nNuke built-in module not found.\nFallback to custom for testing\n' % error)
    try:
        from . import _nuke as nuke
    except Exception as error:
        print("Generic Exception: %s" % error)

try:
    from NodeBox.src import logger
    from NodeBox.src import util
    from NodeBox.src.widgets import *
    from NodeBox.src import main
    from NodeBox.src import resources
except Exception as error:
    print("Generic Exception: %s" % error)
