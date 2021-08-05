from . import _nuke as nuke


def zoom_node(node):
    if nuke.nodesSelected():
        for _ in nuke.selectedNodes():
            _.setSelected(False)

    nuke.toNode(node).setSelected(True)
    nuke.zoomToFitSelected()
