# coding: utf-8
from __future__ import print_function

import logging
import collections

from PySide2.QtCore import QSettings

from ProfileInspector.src import nuke

LOGGER = logging.getLogger('ProfileInspector.dag_nodes')


class DagNodes():
    def __init__(self, profiling_type=nuke.PROFILE_ENGINE):
        self.profiling_type = profiling_type

        self.settings = QSettings()
        self._exclude_nodes = self.settings.value('exclude_nodes', "")
        self._exclude_nodes = self._exclude_nodes.replace(',', '').split(' ')

        self.nodes_list = self._create_list()

    def _create_list(self):
        node_dict = {}
        using_timers = nuke.usingPerformanceTimers()

        # LOGGER.debug('nuke all nodes: %s', [i.name() for i in nuke.allNodes()])

        for node in nuke.allNodes():
            if node.Class() in self._exclude_nodes:
                continue
            node_dict[node.name()] = {}
            node_dict[node.name()].update({'class': node.Class()})
            if using_timers:
                node_dict[node.name()].update(
                    {'timings': node.performanceInfo(self.profiling_type)})

        return collections.OrderedDict(sorted(node_dict.items()))
