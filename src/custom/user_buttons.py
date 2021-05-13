from NodeBox.src import nuke


class NodeFinder:
    node = ""

    def __init__(self, node_class=""):
        self._node_class = "Write"
        self.finder()

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
