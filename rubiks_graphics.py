
import numpy as np
import graphics as grp

g_win = None
g_num_cubies = 3
g_front = [[grp.Polygon(grp.Point(0,0), grp.Point(0,0), grp.Point(0,0)) for _ in range(0,g_num_cubies)]\
    for _ in range(0,g_num_cubies)]
g_left = [[grp.Polygon(grp.Point(0,0), grp.Point(0,0), grp.Point(0,0)) for _ in range(0,g_num_cubies)]\
    for _ in range(0,g_num_cubies)]
g_top = [[grp.Polygon(grp.Point(0,0), grp.Point(0,0), grp.Point(0,0)) for _ in range(0,g_num_cubies)]\
    for _ in range(0,g_num_cubies)]
g_cubie_width = 64
g_cubie_angle_width = 20
g_top_margin = g_cubie_width
g_left_margin = g_cubie_width
g_bottom_margin = g_cubie_width
g_right_margin = g_cubie_width

def toColor(color_val):
    switch = {
        0: "white",
        1: "red",
        2: "blue",
        3: "green",
        4: "orange",
        5: "yellow"
    }
    return switch.get(int(color_val))

def createWin(num_cubies, width, height):
    global g_win
    global g_num_cubies
    global g_front
    global g_left
    global g_top
    g_win = grp.GraphWin("Rubik's Cube", width, height)
    # Set the coordinates such that the cube allows for one cubie_width's space on the left
    # and top sides. 
    g_win.setCoords(0, 0, g_left_margin + (num_cubies * (g_cubie_width + g_cubie_angle_width)) + g_right_margin,\
        g_bottom_margin + (num_cubies * (g_cubie_width + g_cubie_angle_width)) + g_top_margin)
    g_num_cubies = num_cubies
    g_front = [[grp.Polygon(grp.Point(0,0), grp.Point(0,0), grp.Point(0,0)) for _ in range(0,num_cubies)] for _ in range(0,num_cubies)]
    g_left = [[grp.Polygon(grp.Point(0,0), grp.Point(0,0), grp.Point(0,0)) for _ in range(0,num_cubies)] for _ in range(0,num_cubies)]
    g_top = [[grp.Polygon(grp.Point(0,0), grp.Point(0,0), grp.Point(0,0)) for _ in range(0,num_cubies)] for _ in range(0,num_cubies)]

def drawCubieFront(x, y, z, color):
    global g_front
    g_front[x][y].undraw()
    x_lower_left = g_left_margin + (g_num_cubies * g_cubie_angle_width) + (x * g_cubie_width) - (z * g_cubie_angle_width)
    y_lower_left = g_bottom_margin + (y * g_cubie_width) + (z * g_cubie_angle_width)
    g_front[x][y] = grp.Polygon(\
    grp.Point(x_lower_left, y_lower_left), \
    grp.Point(x_lower_left + g_cubie_width, y_lower_left), \
    grp.Point(x_lower_left + g_cubie_width, y_lower_left + g_cubie_width), \
    grp.Point(x_lower_left, y_lower_left + g_cubie_width))
    g_front[x][y].setFill(color)
    g_front[x][y].draw(g_win)

def drawCubieLeft(x, y, z, color):
    global g_left
    g_left[y][z].undraw()
    x_lower_right = g_left_margin + (g_num_cubies * g_cubie_angle_width) + (x * g_cubie_width) - (z * g_cubie_angle_width)
    y_lower_right = g_bottom_margin + (y * g_cubie_width) + (z * g_cubie_angle_width)
    g_left[y][z] = grp.Polygon(\
    grp.Point(x_lower_right, y_lower_right), \
    grp.Point(x_lower_right, y_lower_right + g_cubie_width), \
    grp.Point(x_lower_right - g_cubie_angle_width, y_lower_right + g_cubie_width + g_cubie_angle_width), \
    grp.Point(x_lower_right - g_cubie_angle_width, y_lower_right + g_cubie_angle_width))
    g_left[y][z].setFill(color)
    g_left[y][z].draw(g_win)
    
def drawCubieTop(x, y, z, color):
    global g_top
    g_top[x][z].undraw()
    x_lower_left = g_left_margin + (g_num_cubies * g_cubie_angle_width) + (x * g_cubie_width) - (z * g_cubie_angle_width)
    y_lower_left = g_bottom_margin + ((y + 1) * g_cubie_width) + (z * g_cubie_angle_width)
    g_top[x][z] = grp.Polygon(\
    grp.Point(x_lower_left, y_lower_left), \
    grp.Point(x_lower_left + g_cubie_width, y_lower_left), \
    grp.Point(x_lower_left + g_cubie_width - g_cubie_angle_width, y_lower_left + g_cubie_angle_width), \
    grp.Point(x_lower_left - g_cubie_angle_width, y_lower_left + g_cubie_angle_width))
    g_top[x][z].setFill(color)
    g_top[x][z].draw(g_win)
    
def drawCube(cube):
    cube_size = cube.shape[1]
    for i in range(0, cube_size):
        for j in range(0, cube_size):
            drawCubieFront(i, j, 0, toColor(cube[1][cube_size - 1 - j][i]))
            drawCubieLeft(0, i, j, toColor(cube[2][cube_size - 1 - i][cube_size - 1 - j]))
            drawCubieTop(i, cube_size - 1, j, toColor(cube[0][cube_size - 1 - j][i]))


    
