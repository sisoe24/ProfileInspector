# coding: utf-8
from __future__ import print_function

"""Logging module."""
import os
import sys
import logging

# base logging
LOGGER = logging.getLogger('NodeBox')

LOGGER.setLevel(logging.DEBUG)
LOGGER.setLevel(logging.INFO)

LOG_PATH = os.path.dirname(os.path.dirname(__file__))

CRITICAL_FORMAT = logging.Formatter(
    '%(asctime)s - [%(levelname)s] - %(module)s:%(lineno)d:%(funcName)s() - %(message)s')
CRITICAL = logging.FileHandler(os.path.join(LOG_PATH, 'log/errors.log'), 'a')
CRITICAL.setLevel(logging.WARNING)
CRITICAL.setFormatter(CRITICAL_FORMAT)
LOGGER.addHandler(CRITICAL)

BASE_FORMAT = logging.Formatter(
    '%(asctime)s - %(filename)-20s %(funcName)-25s %(levelname)-10s %(message)s')
DEBUG = logging.FileHandler(os.path.join(LOG_PATH, 'log/debug.log'), 'w')
DEBUG.setLevel(logging.DEBUG)
DEBUG.setFormatter(BASE_FORMAT)
LOGGER.addHandler(DEBUG)

CONSOLE_FORMAT = logging.Formatter(
    '[%(levelname)s] %(module)-7s%(lineno)-5d%(funcName)-25s : %(message)s')
CONSOLE = logging.StreamHandler(stream=sys.stdout)
CONSOLE.setLevel(logging.DEBUG)
CONSOLE.setFormatter(CONSOLE_FORMAT)
LOGGER.addHandler(CONSOLE)
