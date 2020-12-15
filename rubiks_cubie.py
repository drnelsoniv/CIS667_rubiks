
import numpy as np
import math

class RubiksCubie:
    def __init__(self, cube, x, y, z, cubeSize, cost):
        self.cube = cube
        self.currentLocation = x*(cubeSize**2) + y*cubeSize + z
        self.initialLocation = x*(cubeSize**2) + y*cubeSize + z
        if y == (cubeSize-1):
            self.colorUpDown = 0
        elif y == 0:
            self.colorUpDown = 5
        else:
            self.colorUpDown = None
        if z == 0:
            self.colorFrontBack = 1
        elif z == (cubeSize-1):
            self.colorFrontBack = 4
        else:
            self.colorFrontBack = None
        if x == 0:
            self.colorLeftRight = 2
        elif x == (cubeSize-1):
            self.colorLeftRight = 3
        else:
            self.colorLeftRight = None
        self.cubeSize = cubeSize
        self.cost = cost
        
    def __str__(self):
        return str(self.currentLocation) + " " + str(self.unpackLocation(self.currentLocation)) + ": Up/Down: " + str(self.colorUpDown) + ", Left/Right: " + str(self.colorLeftRight) + ", Front/Back: " + str(self.colorFrontBack)
        
    def copy(self):
        cubie = RubiksCubie(0, 0, 0, 0, 0, 0)
        cubie.cube = self.cube
        cubie.currentLocation = self.currentLocation
        cubie.initialLocation = self.initialLocation
        cubie.colorUpDown = self.colorUpDown
        cubie.colorFrontBack = self.colorFrontBack
        cubie.colorLeftRight = self.colorLeftRight
        cubie.cubeSize = self.cubeSize
        cubie.cost = self.cost
        return cubie
        
    def initialLocation(self):
        return self.initialLocation
        
    def currentLocation(self):
        return self.currentLocation
        
    def packLocation(self, x_y_z):
        return x_y_z[0]*(self.cubeSize**2) + x_y_z[1]*(self.cubeSize) + x_y_z[2]
        
    def unpackLocation(self, location):
        return ((location // (self.cubeSize**2)) % self.cubeSize,\
            (location // self.cubeSize) % self.cubeSize,\
            location % self.cubeSize)
            
    def rotateX90(self):
        (x,y,z) = self.unpackLocation(self.currentLocation)
        self.currentLocation = (x)*(self.cubeSize**2) + ((self.cubeSize-1) - z)*self.cubeSize + (y)
            
        tempFrontBack = self.colorFrontBack
        self.colorFrontBack = self.colorUpDown
        self.colorUpDown = tempFrontBack
        
    def rotateX180(self):
        (x,y,z) = self.unpackLocation(self.currentLocation)
        self.currentLocation = (x)*(self.cubeSize**2) + ((self.cubeSize-1) - y)*self.cubeSize + ((self.cubeSize-1) - z)
        
    def rotateX270(self):
        x = self.currentLocation // (self.cubeSize**2) % self.cubeSize
        y = self.currentLocation // self.cubeSize % self.cubeSize
        z = self.currentLocation % self.cubeSize
        self.currentLocation = (x)*(self.cubeSize**2) + (z)*self.cubeSize + ((self.cubeSize-1) - y)
        
        tempFrontBack = self.colorFrontBack
        self.colorFrontBack = self.colorUpDown
        self.colorUpDown = tempFrontBack
       
    def rotateY90(self):
        x = self.currentLocation // (self.cubeSize**2) % self.cubeSize
        y = self.currentLocation // self.cubeSize % self.cubeSize
        z = self.currentLocation % self.cubeSize
        self.currentLocation = ((self.cubeSize-1) - z)*(self.cubeSize**2) + (y)*self.cubeSize + (x)
        
        tempFrontBack = self.colorFrontBack
        self.colorFrontBack = self.colorLeftRight
        self.colorLeftRight = tempFrontBack
        
    def rotateY180(self):
        x = self.currentLocation // (self.cubeSize**2) % self.cubeSize
        y = self.currentLocation // self.cubeSize % self.cubeSize
        z = self.currentLocation % self.cubeSize
        self.currentLocation = ((self.cubeSize-1) - x)*(self.cubeSize**2) + (y)*self.cubeSize + ((self.cubeSize-1) - z)
        
    def rotateY270(self):
        x = self.currentLocation // (self.cubeSize**2) % self.cubeSize
        y = self.currentLocation // self.cubeSize % self.cubeSize
        z = self.currentLocation % self.cubeSize
        self.currentLocation = (z)*(self.cubeSize**2) + (y)*self.cubeSize + ((self.cubeSize-1) - x)
        
        tempFrontBack = self.colorFrontBack
        self.colorFrontBack = self.colorLeftRight
        self.colorLeftRight = tempFrontBack
        
    def rotateZ90(self):
        x = self.currentLocation // (self.cubeSize**2) % self.cubeSize
        y = self.currentLocation // self.cubeSize % self.cubeSize
        z = self.currentLocation % self.cubeSize
        self.currentLocation = ((self.cubeSize-1) - y)*(self.cubeSize**2) + (x)*self.cubeSize + (z)
        
        tempUpDown = self.colorUpDown
        self.colorUpDown = self.colorLeftRight
        self.colorLeftRight = tempUpDown
        
    def rotateZ180(self):
        x = self.currentLocation // (self.cubeSize**2) % self.cubeSize
        y = self.currentLocation // self.cubeSize % self.cubeSize
        z = self.currentLocation % self.cubeSize
        self.currentLocation = ((self.cubeSize-1) - x)*(self.cubeSize**2) + ((self.cubeSize-1) - y)*self.cubeSize + (z)
        
    def rotateZ270(self):
        x = self.currentLocation // (self.cubeSize**2) % self.cubeSize
        y = self.currentLocation // self.cubeSize % self.cubeSize
        z = self.currentLocation % self.cubeSize
        self.currentLocation = (y)*(self.cubeSize**2) + ((self.cubeSize-1) - x)*self.cubeSize + (z)
        
        tempUpDown = self.colorUpDown
        self.colorUpDown = self.colorLeftRight
        self.colorLeftRight = tempUpDown
        
def RubiksCubie_v_copy(element):
    return element.copy()
        
def RubiksCubie_v_rotateX90(element):
    element.rotateX90()
    
def RubiksCubie_v_rotateX180(element):
    element.rotateX180()
    
def RubiksCubie_v_rotateX270(element):
    element.rotateX270()
    
def RubiksCubie_v_rotateY90(element):
    element.rotateY90()
    
def RubiksCubie_v_rotateY180(element):
    element.rotateY180()
        
def RubiksCubie_v_rotateY270(element):
    element.rotateY270()
    
def RubiksCubie_v_rotateZ90(element):
    element.rotateZ90()
    
def RubiksCubie_v_rotateZ180(element):
    element.rotateZ180()
    
def RubiksCubie_v_rotateZ270(element):
    element.rotateZ270()
    
def RubiksCubie_v_colorUpDown(element):
    return element.colorUpDown
    
def RubiksCubie_v_colorFrontBack(element):
    return element.colorFrontBack
    
def RubiksCubie_v_colorLeftRight(element):
    return element.colorLeftRight
    
def RubiksCubie_v_currentLocation(element):
    return element.currentLocation
    
def RubiksCubie_v_str(element):
    return str(element)
    
def RubiksCubie_v_cost(element):
    return element.cost
    
def RubiksCubie_v_setCost(element, cost):
    element.cost = cost
    return cost

# Note: If you do not specify an output type here (otypes), then the function will
# execute on the first element twice. (the first time is to determine the output
# type of the function, the second is part of the actual vectorized call...)
# https://numpy.org/doc/stable/reference/generated/numpy.vectorize.html
# This is odd.  In any case, ALWAYS specify the output type to avoid this.
RubiksCubie_copy = np.vectorize(RubiksCubie_v_copy, otypes=[RubiksCubie])
RubiksCubie_rotateX90 = np.vectorize(RubiksCubie_v_rotateX90, otypes=[RubiksCubie])
RubiksCubie_rotateX180 = np.vectorize(RubiksCubie_v_rotateX180, otypes=[RubiksCubie])
RubiksCubie_rotateX270 = np.vectorize(RubiksCubie_v_rotateX270, otypes=[RubiksCubie])
RubiksCubie_rotateY90 = np.vectorize(RubiksCubie_v_rotateY90, otypes=[RubiksCubie])
RubiksCubie_rotateY180 = np.vectorize(RubiksCubie_v_rotateY180, otypes=[RubiksCubie])
RubiksCubie_rotateY270 = np.vectorize(RubiksCubie_v_rotateY270, otypes=[RubiksCubie])
RubiksCubie_rotateZ90 = np.vectorize(RubiksCubie_v_rotateZ90, otypes=[RubiksCubie])
RubiksCubie_rotateZ180 = np.vectorize(RubiksCubie_v_rotateZ180, otypes=[RubiksCubie])
RubiksCubie_rotateZ270 = np.vectorize(RubiksCubie_v_rotateZ270, otypes=[RubiksCubie])
RubiksCubie_colorUpDown = np.vectorize(RubiksCubie_v_colorUpDown, otypes=[int])
RubiksCubie_colorFrontBack = np.vectorize(RubiksCubie_v_colorFrontBack, otypes=[int])
RubiksCubie_colorLeftRight = np.vectorize(RubiksCubie_v_colorLeftRight, otypes=[int])
RubiksCubie_currentLocation = np.vectorize(RubiksCubie_v_currentLocation, otypes=[int])
RubiksCubie_str = np.vectorize(RubiksCubie_v_str, otypes=[str])
RubiksCubie_cost = np.vectorize(RubiksCubie_v_cost, otypes=[int])
RubiksCubie_setCost = np.vectorize(RubiksCubie_v_setCost, otypes=[int])

