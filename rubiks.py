import sys
import numpy as np
import random
import copy

color_white = 0
color_red = 1
color_blue = 2
color_green = 3
color_orange = 4
color_yellow = 5

def generate_solved_cube(cube_size):
    cube = np.empty((6, cube_size, cube_size))
    # Fill the cube with a statically instanced cube for now.
    # TODO: Allow the user to specify a cube, or generate a random valid cube.
    for i in range(cube.shape[0]):
        cube[i] = i
    return cube

def generate_cube(cube_size):
    # Fill the cube with a statically instanced cube for now.
    # TODO: Allow the user to specify a cube, or generate a random valid cube.
    cube = generate_solved_cube(cube_size)
    
    #names = ["U", "F", "L", "R", "B", "D"]
    #for i in range(cube.shape[0]):
    #    for j in range(cube.shape[1]):
    #        for k in range(cube.shape[2]):
    #            if (i == 0):
    #                cube[i][j][k] = names[i] + str(j*k + 1)
    
    # TODO: Allow the user to specify min/max random cost per cubie.
    cubie_cost = np.empty((cube_size, cube_size, cube_size))
    for i in range(cubie_cost.shape[0]):
        for j in range(cubie_cost.shape[1]):
            for k in range(cubie_cost.shape[2]):
                cubie_cost[i][j][k] = random.randint(0, 20)
                
    return (0, cube, cubie_cost)

def parse_cmd(cost_cube_cubieCost, cmd):
    # Commands will be of the form:
    # (Index)(Row/Column)(Rotation)
    # where:
    # Index - The numeric index of the row/column to rotate.
    # Rows are top-to-bottom starting from 0.
    # Columns are left-to-right starting from 0.
    # Row/Column - The type of the rotation, along a row (R) or along a column (C).
    # Rotation - A rotation amount, in degrees.
    # Expected values are 90, 180, or 270 to rotate right-to-left (for rows) or
    # top-to-bottom (for columns) when viewing from the front.
    #  Alternatively, specify -90, -180, -270 to rotate left-to-right (for rows) or
    # bottom-to-top (for columns) when viewing from the front.
    
    # TODO: Make command processing more robust.
    
    # Check for errors.
    cube_size = (cost_cube_cubieCost[1]).shape[1]
    if len(cmd) < 4:
        print("Invalid command.  Expected (0-" + str(cube_size - 1) + ")(R|C)(90|180|270|-90|-180|-270)")
        return cost_cube_cubieCost
        
    try:
        index = int(cmd[0])
    except:
        print("Invalid index: '" + cmd[0] + "'; Expected (0-" + str(cube_size - 1) + ")")
        return cost_cube_cubieCost
    
    try:
        row_column = cmd[1].upper()
    except:
        print("Invalid row/column indicator: '" + cmd[1] + "'; Expected (R|C)")
        return cost_cube_cubieCost
    
    try:
        rotation = int(cmd[2:])
    except:
        print("Invalid rotation: '" + cmd[2:] + "'; Expected (90|180|270|-90|-180|-270)")
        return cost_cube_cubieCost

    if (index < 0 or index >= cube_size):
        print("Invalid index: '" + str(index) + "'")
        return cost_cube_cubieCost
    
    if (row_column != "R" and row_column != 'C'):
        print("Invalid row/column indicator: '" + cmd[1] + "'; Expected (R|C)")
        return cost_cube_cubieCost
        
    if abs(rotation) != 90 and abs(rotation) != 180 and abs(rotation) != 270:
        print("Invalid rotation: '" + str(rotation) + "'; Expected (90|180|270|-90|-180|-270)")
        return cost_cube_cubieCost
    
    # Perform action.
    if rotation < 0:
        rotation = rotation + 360
    prev_cube = copy.deepcopy(cost_cube_cubieCost[1])
    while rotation > 0:
        if (row_column == "R"):
            rotate_row_90(index, cost_cube_cubieCost)
        else:
            rotate_col_90(index, cost_cube_cubieCost)
        rotation = rotation - 90
    
    # Determine new cost based on which cubies moved.
    prev_cube = prev_cube - cost_cube_cubieCost[1]
    # Any non-zero values include colors which have changed.
    #for i in range(prev_cube.shape[0]):
    #    for j in range(prev_cube.shape[1]):
    #        for k in range(prev_cube.shape[2]):
    #            if prev_cube[i][j][k] != 0:
                    
    
    # TODO: Need to rotate cost array.
    # TODO: Need to producing mapping between prev_cube and cost array.
    # For each cubie in cost array, if any value in prev_cube mapping to that cubie is not 0, include that cost.
    # Only include the cost once for each cubie.
 
# Rotate right-to-left when viewing from front.
def rotate_row_90(index, cost_cube_cubieCost):
    # Rotate faces orthogonal to axis of rotation.
    # Define a temporary storage array.
    front_row = copy.deepcopy(cost_cube_cubieCost[1][1][index])
    # Right-to-front
    cost_cube_cubieCost[1][1][index] = cost_cube_cubieCost[1][3][index]
    # Back-to-right
    cost_cube_cubieCost[1][3][index] = cost_cube_cubieCost[1][4][index]
    # Left-to-back
    cost_cube_cubieCost[1][4][index] = cost_cube_cubieCost[1][2][index]
    # Front-to-left
    cost_cube_cubieCost[1][2][index] = front_row
    # If working with first/last index, rotate the face associated with that row as well.
    if index == 0:
        cost_cube_cubieCost[1][0] = np.rot90(cost_cube_cubieCost[1][0], 3)
    elif index == cost_cube_cubieCost[1].shape[1] - 1:
        cost_cube_cubieCost[1][5] = np.rot90(cost_cube_cubieCost[1][5])
    return cost_cube_cubieCost

# Rotate top-to-bottom when viewing from front.
def rotate_col_90(index, cost_cube_cubieCost):
    # Rotate faces orthogonal to axis of rotation.
    # Define a temporary storage array.
    cube_copy = copy.deepcopy(cost_cube_cubieCost[1])
    for i in range(cost_cube_cubieCost[1].shape[1]):
        # Top-to-front
        cost_cube_cubieCost[1][1][i][index] = cube_copy[0][i][index]
        # Back-to-top
        cost_cube_cubieCost[1][0][i][index] = cube_copy[4][(cost_cube_cubieCost[1].shape[1] - 1) - i][index]
        # Bottom-to-back
        cost_cube_cubieCost[1][4][i][index] = cube_copy[5][(cost_cube_cubieCost[1].shape[1] - 1) - i][index]
        # Front-to-bottom
        cost_cube_cubieCost[1][5][i][index] = cube_copy[1][i][index]
    # If working with first/last index, rotate the face associated with that row as well.
    if index == 0:
        cost_cube_cubieCost[1][2] = np.rot90(cost_cube_cubieCost[1][2], 3)
    elif index == index == cost_cube_cubieCost[1].shape[1] - 1:
        cost_cube_cubieCost[1][3] = np.rot90(cost_cube_cubieCost[1][3])
    
    return cost_cube_cubieCost
