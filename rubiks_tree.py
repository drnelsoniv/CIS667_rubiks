
import rubiks_tree_node

class RubiksTree:
    def __init__(self, cube):
        self.root = rubiks_tree_node.RubiksTreeNode(None, cube)
        self.validActions = cube.validActions()
        self.currentSearchNode = self.root
        
    def next(self):
        currentNode = self.currentSearchNode
        while currentNode.visited():
            currentNode = currentNode.next()
        currentNode.visit(self.validActions)

        propogationNode = currentNode.parent
        lastPropogationNode = currentNode
        while propogationNode != None:
            lastPropogationNode = propogationNode
            propogationNode = propogationNode.propogateMinCost()
        self.currentSearchNode = lastPropogationNode
        
        return currentNode
        
    def getActions(self, node):
        strActions = []
        while node != self.root:
            strActions.append(node.cube.moveToString(node.action))
            node = node.parent
        strActions.reverse()
        return strActions
    