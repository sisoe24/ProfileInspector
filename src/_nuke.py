# coding: utf-8
from __future__ import print_function

import os
import random
import logging


def set_handler():
    handler = logging.FileHandler('log/nuke.log', 'w')
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter(
        '%(levelname)-8s %(funcName)-25s L:%(lineno)-3s :: %(message)s'
    ))
    return handler


LOGGER = logging.getLogger('nuke')
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(set_handler())


NUKE_VERSION_STRING = '13.0v1'

PROFILE_STORE = 0
PROFILE_VALIDATE = 1
PROFILE_REQUEST = 2
PROFILE_ENGINE = 3

env = {
    '64bit': True,
    'ExecutablePath': '/Applications/Nuke13.0v1/Nuke13.0v1.app/Contents/MacOS/Nuke13.0',
    'ExternalPython': False,
    'LINUX': False,
    'MACOS': True,
    'WIN32': False,
    'numCPUs': 10,
    'threads': 10,
    'NukeLibraryPath': '/Applications/Nuke13.0v1/Nuke13.0v1.app/Contents/MacOS/libnuke-13.0.1.dylib',
    'NukeVersionDate': 'Mar  9 2021',
    'NukeVersionMajor': 13,
    'NukeVersionMinor': 0,
    'NukeVersionPhase': None,
    'NukeVersionPhaseNumber': 633628,
    'NukeVersionRelease': 1,
    'NukeVersionString': '13.0v1',
    'PluginExtension': 'dylib',
    'PluginsVerbose': False,
    'assist': False,
    'gui': True,
    'hiero': False,
    'hieroNuke': False,
    'hieroStudio': False,
    'indie': False,
    'interactive': True,
    'nc': False,
    'nukex': False,
    'ple': False,
    'studio': False,
}


class callbacks:
    updateUIs = {'*': []}
    knobChangeds = {'*': []}


def addKnobChanged(call, args=(), kwargs={}, nodeClass="*"):
    LOGGER.debug('KnobChanged enabled')
    call()


def addUpdateUI(call, args=(), kwargs={}, nodeClass="*"):
    LOGGER.debug('UpdateUI enabled')
    call()


def showInfo(msg):
    return msg


class root:
    def name(self):
        path = 'string_placeholder_name_project.nk'

        tmp_project = 'other/test_project.nk'
        if os.path.exists(tmp_project):
            path = os.path.abspath(tmp_project)

        LOGGER.debug('Nuke.root() project name: %s', path)
        return path


def allNodes():
    nodes = {
        'Grade': 'Grade',
        'Render': 'Write',
        'ReadRGB': 'Shuffle',
        'Diff_color': 'Read',
        'Transform_Roto': 'Transform',
        'LeftAxis': 'Reconcile3D',
        'Dot': 'Dot', 'Viewer': 'Viewer',
    }

    nodes_list = {}
    node_index = 1

    while len(nodes_list) <= random.randint(15, 16):
        node_name = random.choice(nodes.keys())

        if random.randint(1, 10) % 2 == 0:
            node_index = 1

        node_name += str(node_index)

        nodes_list[node_name] = nodes[node_name[:-1]]

        node_index += 1

    return [Node(n) for n in nodes_list.items()]


class Node:
    """Nuke node class imitation."""

    def __init__(self, node):
        self.node = node

    def setName(self, name):
        pass

    def setSelected(self, state):
        pass

    def name(self):
        return self.node[0]

    def Class(self):
        return self.node[1]

    @staticmethod
    def performanceInfo(stats=PROFILE_ENGINE):
        LOGGER.debug('Profiling type: %s', stats)

        def r(): return random.randint(0,  10000000)

        return {'callCount': r(),
                'timeTakenWall': r(),
                'timeTakenCPU': r()}


class ProfileState:
    state = False

    @classmethod
    def update_state(cls, state):
        cls.state = state

    @classmethod
    def get_state(cls):
        return cls.state


def startPerformanceTimers():
    LOGGER.debug('-> Start Profiling')
    ProfileState().update_state(True)


def stopPerformanceTimers():
    LOGGER.debug('Stop Profiling <-')
    ProfileState().update_state(False)


def usingPerformanceTimers():
    state = ProfileState().get_state()
    LOGGER.debug('Profiling active: %s', state)
    return state


def resetPerformanceTimers():
    LOGGER.debug('Reset Profiling Timers')


def selectedNode():
    LOGGER.debug('Get selected node')
    return Node('Random')


def toNode(node):
    LOGGER.debug(node)
    return Node(str(node))


def zoomToFitSelected():
    LOGGER.debug('Zooming selected Node')


def nodesSelected():
    return True


def selectedNodes():
    return [Node(_) for _ in range(5)]


def show(node, forceFloat=False):
    LOGGER.debug('Show panel for: %s - floating: %s', node, forceFloat)


if __name__ == '__main__':

    for i in allNodes():
        print('name :', i.name(), '- class :', i.Class())
