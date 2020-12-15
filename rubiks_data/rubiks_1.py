rubiks_1 = rubiks.Rubiks(3,1,1)
rubiks_1.cubeSize = 3
rubiks_1.numMoves = 2
rubiks_1.mode = 1
rubiks_1.programmedMoves = ['0Y90', '1X270']
rubiks_1.programmedCosts = np.array([[[5,6,7],[8,8,5],[2,5,2]],[[8,3,7],[8,7,7],[7,1,1]],[[2,7,3],[3,6,2],[3,1,2]]])
rubiks_1.solveLimit = math.inf
rubiks_1.metaSolve = 0
rubiks_1.diagnostics = 0
rubiks_1.mode = 1
rubiks_1.cube = rubiks_cube.RubiksCube(rubiks_1.cubeSize)
rubiks_1.cube.loadCube(rubiks_1.programmedMoves,rubiks_1.programmedCosts)
rubiks_1.actualMoves = ['0Y90', '1X270']
rubiks_1.actualCosts = np.array([[[5,6,7],[8,8,5],[2,5,2]],[[8,3,7],[8,7,7],[7,1,1]],[[2,7,3],[3,6,2],[3,1,2]]])
rubiks_1_optimalMoves = ['1X90', '0Y270']
rubiks_1_optimalCost = 75
