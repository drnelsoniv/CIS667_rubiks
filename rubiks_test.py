
import numpy as np
import rubiks
import unittest as ut

def printCubes(actualCube, expectedCube):
    print("\nActual cube:")
    print(actualCube)
    print("Expected cube:")
    print(expectedCube)

class RubiksTestCase(ut.TestCase):
    def test_0x90(self):        
        expectedCube = np.array(\
          [[[44,  1,  2],\
            [41,  4,  5],\
            [38,  7,  8]],\
           [[ 0, 10, 11],\
            [ 3, 13, 14],\
            [ 6, 16, 17]],\
           [[24, 21, 18],\
            [25, 22, 19],\
            [26, 23, 20]],\
           [[27, 28, 29],\
            [30, 31, 32],\
            [33, 34, 35]],\
           [[36, 37, 51],\
            [39, 40, 48],\
            [42, 43, 45]],\
           [[ 9, 46, 47],\
            [12, 49, 50],\
            [15, 52, 53]]]\
        )
        cube = np.array([i for i in range(0, 6*3*3)])
        cube = cube.reshape(6,3,3)
        rubiks.rotate(cube, 0, "X", 90)
        equal = np.all(cube == expectedCube)
        if not equal:
            printCubes(cube, expectedCube)
        self.assertTrue(equal)

    def test_1x90(self):
        expectedCube = np.array(\
          [[[ 0, 43,  2],\
            [ 3, 40,  5],\
            [ 6, 37,  8]],\
           [[ 9,  1, 11],\
            [12,  4, 14],\
            [15,  7, 17]],\
           [[18, 19, 20],\
            [21, 22, 23],\
            [24, 25, 26]],\
           [[27, 28, 29],\
            [30, 31, 32],\
            [33, 34, 35]],\
           [[36, 52, 38],\
            [39, 49, 41],\
            [42, 46, 44]],\
           [[45, 10, 47],\
            [48, 13, 50],\
            [51, 16, 53]]]\
        )
        cube = np.array([i for i in range(0, 6*3*3)])
        cube = cube.reshape(6,3,3)
        rubiks.rotate(cube, 1, "X", 90)
        equal = np.all(cube == expectedCube)
        if not equal:
            printCubes(cube, expectedCube)
        self.assertTrue(equal)
        
    def test_2x90(self):
        expectedCube = np.array(\
          [[[ 0,  1, 42],\
            [ 3,  4, 39],\
            [ 6,  7, 36]],\
           [[ 9, 10,  2],\
            [12, 13,  5],\
            [15, 16,  8]],\
           [[18, 19, 20],\
            [21, 22, 23],\
            [24, 25, 26]],\
           [[29, 32, 35],\
            [28, 31, 34],\
            [27, 30, 33]],\
           [[53, 37, 38],\
            [50, 40, 41],\
            [47, 43, 44]],\
           [[45, 46, 11],\
            [48, 49, 14],\
            [51, 52, 17]]]\
        )
        cube = np.array([i for i in range(0, 6*3*3)])
        cube = cube.reshape(6,3,3)
        rubiks.rotate(cube, 2, "X", 90)
        equal = np.all(cube == expectedCube)
        if not equal:
            printCubes(cube, expectedCube)
        self.assertTrue(equal)
        
    def test_0y90(self):
        expectedCube = np.array(\
          [[[ 0,  1,  2],\
            [ 3,  4,  5],\
            [ 6,  7,  8]],\
           [[ 9, 10, 11],\
            [12, 13, 14],\
            [24, 25, 26]],\
           [[18, 19, 20],\
            [21, 22, 23],\
            [42, 43, 44]],\
           [[27, 28, 29],\
            [30, 31, 32],\
            [15, 16, 17]],\
           [[36, 37, 38],\
            [39, 40, 41],\
            [33, 34, 35]],\
           [[51, 48, 45],\
            [52, 49, 46],\
            [53, 50, 47]]]\
        )
        cube = np.array([i for i in range(0, 6*3*3)])
        cube = cube.reshape(6,3,3)
        rubiks.rotate(cube, 0, "Y", 90)
        equal = np.all(cube == expectedCube)
        if not equal:
            printCubes(cube, expectedCube)
        self.assertTrue(equal)
        
    def test_1y90(self):
        expectedCube = np.array(\
          [[[ 0,  1,  2],\
            [ 3,  4,  5],\
            [ 6,  7,  8]],\
           [[ 9, 10, 11],\
            [21, 22, 23],\
            [15, 16, 17]],\
           [[18, 19, 20],\
            [39, 40, 41],\
            [24, 25, 26]],\
           [[27, 28, 29],\
            [12, 13, 14],\
            [33, 34, 35]],\
           [[36, 37, 38],\
            [30, 31, 32],\
            [42, 43, 44]],\
           [[45, 46, 47],\
            [48, 49, 50],\
            [51, 52, 53]]]\
        )
        cube = np.array([i for i in range(0, 6*3*3)])
        cube = cube.reshape(6,3,3)
        rubiks.rotate(cube, 1, "Y", 90)
        equal = np.all(cube == expectedCube)
        if not equal:
            printCubes(cube, expectedCube)
        self.assertTrue(equal)
        
    def test_2y90(self):
        expectedCube = np.array(\
          [[[ 2,  5,  8],\
            [ 1,  4,  7],\
            [ 0,  3,  6]],\
           [[18, 19, 20],\
            [12, 13, 14],\
            [15, 16, 17]],\
           [[36, 37, 38],\
            [21, 22, 23],\
            [24, 25, 26]],\
           [[ 9, 10, 11],\
            [30, 31, 32],\
            [33, 34, 35]],\
           [[27, 28, 29],\
            [39, 40, 41],\
            [42, 43, 44]],\
           [[45, 46, 47],\
            [48, 49, 50],\
            [51, 52, 53]]]\
        )
        cube = np.array([i for i in range(0, 6*3*3)])
        cube = cube.reshape(6,3,3)
        rubiks.rotate(cube, 2, "Y", 90)
        equal = np.all(cube == expectedCube)
        if not equal:
            printCubes(cube, expectedCube)
        self.assertTrue(equal)
        
    def test_0z90(self):
        expectedCube = np.array(\
          [[[ 0,  1,  2],\
            [ 3,  4,  5],\
            [26, 23, 20]],\
           [[15, 12,  9],\
            [16, 13, 10],\
            [17, 14, 11]],\
           [[18, 19, 45],\
            [21, 22, 46],\
            [24, 25, 47]],\
           [[ 6, 28, 29],\
            [ 7, 31, 32],\
            [ 8, 34, 35]],\
           [[36, 37, 38],\
            [39, 40, 41],\
            [42, 43, 44]],\
           [[33, 30, 27],\
            [48, 49, 50],\
            [51, 52, 53]]]\
        )
        cube = np.array([i for i in range(0, 6*3*3)])
        cube = cube.reshape(6,3,3)
        rubiks.rotate(cube, 0, "Z", 90)
        equal = np.all(cube == expectedCube)
        if not equal:
            printCubes(cube, expectedCube)
        self.assertTrue(equal)
        
    def test_1z90(self):
        expectedCube = np.array(\
          [[[ 0,  1,  2],\
            [25, 22, 19],\
            [ 6,  7,  8]],\
           [[ 9, 10, 11],\
            [12, 13, 14],\
            [15, 16, 17]],\
           [[18, 48, 20],\
            [21, 49, 23],\
            [24, 50, 26]],\
           [[27,  3, 29],\
            [30,  4, 32],\
            [33,  5, 35]],\
           [[36, 37, 38],\
            [39, 40, 41],\
            [42, 43, 44]],\
           [[45, 46, 47],\
            [34, 31, 28],\
            [51, 52, 53]]]\
        )
        cube = np.array([i for i in range(0, 6*3*3)])
        cube = cube.reshape(6,3,3)
        rubiks.rotate(cube, 1, "Z", 90)
        equal = np.all(cube == expectedCube)
        if not equal:
            printCubes(cube, expectedCube)
        self.assertTrue(equal)
        
    def test_2z90(self):
        expectedCube = np.array(\
          [[[24, 21, 18],\
            [ 3,  4,  5],\
            [ 6,  7,  8]],\
           [[ 9, 10, 11],\
            [12, 13, 14],\
            [15, 16, 17]],\
           [[51, 19, 20],\
            [52, 22, 23],\
            [53, 25, 26]],\
           [[27, 28,  0],\
            [30, 31,  1],\
            [33, 34,  2]],\
           [[38, 41, 44],\
            [37, 40, 43],\
            [36, 39, 42]],\
           [[45, 46, 47],\
            [48, 49, 50],\
            [35, 32, 29]]]\
        )
        cube = np.array([i for i in range(0, 6*3*3)])
        cube = cube.reshape(6,3,3)
        rubiks.rotate(cube, 2, "Z", 90)
        equal = np.all(cube == expectedCube)
        if not equal:
            printCubes(cube, expectedCube)
        self.assertTrue(equal)
        
if __name__ == "__main__":    
    
    test_suite = ut.TestLoader().loadTestsFromTestCase(RubiksTestCase)
    res = ut.TextTestRunner(verbosity=2).run(test_suite)
    num, errs, fails = res.testsRun, len(res.errors), len(res.failures)
    print("score: %d of %d (%d errors, %d failures)" % (num - (errs+fails), num, errs, fails))