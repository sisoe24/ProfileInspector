"""Logging module."""
# coding: utf-8
from __future__ import print_function

import os
import sys
import logging

# ! TODO: nuke will create its own logging console stdout for some reason

LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'log')
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)


LOGGER = logging.getLogger('ProfileInspector')
LOGGER.setLevel(logging.DEBUG)

BASE_FORMAT = logging.Formatter(
    '[%(asctime)s] %(levelname)-10s %(filename)-20s %(funcName)-25s :: %(message)s',
    "%m-%d %I:%M%p")


def set_critical():
    critical = logging.FileHandler(os.path.join(LOG_PATH, 'errors.log'), 'w')
    critical.setLevel(logging.WARNING)
    critical.setFormatter(BASE_FORMAT)
    return critical


def set_debug():
    debug = logging.FileHandler(os.path.join(LOG_PATH, 'debug.log'), 'w')
    debug.setLevel(logging.DEBUG)
    debug.setFormatter(BASE_FORMAT)
    return debug


def set_console():
    console_format = logging.Formatter(
        '%(levelname)-8s:: %(module)-10s%(funcName)-15sL:%(lineno)-5d :: %(message)s')
    console = logging.StreamHandler(stream=sys.stdout)
    console.setLevel(logging.INFO)
    console.setFormatter(console_format)
    return console


LOGGER.addHandler(set_critical())
LOGGER.addHandler(set_debug())
LOGGER.addHandler(set_console())
