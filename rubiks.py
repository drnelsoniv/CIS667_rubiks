import sys
import numpy as np
import random
import time
import signal
import math

import rubiks_graphics as grp
import rubiks_cube
import rubiks_cubie
import rubiks_tree
import rubiks_tree_node

cancel = True
def signal_handler(sig, frame):
    global cancel
    if sig == signal.SIGINT:
        if cancel == False:
            print("Cancelling solve...")
            cancel = True
        else:
            cmd = input("Enter 'y' to kill the program (n): ")
            if cmd.lower() == "y":
                exit(1)
    
signal.signal(signal.SIGINT, signal_handler)

'''
def getColorUpDown(element):
    return element.colorUpDown
v_getColorUpDown = np.vectorize(getColorUpDown, otypes=[int])

def getColorFrontBack(element):
    return element.colorFrontBack
v_getColorFrontBack = np.vectorize(getColorFrontBack, otypes=[int])

def getColorLeftRight(element):
    return element.colorLeftRight
v_getColorLeftRight = np.vectorize(getColorLeftRight, otypes=[int])
'''

#cubeSize/numMoves: numIterations
# Note that these are estimates as they represent the number
# of states up to numMoves.  A* may need to search beyond the
# original number of numMoves if it finds a lower-cost path with
# more moves than how many were used to randomize the cube.
#2/4: 4681
#3/2: 757
#3/3: 20440
#4/2: 4161
#5/2: 15751
cubeConfig = {
    0: (2,4),
    1: (3,2),
    2: (3,3),
    3: (4,2),
    4: (5,2)
}

class Rubiks:        
    def __init__(self, cubeSize, numMoves, mode):    
        self.cubeSize = cubeSize
        self.numMoves = numMoves
        # 0 - Manual gameplay
        # 1 - Tree AI
        # 2 - Baseline (Random) AI
        # TODO: Rework this listing.
        self.mode = mode
        # Window width/height in pixels.
        self.winWidth = 600
        self.winHeight = 600
        
        # Using: self.programmedMoves = ['0Y270', '1Z180', '2X180', '2Z180', '1X270', '2Y180', '2Z270']
        # 3//64, 4//88, 5//112 showed good performance.
        self.programmedMoves = []
        self.programmedCosts = np.array([], dtype=int)
        #self.programmedMoves = ['1X270', '0X90', '1X90']
        #self.programmedMoves = ['1X270', '1Y90', '0X180']
        #self.programmedMoves = ['0Y270', '1Z180', '2X180', '2Z180', '1X270', '2Y180', '2Z270']
        #self.neighborFactor = 5
        #self.depthReductionFactor = 112
        self.solveLimit = math.inf
        self.metaSolve = 0
        self.diagnostics = 0
        
        # The current state of the game.
        self.cube = rubiks_cube.RubiksCube(cubeSize)
            
        if len(self.programmedMoves) == 0:
            actualMoves_actualCosts = self.cube.generateCube(numMoves)
            self.actualMoves = actualMoves_actualCosts[0]
            self.actualCosts = actualMoves_actualCosts[1]
        else:
            self.cube.loadCube(self.programmedMoves, self.programmedCosts)
            self.actualMoves = self.programmedMoves
            self.actualCosts = self.programmedCosts
        print("Actual moves: \n" + str(self.actualMoves))
        
        self.tree = rubiks_tree.RubiksTree(self.cube)
        
        # The remaining moves to complete the game, as solved by the AI.
        self.moves = []
        self.optimalCost = math.inf
        
    def copy(self):
        rubiks = Rubiks(self.cubeSize, self.numMoves, self.mode)
        rubiks.cubeSize = self.cubeSize
        rubiks.mode = self.mode
        rubiks.winWidth = self.winWidth
        rubiks.winHeight = self.winHeight
        rubiks.programmedMoves = self.programmedMoves
        rubiks.neighborFactor = self.neighborFactor
        rubiks.depthReductionFactor = self.depthReductionFactor
        rubiks.solveLimit = self.solveLimit
        rubiks.metaSolve = self.metaSolve
        rubiks.diagnostics = self.diagnostics
        rubiks.actualMoves = self.actualMoves
        rubiks.moves = self.moves
        return rubiks
    '''
    def getUp(self, cube):
        return cube.takeY(cube.cubeSize-1)[1]
    def getFront(self, cube):
        return cube.takeZ(0)[1]
    def getLeft(self, cube):
        return cube.takeX(0)[1]
    def getRight(self, cube):
        return cube.takeX(cube.cubeSize-1)[1]
    def getBack(self, cube):
        return cube.takeZ(cube.cubeSize-1)[1]
    def getDown(self, cube):
        return cube.takeY(0)[1]
    def stringToMoveTuple(self, string):
        # Check for errors.
        if len(string) < 4:
            print("Invalid command.  Expected (0-" + str(self.cubeSize - 1) + ")(X|Y|Z)(90|180|270|-90|-180|-270)")
            return None
            
        try:
            index = int(string[0])
        except:
            print("Invalid index: '" + cmd[0] + "'; Expected (0-" + str(cubeSize - 1) + ")")
            return None
        
        try:
            plane = string[1].upper()
        except:
            print("Invalid plane: '" + string[1] + "'; Expected (X|Y|Z)")
            return None
        
        try:
            rotation = int(string[2:])
        except:
            print("Invalid rotation: '" + string[2:] + "'; Expected (90|180|270|-90|-180|-270)")
            return None

        if (index < 0 or index >= self.cubeSize):
            print("Invalid index: '" + str(index) + "'")
            return None
        
        if (plane != "X" and plane != 'Y' and plane != 'Z'):
            print("Invalid plane: '" + plane + "'; Expected (X|Y|Z)")
            return None
            
        if abs(rotation) != 90 and abs(rotation) != 180 and abs(rotation) != 270:
            print("Invalid rotation: '" + str(rotation) + "'; Expected (90|180|270|-90|-180|-270)")
            return None
            
        return (index, plane, rotation)
        
    def moveTupleToString(self, moveTuple):
        return str(moveTuple[0]) + moveTuple[1] + str(moveTuple[2])
        
    def reverseMoves(self, moveList):
        reverse = []
        # Reverse list of moves.
        for i in range(len(moveList)):
            reverse.append(moveList[(len(moveList)-1)-i])
        # For each move, replace with the move which reverses that move.
        for i in range(len(reverse)):
            moveTuple = self.stringToMoveTuple(reverse[i])
            reverse[i] = self.moveTupleToString((moveTuple[0], moveTuple[1], 360 - moveTuple[2]))
        return reverse
    '''
    '''
        prev_cube = cube.copy()
        
        self.rotate(index, plane, rotation)
        
        # Determine new cost based on which cubies moved.
        prev_cube = prev_cube - cube
        #print("Cube diff:")
        #print(prev_cube)
        #print("Cost identity matrix:")
        #print(to_cost_identity(prev_cube))
        
        cost = (cube_cost_cubieCost[2] * to_cost_identity(prev_cube)).sum()
        print("Cost: " + str(cost))
        
        # Any non-zero values include colors which have changed.
        #for i in range(prev_cube.shape[0]):
        #    for j in range(prev_cube.shape[1]):
        #        for k in range(prev_cube.shape[2]):
        #            if prev_cube[i][j][k] != 0:
                        
        
        # TODO: Need to rotate cost array.
        # TODO: Need to produce mapping between prev_cube and cost array.
        # For each cubie in cost array, if any value in prev_cube mapping to that cubie is not 0, include that cost.
        # Only include the cost once for each cubie.
    '''
    # 6, 36, 1634 iterations
    # 8, 36, 2718 iterations
    # 6, 24, 2247 iterations
    '''
    def score(self, cube, moves):
        if (cube.shape[1] % 2 == 0):
            score = -4
        else:
            score = 0
        for i in range(0, cube.shape[0]):
            for j in range(0, cube.shape[1]):
                for k in range(0, cube.shape[2]):
                    if (cube.shape[1] % 2 == 0):
                        # Even, need to check against center 4-cubie.
                        score = -4
                    else:
                        # Odd, check against center cubie.
                        #if cube[i][j][k] == cube[i][int(cube.shape[1] / 2)][int(cube.shape[2] / 2)]:
                        #    score = score + 1
                        if j > 0:
                            if cube[i][j][k] == cube[i][j-1][k]:
                                score = score + 6
                        if j < cube.shape[1] - 1:
                            if cube[i][j][k] == cube[i][j+1][k]:
                                score = score + 6
                        if k > 0:
                            if cube[i][j][k] == cube[i][j][k-1]:
                                score = score + 6
                        if k < cube.shape[2] - 1:
                            if cube[i][j][k] == cube[i][j][k+1]:
                                score = score + 6
        score = score - (48 * len(moves))
        return score
    '''
    
    '''
    def score_face(self, cube, faceIndex):
        numCubies = cube.shape[1]
        colorScore = np.array([0,0,0,0,0,0])
        if numCubies % 2 == 0:
            colorScore[cube[faceIndex][int(numCubies/2)-1][int(numCubies/2)-1]] += 1
            colorScore[cube[faceIndex][int(numCubies/2)-1][int(numCubies/2)]] += 1
            colorScore[cube[faceIndex][int(numCubies/2)][int(numCubies/2)-1]] += 1
            colorScore[cube[faceIndex][int(numCubies/2)][int(numCubies/2)]] += 1
            # Prefer matching center colors.
            colorScore = colorScore**2
        else:
            colorScore[int(cube[faceIndex][int(numCubies/2)][int(numCubies/2)])] += 1
        
        score = 0
        # Increase score if matching center cubie.
        for i in range(numCubies):
            for j in range(numCubies):
                score += colorScore[int(cube[faceIndex][i][j])]
        # Increase score for matching along row.
        for i in range(numCubies):
            rowScore = np.array([0,0,0,0,0,0])
            for j in range(numCubies):
                rowScore[int(cube[faceIndex][i][j])] += 1
            rowScore = rowScore ** 2
            score += rowScore.sum()
        # Increase score for matching along column.
        for i in range(numCubies):
            columnScore = np.array([0,0,0,0,0,0])
            for j in range(numCubies):
                columnScore[int(cube[faceIndex][j][i])] += 1
            columnScore = columnScore ** 2
            score += columnScore.sum()
                
        return score
        
    def score(self, cube, moves, index, plane):
        score = 0
        
        if plane == "X":
            # Check Top/Front/Down/Back
            score += self.score_face(cube, 0)
            score += self.score_face(cube, 1)
            score += self.score_face(cube, 5)
            score += self.score_face(cube, 4)
        elif plane == "Y":
            # Check Front/Right/Back/Left
            score += self.score_face(cube, 1)
            score += self.score_face(cube, 3)
            score += self.score_face(cube, 4)
            score += self.score_face(cube, 2)
        else: # plane == "Z"
            # Check Top/Right/Down/Left
            score += self.score_face(cube, 0)
            score += self.score_face(cube, 3)
            score += self.score_face(cube, 5)
            score += self.score_face(cube, 2)
        
        # Since we may end up investigating a local maximum with little chance
        # to solve the cube, decrease the score over time to allow the
        # algorithm to investigate other branches.
        # Adjusting this "too low" causes local maxima to be explored.
        # Adjusting this "too high" reduces the solve to performing
        # breadth-first search, where additional depth is much more expensive
        # then simply exploring the current depth.
        #
        # Example data:
        # Given a cube randomized with:
        # ['1Y180', '0Y270', '0Z270', '1X270', '2Z270']
        # (5 moves)
        # | Depth-reduction factor  |   Number of Iterations    |
        # |            4            |           8162            |
        # |            8            |             67            |
        # |           12            |             32            |
        # |           16            |             19            |
        # |           20            |             15            |
        # |           24            |             39            |
        # |           28            |             68            |
        # |           32            |            146            |
        score -= (8 * len(moves))
            
        return score
    '''

    # TODO: Search space is huge.  Figure out how to increase performance.
    '''
    def solve(self):
        count = 0
        startTime = time.process_time()
        visited = []
        search = [((self.cube, self.totalCost, self.cubieCost, 0), [])]
        min_cost = float('inf')
        
        # For now, get a state from search.
        # In the future, get the state from search with the maximum score.
        while len(search) > 0:
            count = count + 1
            if count % 100 == 0:
                print("count: " + str(count) + ", time: " + str(time.process_time() - startTime))
                startTime = time.process_time()
            cube_cost_cubieCost_score = search[0][0]
            index = 0
            for i in range(1, len(search)):
                if search[i][0][3] > cube_cost_cubieCost_score[3]:
                    cube_cost_cubieCost_score = search[i][0]
                    index = i
            moves = search[index][1]
            search.pop(index)
            
            #if (len(moves) > 3):
            #    return None
            
            if (self.is_game_over(cube_cost_cubieCost_score[0])):
                print("Solved in " + str(count) + " iterations...")
                return moves
            
            visited = visited + [cube_cost_cubieCost_score]
            
            cube = cube_cost_cubieCost_score[0]
            totalCost = cube_cost_cubieCost_score[1]
            cubieCost = cube_cost_cubieCost_score[2]
            for index in range(0, cube.shape[1]):
                for plane in range(0,3):
                    for rotation in range(0,3):
                        new_cube = cube.copy()
                        
                        self.rotate(new_cube, index, chr(ord("X") + plane), (rotation + 1) * 90)
                        move = str(index) + chr(ord("X") + plane) + str((rotation + 1) * 90)
                        
                        new_totalCost = totalCost
                        new_cubieCost = cubieCost.copy()
                        new_score = self.score(new_cube, moves + [move], index, chr(ord("X") + plane))

                        found = False
                        for visited_tuple in visited:
                            visited_cube = visited_tuple[0]
                            if np.all(visited_cube == new_cube):
                                found = True
                        
                        if not found:
                            #print("new_score: " + str(new_score) + ", Trying\n" + str(moves + [move]) + "\n")
                            search = search + [((new_cube, new_totalCost, new_cubieCost, new_score), moves + [move])]
    '''
    def scoreCube(self, cube, numMoves):      
        '''
        # This is testing if the colors along a given row/column match.
        # Alternatively, check if cubie x/y/z are close (off by at most 1 in a single dimension).
        neighborScore = cube.score()

        depthScore = -(self.depthReductionFactor*(numMoves+1))
        
        #print("Neighbor: " + str(neighborScore) + ", Depth-reduction: " + str(depthReductionFactor))
        scoreArray = np.array([neighborScore, depthScore])
        return (scoreArray.sum(), scoreArray)
        '''
        score = cube.score()
        return (score, score)
    
    def sortByScore(self, element):
        return element[1]
        
    def solve(self):
        global cancel
        
        count = 0
        timeStart = time.process_time()
        
        timeLoop = 0
        timeSearch = 0
        timeGameOver = 0
        
        # Use CTRL-C to cancel the solve function.
        cancel = False
        node = self.tree.root
        timeIterations = time.process_time()
        minCost = math.inf
        while node.cube.isGameOver() == False:
            timeLoopStart = time.process_time()
            if cancel or count > self.solveLimit:
                actions = []
                break
            count += 1
                
            if count % 100 == 0:
                print("count: " + str(count) + ", time: " + str(time.process_time() - timeIterations))
                timeIterations = time.process_time()
            
            timeSearchStart = time.process_time()
            node = self.tree.next()
            if minCost < node.minCost:
                print("Solved in " + str(count) + " iterations...")
                break
                
            if self.diagnostics >= 2:
                print("Investigating: Cost: " + str(node.minCost))
            timeSearch += time.process_time() - timeSearchStart
            
            timeGameOverStart = time.process_time()
            if (node.cube.isGameOver()):
                # This represents a cost-limit to prune the size of the A* search tree after
                # a solution has been found.
                if node.minCost < minCost:
                    minCost = node.cube.totalCost
                    actions = self.tree.getActions(node)
                    print("Solution found in " + str(count) + " iterations...pruning tree using cost of " + str(minCost))
                    
            timeGameOver += time.process_time() - timeGameOverStart
            
            timeLoop += time.process_time() - timeLoopStart
        
        statsArray = None
        
        if self.diagnostics >= 1:
            timeTotal = time.process_time() - timeStart
            print("Loop: " + str(timeLoop))
            print("  Search: " + str(timeSearch))
            print("  Game Over: " + str(timeGameOver))
            print("Total time: " + str(timeTotal))
            print(rubiks_tree_node.visitTime)
            print(rubiks_tree_node.copyTime)
            print(rubiks_tree_node.treenodeCtorTime)
            print(rubiks_cube.copyTime)
        
            '''
            # Produce report of which nodes were visited.
            logVisited = open("visited.log", "w")
            for i in range(len(allVisited)):
                logVisited.write(str(allVisited[i][0][1]) + "(" + str(allVisited[i][0][2]) + "): " + str(allVisited[i][0][3]) + "\n")
                logVisited.write("    " + str(allVisited[i][1]) + "\n")
            logVisited.close()
            '''
            
            # Produce stats of success
            '''
            solutionMoves = self.cube.reverseActions(self.actualMoves)
            totalMoves = np.full((len(solutionMoves)), 0)
            correctMoves = np.full((len(solutionMoves)), 0)
            for i in range(len(allVisited)):
                visitedMoves = allVisited[i][0][3]
                for moveIndex in range(len(visitedMoves)):
                    if moveIndex < len(solutionMoves):
                        totalMoves[moveIndex] += 1
                        if visitedMoves[moveIndex] == solutionMoves[moveIndex]:
                            correctMoves[moveIndex] += 1
                        else:
                            break
                    else:
                        break
            
            print("STATS:")
            print("Total moves: " + str(totalMoves[0]))
            stats = open("stats.log", "w")
            statsArray = np.full((len(solutionMoves)), 0.)
            for i in range(len(correctMoves)):
                divisor = totalMoves[i]
                if divisor == 0: divisor = 1
                print(str(correctMoves[i]) + " / " + str(divisor) + " = " + str(correctMoves[i]/divisor))
                stats.write(str(correctMoves[i]/divisor) + "\n")
                statsArray[i] = correctMoves[i]/divisor
            stats.close()
            '''

        return (actions, minCost, statsArray)
        
    def statsSort(self, element):
        return element[2].sum()
    '''    
    def autoSolve(self):
        global cancel
        cancel = False
        statsList = []
        for neighbor in range(1,6,1):
            for depthReduct in range(8,136,8):
                factors = (neighbor, depthReduct)
                print("----------------------------------------")
                rubiks = self.copy()
                rubiks.solveLimit = 1000
                rubiks.neighborFactor = neighbor
                # Rubiks contains a copy of the original neighbor factor when the cube was
                # first created.  Override that here with the specified loop iteration var.
                rubiks.cube.neighborFactor = neighbor
                rubiks.depthReductionFactor = depthReduct
                solveTuple = rubiks.solve()
                moves = solveTuple[0]
                stats = solveTuple[1]
                statsList.append((factors, moves, stats))
                print("Factors:\n" + str(factors) + "\nMoves:\n" + str(moves) + "\nStats:\n" + str(stats))
                if (cancel): break
            if (cancel): break
            

        statsList.sort(key=self.statsSort, reverse=True)
        autoSolveFile = open("autoSolve.log", "w")
        autoSolveFile.write("Actual Moves:\n" + str(self.actualMoves) + "\n")
        for i in range(len(statsList)):
            autoSolveFile.write("----------------------------------------\n")
            autoSolveFile.write("Factors:\n" + str(statsList[i][0]) + "\n")
            autoSolveFile.write("Moves:\n" + str(statsList[i][1]) + "\n")
            autoSolveFile.write("Stats:\n" + str(statsList[i][2]) + "\n")
        autoSolveFile.close()
    '''
    
def exit_failure(error_msg):
    print(error_msg)
    exit(-1)
    
# Main function
def main():
    config = None
    while config == None:
        print("Enter the rubiks cube game configuration option:")
        for i in range(5):
            config = cubeConfig.get(i)
            print(str(i) + ": Cube size " + str(config[0]) + "; Randomized moves " + str(config[1]))
        strConfig = input("> ")
        try:
            config = cubeConfig.get(int(strConfig))
        except:
            config = None
        if config != None:
            cubeSize = config[0]
            numMoves = config[1]
        else:
            print("Invalid option: " + strConfig)
    '''
    print("Enter the size of the cube (3-7; default is 3)")
    #cubeSize = input("> ")
    cubeSize = 3
    
    if cubeSize == "":
        # Use 3 as the default cube size if no size is specified.
        cubeSize = 3
    else:
        try:
            cubeSize = int(cubeSize)
        except:
            # Failed to convert cubeSize to int.
            exit_failure("cube size was not an integer.")

    if cubeSize < 3 or cubeSize > 7:
        # Cube size not between 3-7.
        exit_failure("cube size outside valid range.")
    '''
    print("Enter mode (0-1; default is 0 - Manual gameplay):")
    print("0 - Manual gameplay")
    print("1 - Tree-based AI")
    mode = input("> ")
    #mode = 1
    
    if mode == "":
        mode = 0
    else:
        try:
            mode = int(mode)
        except:
            exit_failure("mode was not an integer.")
    
    if mode < 0 or mode > 1: #mode > 2:
        exit_failure("mode was outside valid range.")
    
    rubiks = Rubiks(cubeSize, numMoves, mode)
    
    '''
    if rubiks.metaSolve == 1:
        rubiks.autoSolve()
        print("Auto-solve completed.")
        exit(0)
    '''
    
    if mode == 1:
        moves_cost_stats = rubiks.solve()
        rubiks.moves = moves_cost_stats[0]
        if len(rubiks.moves) == 0:
            # Solve failed, boot up in manual mode.
            rubiks.mode = 0
        else:
            rubiks.optimalCost = moves_cost_stats[1]
            print("Optimal Cost: " + str(rubiks.optimalCost))
    
    # Create window for graphical cube.
    rubiks_grp = grp.RubiksGraphics()
    rubiks_grp.create_win(rubiks.cubeSize, rubiks.winWidth, rubiks.winHeight)

    while (True):        
        # Draw cube/print state.
        rubiks_grp.draw_cube(rubiks.cube.toArray())
            
        print("State:")
        print("In order: Up, Front, Left, Right, Back, Down");
        print(str(rubiks.cube.toArray()))
        print("Cubie Cost:\n" + str(rubiks_cubie.RubiksCubie_cost(rubiks.cube.cube)))
        #print("Cost per cubie:")
        #print(rubiks_cubie.RubiksCubie_cost(rubiks.cube))
        
        if rubiks.mode == 1:
            print("Moves remaining: " + str(rubiks.moves))
        
        print("Total Cost: " + str(rubiks.cube.totalCost))
        
        # Test if game is over.
        if rubiks.cube.isGameOver():
            print("Cube solved!")
            break
        
        print("Actual moves:\n" + str(rubiks.actualMoves))
        print("[Solution]:\n" + str(rubiks.cube.reverseActions(rubiks.actualMoves)))
        # Wait for user input.
        if rubiks.mode == 1:
            if rubiks.moves != None and len(rubiks.moves) > 0:
                cmd = input("Move (q to quit, enter for '" + rubiks.moves[0] + "'): ")
                if cmd == "":
                    cmd = rubiks.moves.pop(0)
                    try:
                        move = rubiks.cube.stringToMove(cmd)
                        rubiks.cube.rotate(move)
                    except:
                        print(str(valueError))
                elif cmd.lower() == "q":
                    break
            else:
                cmd = input("Solve failed; press enter to continue.")
        else:
            cmd = input("Move (q to quit): ")
            if cmd.lower() == "q":
                break
            try:
                move = rubiks.cube.stringToMove(cmd)
                rubiks.cube.rotate(move)
            except ValueError as valueError:
                print(str(valueError))

if __name__ == "__main__":
    main()