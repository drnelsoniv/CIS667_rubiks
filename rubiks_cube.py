
import numpy as np
import random
import math
import time

import rubiks_cubie

copyTime = 0

class RubiksCube:
    def __init__(self, cubeSize):
        self.cubeSize = cubeSize
        self.cube = None
        self.moveCost = 0
        self.totalCost = 0
        
        self.cubeIndices = np.array(range(self.cubeSize**3)).reshape(self.cubeSize,self.cubeSize,self.cubeSize)
        
    def __str__(self):
        return str(rubiks_cubie.RubiksCubie_str(self.cube))
        
    def copy(self):
        global copyTime
        
        cube = RubiksCube(self.cubeSize)
        
        copyTimeStart = time.process_time()
        cube.cube = rubiks_cubie.RubiksCubie_copy(self.cube)
        copyTime += time.process_time() - copyTimeStart
        
        cube.moveCost = self.moveCost
        cube.totalCost = self.totalCost
        cube.cubeIndices = self.cubeIndices
        
        return cube
        
    def getUp(self):
        return self.takeY(self.cubeSize-1)
    
    def getFront(self):
        return self.takeZ(0)
        
    def getLeft(self):
        return self.takeX(0)
        
    def getRight(self):
        return self.takeX(self.cubeSize-1)
        
    def getBack(self):
        return self.takeZ(self.cubeSize-1)
        
    def getDown(self):
        return self.takeY(0)
        
    def isGameOver(self):
        up_back_left = self.cube[0,0,0]
        down_front_right = self.cube[(self.cubeSize-1),(self.cubeSize-1),(self.cubeSize-1)]
        if not np.all(rubiks_cubie.RubiksCubie_colorUpDown(self.getUp()) == up_back_left.colorUpDown): return False
        if not np.all(rubiks_cubie.RubiksCubie_colorFrontBack(self.getFront()) == down_front_right.colorFrontBack): return False
        if not np.all(rubiks_cubie.RubiksCubie_colorLeftRight(self.getLeft()) == up_back_left.colorLeftRight): return False
        if not np.all(rubiks_cubie.RubiksCubie_colorLeftRight(self.getRight()) == down_front_right.colorLeftRight): return False
        if not np.all(rubiks_cubie.RubiksCubie_colorFrontBack(self.getBack()) == up_back_left.colorFrontBack): return False
        if not np.all(rubiks_cubie.RubiksCubie_colorUpDown(self.getDown()) == down_front_right.colorUpDown): return False
        return True
        
    def toArray(self):
        return np.array([\
            rubiks_cubie.RubiksCubie_colorUpDown(self.getUp()),\
            rubiks_cubie.RubiksCubie_colorFrontBack(self.getFront()),\
            rubiks_cubie.RubiksCubie_colorLeftRight(self.getLeft()),\
            rubiks_cubie.RubiksCubie_colorLeftRight(np.fliplr(self.getRight())),\
            rubiks_cubie.RubiksCubie_colorFrontBack(np.fliplr(self.getBack())),\
            rubiks_cubie.RubiksCubie_colorUpDown(self.getDown())\
        ])
    
    def generateSolvedCube(self):
        cube = np.empty((self.cubeSize, self.cubeSize, self.cubeSize), dtype=rubiks_cubie.RubiksCubie)
        for y in range(self.cubeSize):
            for z in range(self.cubeSize):
                for x in range(self.cubeSize):
                    cube[y,z,x] = rubiks_cubie.RubiksCubie(self, x, (self.cubeSize-1) - y, (self.cubeSize-1) - z, self.cubeSize, random.randint(1,8))
        return cube
        
    def generateCube(self, numMoves):
        self.cube = self.generateSolvedCube()

        costs = rubiks_cubie.RubiksCubie_cost(self.cube)

        actions = []
        validActions = self.validActions()
        for i in range(numMoves):
            action = validActions[random.randint(0,len(validActions)-1)]
            if len(actions) > 0:
                lastAction = self.stringToMove(actions[len(actions)-1])
                # Avoid performing an action on the same index/plane back-to-back.
                while action[0] == lastAction[0] and action[1] == lastAction[1]:
                    action = validActions[random.randint(0,len(validActions)-1)]
            self.rotate(action, False)
            actions.append(self.moveToString(action))
        
        return (actions, costs)
        
    def loadCube(self, moves, costs):
        self.cube = self.generateSolvedCube()
        rubiks_cubie.RubiksCubie_setCost(self.cube, costs)
        for i in range(len(moves)):
            action = self.stringToMove(moves[i])
            self.rotate(action, False)
        
    def takeX(self, index):
        return self.cube.take(index, axis=2)
        
    def takeXIndices(self, index):
        return self.cubeIndices.take(index, axis=2)
        
    def takeY(self, index):
        return self.cube.take((self.cubeSize-1) - index, axis=0)
        
    def takeYIndices(self, index):
        return self.cubeIndices.take((self.cubeSize-1) - index, axis=0)
        
    def takeZ(self, index):
        return self.cube.take((self.cubeSize-1) - index, axis=1)
        
    def takeZIndices(self, index):
        return self.cubeIndices.take((self.cubeSize-1) - index, axis=1)
        
    def takeRowX(self, y, z):
        return self.cube.take((self.cubeSize-1) - y, axis=0).take((self.cubeSize-1) - z, axis=0)
        
    def takeRowY(self, x, z):
        return self.cube.take(x, axis=2).take((self.cubeSize-1) - z, axis=1)
        
    def takeRowZ(self, x, y):
        return self.cube.take(x, axis=2).take((self.cubeSize-1) - y, axis=0)
        
    def rotate(self, index_plane_rotation, updateCost = True):
        index = index_plane_rotation[0]
        plane = index_plane_rotation[1]
        rotation = index_plane_rotation[2]
        
        switch = {
            "X": {
                90: (self.takeX, self.takeXIndices, rubiks_cubie.RubiksCubie_rotateX90, np.rot90, 1),
                180: (self.takeX, self.takeXIndices, rubiks_cubie.RubiksCubie_rotateX180, np.rot90, 2),
                270: (self.takeX, self.takeXIndices, rubiks_cubie.RubiksCubie_rotateX270, np.rot90, 3)
            },
            "Y": {
                90: (self.takeY, self.takeYIndices, rubiks_cubie.RubiksCubie_rotateY90, np.rot90, 1),
                180: (self.takeY, self.takeYIndices, rubiks_cubie.RubiksCubie_rotateY180, np.rot90, 2),
                270: (self.takeY, self.takeYIndices, rubiks_cubie.RubiksCubie_rotateY270, np.rot90, 3)
            },
            "Z": {
                90: (self.takeZ, self.takeZIndices, rubiks_cubie.RubiksCubie_rotateZ90, np.rot90, 1),
                180: (self.takeZ, self.takeZIndices, rubiks_cubie.RubiksCubie_rotateZ180, np.rot90, 2),
                270: (self.takeZ, self.takeZIndices, rubiks_cubie.RubiksCubie_rotateZ270, np.rot90, 3)
            }
        }
        rotSwitch = switch.get(plane)
        if rotSwitch == None:
            raise ValueError("Invalid plane: " + str(plane) + "; Expected (X|Y|Z)")
        funcs = rotSwitch.get(rotation)
        if funcs == None:
            raise ValueError("Invalid rotation: " + str(rotation) + "; Expected (90|180|270)")
        
        takeCubiesFunc = funcs[0]
        takeIndicesFunc = funcs[1]
        elementRotateFunc = funcs[2]
        faceRotateFunc = funcs[3]
        rotationAmount = funcs[4]
        
        cubies = takeCubiesFunc(index)
        indices = takeIndicesFunc(index)
        
        # Move the cubies in the cube array.
        cubies = faceRotateFunc(cubies, rotationAmount)
        # Reassign the cubie current location according to the rotation.
        elementRotateFunc(cubies)
        # Write the cubies back into the cube array.
        self.cube.put(indices, cubies)
        
        # Update cost due to rotation if flag has been set.
        # (Not set when randomizing/loading cube at start of game.)
        if updateCost:
            self.moveCost = rubiks_cubie.RubiksCubie_cost(cubies).sum()
            self.totalCost = self.score(self.moveCost)
            
    def stringToMove(self, string):
        # Check for errors.
        if len(string) < 4:
            raise ValueError("Invalid command.  Expected (0-" + str(self.cubeSize - 1) + ")(X|Y|Z)(90|180|270)")
            
        try:
            index = int(string[0])
        except:
            raise ValueError("Invalid index: '" + cmd[0] + "'; Expected (0-" + str(cubeSize - 1) + ")")
        
        try:
            plane = string[1].upper()
        except:
            raise ValueError("Invalid plane: '" + string[1] + "'; Expected (X|Y|Z)")
        
        try:
            rotation = int(string[2:])
        except:
            raise ValueError("Invalid rotation: '" + string[2:] + "'; Expected (90|180|270)")

        if (index < 0 or index >= self.cubeSize):
            raise ValueError("Invalid index: '" + str(index) + "'; Expected (0-" + str(self.cubeSize-1))
        
        if (plane != "X" and plane != 'Y' and plane != 'Z'):
            raise ValueError("Invalid plane: '" + plane + "'; Expected (X|Y|Z)")
            
        if rotation != 90 and rotation != 180 and rotation != 270:
            raise ValueError("Invalid rotation: '" + str(rotation) + "'; Expected (90|180|270)")
            
        return (index, plane, rotation)
        
    def moveToString(self, index_plane_rotation):
        index = index_plane_rotation[0]
        plane = index_plane_rotation[1]
        rotation = index_plane_rotation[2]
        return str(index) + plane + str(rotation)
            
    def validActions(self):
        validActions = []
        for index in range(0, self.cubeSize):
            for plane in range(0,3):
                for rotation in range(0,3):
                    index_plane_rotation = (index, chr(ord("X") + plane), (rotation + 1) * 90)
                    validActions.append(index_plane_rotation)
        return validActions
    
    def reverseAction(self, action):
        index_plane_rotation = self.stringToMove(action)
        index = index_plane_rotation[0]
        plane = index_plane_rotation[1]
        rotation = index_plane_rotation[2]
        return self.moveToString((index, plane, 360 - rotation))
    
    def reverseActions(self, actions):
        # Reverse list of moves.
        reverse = actions.copy()
        reverse.reverse()
        # For each move, replace with the move which reverses that move.
        for i in range(len(reverse)):
            reverse[i] = self.reverseAction(reverse[i])
        return reverse
        
    def cubieArrayIndex(self, cubie):
        location = cubie.unpackLocation(cubie.currentLocation)
        return (location[0], self.cubeSize-1 - location[1], self.cubeSize-1 - location[2])
        
    def score(self, moveCost):
        prevCost = self.totalCost
        '''
        estimatedCost = 0
        score = 0
        
        xCost = []
        yCost = []
        zCost = []
        for i in range(self.cubeSize):
            xCost.append(rubiks_cubie.RubiksCubie_cost(self.takeX(i)[1]))
            yCost.append(rubiks_cubie.RubiksCubie_cost(self.takeY(i)[1]))
            zCost.append(rubiks_cubie.RubiksCubie_cost(self.takeZ(i)[1]))
        badCubies = np.full(self.cube.shape, 0)
        for y in range(self.cubeSize):
            for z in range(self.cubeSize):
                for x in range(self.cubeSize):
                    temp = 1
        '''
        estimatedCost = 0
        '''
        up = self.getUp()
        down = self.getDown()
        left = self.getLeft()
        right = self.getRight()
        front = self.getFront()
        back = self.getBack()
        goodCubies = np.full(self.cubeSize**3, 1).reshape(self.cubeSize, self.cubeSize, self.cubeSize)
        for i in range(self.cubeSize):
            for j in range(self.cubeSize):
                # For each cubie, compare location and color to determine score.
                for k in range(0, self.cubeSize):
                    if k != j:
                        if (abs(up[i,j].currentLocation - up[i,k].currentLocation) == abs(k-j)*(self.cubeSize**2) and\
                                up[i,j].colorUpDown == up[i,k].colorUpDown):
                            goodCubies[self.cubieArrayIndex(up[i,j])] = 0
                            goodCubies[self.cubieArrayIndex(up[i,k])] = 0
                        if (abs(down[i,j].currentLocation - down[i,k].currentLocation) == abs(k-j)*(self.cubeSize**2) and\
                                down[i,j].colorUpDown == down[i,k].colorUpDown):
                            goodCubies[self.cubieArrayIndex(down[i,j])] = 0
                            goodCubies[self.cubieArrayIndex(down[i,k])] = 0
                        if (abs(left[i,j].currentLocation - left[i,k].currentLocation) == abs(k-j) and\
                                left[i,j].colorLeftRight == left[i,k].colorLeftRight):
                            goodCubies[self.cubieArrayIndex(left[i,j])] = 0
                            goodCubies[self.cubieArrayIndex(left[i,k])] = 0
                        if (abs(right[i,j].currentLocation - right[i,k].currentLocation) == abs(k-j) and\
                                right[i,j].colorLeftRight == right[i,k].colorLeftRight):
                            goodCubies[self.cubieArrayIndex(right[i,j])] = 0
                            goodCubies[self.cubieArrayIndex(right[i,k])] = 0
                        if (abs(front[i,j].currentLocation - front[i,k].currentLocation) == abs(k-j)*(self.cubeSize**2) and\
                                front[i,j].colorFrontBack == front[i,k].colorFrontBack):
                            goodCubies[self.cubieArrayIndex(front[i,j])] = 0
                            goodCubies[self.cubieArrayIndex(front[i,k])] = 0
                        if (abs(back[i,j].currentLocation - back[i,k].currentLocation) == abs(k-j)*(self.cubeSize**2) and\
                                back[i,j].colorFrontBack == back[i,k].colorFrontBack):
                            goodCubies[self.cubieArrayIndex(back[i,j])] = 0
                            goodCubies[self.cubieArrayIndex(back[i,k])] = 0
                    if k != i:
                        if (abs(up[i,j].currentLocation - up[k,j].currentLocation) == abs(k-i) and\
                                up[i,j].colorUpDown == up[k,j].colorUpDown):
                            goodCubies[self.cubieArrayIndex(up[i,j])] = 0
                            goodCubies[self.cubieArrayIndex(up[k,j])] = 0
                        if (abs(down[i,j].currentLocation - down[k,j].currentLocation) == abs(k-i) and\
                                down[i,j].colorUpDown == down[k,j].colorUpDown):
                            goodCubies[self.cubieArrayIndex(down[i,j])] = 0
                            goodCubies[self.cubieArrayIndex(down[k,j])] = 0
                        if (abs(left[i,j].currentLocation - left[k,j].currentLocation) == abs(k-i)*(self.cubeSize) and\
                                left[i,j].colorLeftRight == left[k,j].colorLeftRight):
                            goodCubies[self.cubieArrayIndex(left[i,j])] = 0
                            goodCubies[self.cubieArrayIndex(left[k,j])] = 0
                        if (abs(right[i,j].currentLocation - right[k,j].currentLocation) == abs(k-i)*(self.cubeSize) and\
                                right[i,j].colorLeftRight == right[k,j].colorLeftRight):
                            goodCubies[self.cubieArrayIndex(right[i,j])] = 0
                            goodCubies[self.cubieArrayIndex(right[k,j])] = 0
                        if (abs(front[i,j].currentLocation - front[k,j].currentLocation) == abs(k-i)*(self.cubeSize) and\
                                front[i,j].colorFrontBack == front[k,j].colorFrontBack):
                            goodCubies[self.cubieArrayIndex(front[i,j])] = 0
                            goodCubies[self.cubieArrayIndex(front[k,j])] = 0
                        if (abs(back[i,j].currentLocation - back[k,j].currentLocation) == abs(k-i)*(self.cubeSize) and\
                                back[i,j].colorFrontBack == back[k,j].colorFrontBack):
                            goodCubies[self.cubieArrayIndex(back[i,j])] = 0
                            goodCubies[self.cubieArrayIndex(back[k,j])] = 0
        estimatedCost = (rubiks_cubie.RubiksCubie_cost(self.cube) * goodCubies).sum()
        '''
        '''
        score = 0

        up = self.getUp()
        down = self.getDown()
        left = self.getLeft()
        right = self.getRight()
        front = self.getFront()
        back = self.getBack()
        for i in range(self.cubeSize):
            for j in range(self.cubeSize):
                # For each cubie, compare location and color to determine score.
                for k in range(0, self.cubeSize):
                    if k != j:
                        if (abs(up[i,j].currentLocation - up[i,k].currentLocation) == abs(k-j)*(self.cubeSize**2) and\
                                up[i,j].colorUpDown == up[i,k].colorUpDown):
                            score += self.neighborFactor
                        if (abs(down[i,j].currentLocation - down[i,k].currentLocation) == abs(k-j)*(self.cubeSize**2) and\
                                down[i,j].colorUpDown == down[i,k].colorUpDown):
                            score += self.neighborFactor
                        if (abs(left[i,j].currentLocation - left[i,k].currentLocation) == abs(k-j) and\
                                left[i,j].colorLeftRight == left[i,k].colorLeftRight):
                            score += self.neighborFactor
                        if (abs(right[i,j].currentLocation - right[i,k].currentLocation) == abs(k-j) and\
                                right[i,j].colorLeftRight == right[i,k].colorLeftRight):
                            score += self.neighborFactor
                        if (abs(front[i,j].currentLocation - front[i,k].currentLocation) == abs(k-j)*(self.cubeSize**2) and\
                                front[i,j].colorFrontBack == front[i,k].colorFrontBack):
                            score += self.neighborFactor
                        if (abs(back[i,j].currentLocation - back[i,k].currentLocation) == abs(k-j)*(self.cubeSize**2) and\
                                back[i,j].colorFrontBack == back[i,k].colorFrontBack):
                            score += self.neighborFactor
                    if k != i:
                        if (abs(up[i,j].currentLocation - up[k,j].currentLocation) == abs(k-i) and\
                                up[i,j].colorUpDown == up[k,j].colorUpDown):
                            score += self.neighborFactor
                        if (abs(down[i,j].currentLocation - down[k,j].currentLocation) == abs(k-i) and\
                                down[i,j].colorUpDown == down[k,j].colorUpDown):
                            score += self.neighborFactor
                        if (abs(left[i,j].currentLocation - left[k,j].currentLocation) == abs(k-i)*(self.cubeSize) and\
                                left[i,j].colorLeftRight == left[k,j].colorLeftRight):
                            score += self.neighborFactor
                        if (abs(right[i,j].currentLocation - right[k,j].currentLocation) == abs(k-i)*(self.cubeSize) and\
                                right[i,j].colorLeftRight == right[k,j].colorLeftRight):
                            score += self.neighborFactor
                        if (abs(front[i,j].currentLocation - front[k,j].currentLocation) == abs(k-i)*(self.cubeSize) and\
                                front[i,j].colorFrontBack == front[k,j].colorFrontBack):
                            score += self.neighborFactor
                        if (abs(back[i,j].currentLocation - back[k,j].currentLocation) == abs(k-i)*(self.cubeSize) and\
                                back[i,j].colorFrontBack == back[k,j].colorFrontBack):
                            score += self.neighborFactor
                            
        return score
        '''
        return prevCost + moveCost + estimatedCost