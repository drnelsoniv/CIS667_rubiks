
import rubiks_cube
import math
import time

visitTime = 0
copyTime = 0
treenodeCtorTime = 0

class RubiksTreeNode:
    def __init__(self, parent, cube):
        self.parent = parent
        if parent == None:
            self.depth = 0
        else:
            self.depth = parent.depth + 1
        self.children = []
        self.cube = cube
        self.minCost = cube.totalCost
        self.action = None
        
        self.actions = []
        
    def __str__(self):
        return str(self.actions)
        
    def next(self):
        return self.children[0]
        
        for child in self.children:
            #print(str(child.minCost) + " " + str(self.minCost))
            if child.minCost == self.minCost: return child
        raise StopIteration("Out of children to search.  To developer: verify score is being tracked properly.")
        
    def propogateMinCost(self):
        self.children.sort(key=self.sortByCost)
        if self.minCost < self.children[0].minCost:
            self.minCost = self.children[0].minCost
            return self.parent
        elif self.minCost == self.children[0].minCost:
            return None
        else:
            raise StopIteration("Parent cost was greater than child.  How did we get here without updating parent cost to minimum child cost?  To developer: verify score is being tracked properly.")
    
    def sortByCost(self, node):
        return node.minCost
        
    def visit(self, validActions):
        global visitTime
        global copyTime
        global treenodeCtorTime
        timeVisitStart = time.process_time()
        for action in validActions:
            if self.action != None and\
                self.action[0] == action[0] and self.action[1] == action[1]:
                # This represents an action with the same index and plane
                # being executed back-to-back.  This will never be the case
                # as those two moves could be reduced to one move with a
                # composite rotation amount (or no moves if rotation sum % 360 = 0).
                # Do not add this action to the tree as it is wasted search time.
                continue
                
            #print("Performing action " + str(action))
            copyTimeStart = time.process_time()
            cubeCopy = self.cube.copy()
            cubeCopy.rotate(action)
            copyTime += time.process_time() - copyTimeStart
            
            treenodeCtorTimeStart = time.process_time()
            child = RubiksTreeNode(self, cubeCopy)
            #child.actions = self.actions + [action]
            #print("Investigating " + str(child.actions) + "...")
            child.action = action
            self.children.append(child)
            treenodeCtorTime += time.process_time() - treenodeCtorTimeStart

        self.children.sort(key=self.sortByCost)
        self.minCost = self.children[0].minCost
        #print("Setting min cost to " + str(self.minCost))
        visitTime += time.process_time() - timeVisitStart
        
    def visited(self):
        return len(self.children) > 0