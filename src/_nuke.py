"""
nuke.startPerformanceTimers()
for node in nuke.allNodes(recurseGroups=True):

    timings = ""
    if nuke.usingPerformanceTimers():
        timings = node.performanceInfo()

    print node.fullName(), timings

nuke.stopPerformanceTimers()
"""

# coding: utf-8
from __future__ import print_function

import random
import logging

PROFILE_STORE = 0
PROFILE_VALIDATE = 1
PROFILE_REQUEST = 2
PROFILE_ENGINE = 3

LOGGER = logging.getLogger('NodeBox._nuke')


def allNodes():
    node_names = ['Grade', 'Write', 'Shuffle', 'Dot1', 'Viewer11',
                  'Axis', 'Roto', 'Viewer', 'Write', 'o_test',
                  'ColorCorrection', 'Reconcile3D', 'Transform',
                  'Diff_color_walls', 'Diff_indirect_walls']
    node_list = set()

    node_index = 1
    while len(node_list) <= random.randint(15, 16):
        random_node = random.choice(node_names)

        if random.randint(1, 10) % 2 == 0:
            node_index = 1

        random_node += str(node_index)

        node_list.add(random_node)

        node_index += 1

    return [Node(n) for n in set(node_list)]


class callbacks:
    updateUIs = {'*': []}
    knobChangeds = {'*': []}


def addKnobChanged(call, args=(), kwargs={}, nodeClass="*"):
    LOGGER.info('KnobChanged enabled')
    call()


def addUpdateUI(call, args=(), kwargs={}, nodeClass="*"):
    LOGGER.info('UpdateUI enabled')
    call()


class root:
    def name(self):
        return 'ProjectName'


class ProfileState:
    state = False

    @classmethod
    def update_state(cls, state):
        cls.state = state

    @classmethod
    def get_state(cls):
        return cls.state


class Node:
    """Nuke node class imitation."""

    def __init__(self, node):
        self.node = node

    def setName(self, name):
        pass

    def setSelected(self, state):
        pass

    def name(self):
        return self.node

    def Class(self):
        return self.node[:-1]

    def dependent(self):
        a = Node('Random')
        b = Node('Random2')
        return None

    @staticmethod
    def performanceInfo(stats=PROFILE_ENGINE):
        LOGGER.debug('Profiling type: %s', stats)

        def r(): return random.randint(0,  10000000)

        return {'callCount': r(),
                'timeTakenWall': r(),
                'timeTakenCPU': r()}


def startPerformanceTimers():
    LOGGER.info('-> Start Profiling')
    ProfileState().update_state(True)


def stopPerformanceTimers():
    LOGGER.info('Stop Profiling <-')
    ProfileState().update_state(False)


def usingPerformanceTimers():
    state = ProfileState().get_state()
    LOGGER.debug('Using Profiling: %s', state)
    return state


def resetPerformanceTimers():
    LOGGER.info('Reset Profiling Timers')


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
    LOGGER.info('Show panel for: %s', node)


def test_class():
    '''
    dict = {'Write1' : {
        'class': 'WRITE',
        'timinigs' : {
            'callCount': 1,
            'timeTakenWall': 1,
            'timeTakenCPU': 1
            }
        }
    }
    '''
    node_dict = {}
    using_timers = usingPerformanceTimers()

    for node in allNodes():
        node_dict[node.name()] = {}
        node_dict[node.name()].update({'class': node.Class()})
        if using_timers:
            node_dict[node.name()].update({'timings': node.performanceInfo()})

    # return collections.OrderedDict(sorted(node_dict.items()))


if __name__ == '__main__':
    test_class()
