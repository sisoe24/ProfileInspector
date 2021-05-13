# coding: utf-8
from __future__ import print_function

import os
from datetime import datetime
from NodeBox.src import nuke


def _nb_node_class(node):
    """Return the class of the node.

    :symbol: $c
    :description: node class
    :param: nuke node object

    """
    return node.Class()


def _nb_project_name():
    """Return project name of current session.

    :symbol: $p
    :description: project name
    :param: nuke node object

    """
    return nuke.root().name()


def _nb_only_write(node, nodeClass="Write"):
    """Return file path name.

    :symbol: $f
    :description: write node file path
    :param: nuke node object

    """
    return node.name()


def _nb_current_date(nodeClass="*"):
    """Return current datetime.

    :symbol: $d
    :description: current date
    :param: nuke node object

    """
    return str(datetime.now())


def _nb_get_write():
    """Get last write from selected node.

    :symbol: $w
    :description: get last write node.

    """
    class NodeFinder:
        node = ""

        def __init__(self):
            self._node_class = 'Write'
            self.finder()

        def __str__(self):
            if self.node:
                return str(self.node.name())
            return ""

        def finder(self):
            selected_node = nuke.selectedNode()
            childrens = selected_node.dependent()

            if childrens:
                for node in childrens:

                    if node.Class() == self._node_class:
                        self.node = node

                    node.setSelected(True)
                    self.finder()
                    node.setSelected(False)

    return str(NodeFinder())


def _nb_XXX():
    """bo.
    :symbol: $x
    """
    return 'bo'


# TODO: this should be update to the function parsing
USER_VARIABLES = {
    "$p": _nb_project_name,
    "$d": _nb_current_date,
    "$c": _nb_node_class,
    "$s": "Custom String",
    "$w": _nb_get_write,
    "$g": _nb_only_write,
}


USER_REGEXP = {
    "$d": r'20[1-3][0-9](?(?=0)0[1-9]|1[0-2])(?(?=3)(3[0-1])|[0-2][0-9])',
    "$x": r'(<=^[A-Z]{3})\d{1,2}(?=_)'
}
