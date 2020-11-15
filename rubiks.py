import sys
import numpy as np
import random
import copy
import rubiks_graphics as grp

color_white = 0
color_red = 1
color_blue = 2
color_green = 3
color_orange = 4
color_yellow = 5

'''
Rotates the cube so that the specified plane is now aligned with
the Y-plane, so a rotation can take place via rotate_y_90().
'''
def rotate_cube(cube, plane):
    if plane == "X":
        # Rotate cube counter-clockwise 90 degrees as viewed from the front.
        temp = copy.deepcopy(cube[0])
        cube[0] = np.rot90(cube[3])
        cube[3] = np.rot90(cube[5])
        cube[5] = np.rot90(cube[2])
        cube[2] = np.rot90(temp)
        
        cube[1] = np.rot90(cube[1])
        cube[4] = np.rot90(cube[4], 3)
    if plane == "Y": return
    if plane == "Z":
        # Rotate cube down 90 degrees as viewed from the front.
        temp = copy.deepcopy(cube[1])
        cube[1] = cube[0]
        cube[0] = np.rot90(cube[4], 2)
        cube[4] = np.rot90(cube[5], 2)
        cube[5] = temp
        
        cube[2] = np.rot90(cube[2], 3)
        cube[3] = np.rot90(cube[3])
    
        # Rotate cube right 90 degrees as viewed from the front.
        temp = copy.deepcopy(cube[1])
        cube[1] = cube[2]
        cube[2] = cube[4]
        cube[4] = cube[3]
        cube[3] = temp
        
        cube[0] = np.rot90(cube[0])
        cube[5] = np.rot90(cube[5], 3)
    
'''
This function rotates a cube aligned for Y-plane rotations back into
the specified plane, restoring the cube faces to their proper locations.
'''
def unrotate_cube(cube, plane):
    if plane == "X":
        # Rotate cube clockwise 90 degrees as viewed from the front.
        cube[4] = np.rot90(cube[4])
        cube[1] = np.rot90(cube[1], 3)
        
        temp = copy.deepcopy(cube[0])
        cube[0] = np.rot90(cube[2], 3)
        cube[2] = np.rot90(cube[5], 3)
        cube[5] = np.rot90(cube[3], 3)
        cube[3] = np.rot90(temp, 3)
    if plane == "Y": return
    if plane == "Z":
        # Rotate cube left 90 degrees as viewed from the front.
        cube[5] = np.rot90(cube[5])
        cube[0] = np.rot90(cube[0], 3)
        
        temp = copy.deepcopy(cube[1])
        cube[1] = cube[3]
        cube[3] = cube[4]
        cube[4] = cube[2]
        cube[2] = temp
        
        # Rotate cube up 90 degrees as viewed from the front.
        cube[3] = np.rot90(cube[3], 3)
        cube[2] = np.rot90(cube[2])
        
        temp = copy.deepcopy(cube[1])
        cube[1] = cube[5]
        cube[5] = np.rot90(cube[4], 2)
        cube[4] = np.rot90(cube[0], 2)
        cube[0] = temp
        
def rotate_y_90(cube, index):
    num_cubies = cube.shape[1]
    # Array stores 0 in top array, while commands treat 0
    # as the bottom array.
    yIndex = num_cubies - 1 - index
    temp = copy.deepcopy(cube[1][yIndex])
    cube[1][yIndex] = cube[2][yIndex]
    cube[2][yIndex] = cube[4][yIndex]
    cube[4][yIndex] = cube[3][yIndex]
    cube[3][yIndex] = temp
    if index == 0:
        # Rotate bottom
        cube[5] = np.rot90(cube[5], 3)
    elif index == num_cubies - 1:
        # Rotate top
        cube[0] = np.rot90(cube[0])
        
def rotate(cube, index, plane, rotation):
    # Rotate the cube so that the move "appears" to be a y-plane move.
    rotate_cube(cube, plane)
    if rotation < 0:
        rotation = rotation + 360
    while rotation > 0:
        rotate_y_90(cube, index)
        rotation = rotation - 90
    # Restore the cube to it's original orientation at the start of this function.
    unrotate_cube(cube, plane)

'''
This function generates a solved cube, where all sides are unique colors
and all sides only contain a single color.
@param cube_size The number of cubies along an edge of the cube.
@return tuple
    cube - [6,cube_size,cube_size] of ints representing cubie colors.
'''    
def generate_solved_cube(cube_size):
    cube = np.empty((6, cube_size, cube_size))
    for i in range(cube.shape[0]):
        cube[i] = i
    return cube

'''
This function generates a cube.
@param cube_size The number of cubies along an edge of the cube.
@return tuple
    cube - [6,cube_size,cube_size] of ints representing cubie colors
    total_cost - 0 at time of cube creation
    cubie_cost - [cube_size,cube_size,cube_size] of ints representing
                 costs to move cubie at that coordinate.
'''
def generate_cube(cube_size):
    # TODO: Allow the user to specify a cube.
    # For now, generate a solved cube then randomize it by making random moves.
    cube = generate_solved_cube(cube_size)
    
    # TODO: Allow user to specify number of random moves.
    num_moves = 2
    for _ in range(0, num_moves):
        index = random.randint(0, cube_size - 1)
        plane = chr(ord("X") + random.randint(0, 2))
        rotation = (random.randint(0,2) + 1) * 90
        rotate(cube, index, plane, rotation)
    
    # TODO: Allow the user to specify min/max random cost per cubie.
    cubie_cost = np.empty((cube_size, cube_size, cube_size))
    for i in range(cubie_cost.shape[0]):
        for j in range(cubie_cost.shape[1]):
            for k in range(cubie_cost.shape[2]):
                cubie_cost[i][j][k] = random.randint(0, 20)
                
    return (cube,0,cubie_cost)
    
def is_game_over(cube):
    for i in range(0, cube.shape[0]):
        color = cube[i][0][0]
        for j in range(0, cube.shape[1]):
            for k in range(0, cube.shape[2]):
                if (cube[i][j][k] != color):
                    return False
    return True

def parse_cmd(cube_cost_cubieCost, cmd):
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
    cube = cube_cost_cubieCost[0]
    cube_size = cube.shape[1]
    if len(cmd) < 4:
        print("Invalid command.  Expected (0-" + str(cube_size - 1) + ")(X|Y|Z)(90|180|270|-90|-180|-270)")
        return cube_cost_cubieCost
        
    try:
        index = int(cmd[0])
    except:
        print("Invalid index: '" + cmd[0] + "'; Expected (0-" + str(cube_size - 1) + ")")
        return cube_cost_cubieCost
    
    try:
        plane = cmd[1].upper()
    except:
        print("Invalid plane: '" + cmd[1] + "'; Expected (X|Y|Z)")
        return cube_cost_cubieCost
    
    try:
        rotation = int(cmd[2:])
    except:
        print("Invalid rotation: '" + cmd[2:] + "'; Expected (90|180|270|-90|-180|-270)")
        return cube_cost_cubieCost

    if (index < 0 or index >= cube_size):
        print("Invalid index: '" + str(index) + "'")
        return cube_cost_cubieCost
    
    if (plane != "X" and plane != 'Y' and plane != 'Z'):
        print("Invalid plane: '" + plane + "'; Expected (X|Y|Z)")
        return cube_cost_cubieCost
        
    if abs(rotation) != 90 and abs(rotation) != 180 and abs(rotation) != 270:
        print("Invalid rotation: '" + str(rotation) + "'; Expected (90|180|270|-90|-180|-270)")
        return cube_cost_cubieCost
    
    prev_cube = copy.deepcopy(cube)
    
    rotate(cube, index, plane, rotation)
    
    # Determine new cost based on which cubies moved.
    prev_cube = prev_cube - cube
    print("Cube diff:")
    print(prev_cube)
    
    # Any non-zero values include colors which have changed.
    #for i in range(prev_cube.shape[0]):
    #    for j in range(prev_cube.shape[1]):
    #        for k in range(prev_cube.shape[2]):
    #            if prev_cube[i][j][k] != 0:
                    
    
    # TODO: Need to rotate cost array.
    # TODO: Need to producing mapping between prev_cube and cost array.
    # For each cubie in cost array, if any value in prev_cube mapping to that cubie is not 0, include that cost.
    # Only include the cost once for each cubie.
    
def exit_failure(error_msg):
    print(error_msg)
    exit(-1)

# Use 3 as the default cube size if no size is specified.
g_cube_size = 3
g_mode = 0

# Window width/height in pixels.
g_winWidth = 600
g_winHeight = 600

# TODO: Search space is huge.  Figure out how to increase performance.
def solve(cube_cost_cubieCost):
    visited = []
    search = [(cube_cost_cubieCost, [])]
    
    # For now, get a state from search.
    # In the future, get the state from search with the minimum cost.
    while len(search) > 0:
        search_tuple = search.pop(0)
        cube_cost_cubieCost = search_tuple[0]
        moves = search_tuple[1]
        
        if (is_game_over(cube_cost_cubieCost[0])):
            return moves
        
        visited = visited + [cube_cost_cubieCost]
        
        cube = cube_cost_cubieCost[0]
        for index in range(0, cube.shape[1]):
            for plane in range(0,3):
                for rotation in range(0,3):
                    new_cube_cost_cubieCost = copy.deepcopy(cube_cost_cubieCost)
                    new_cube = new_cube_cost_cubieCost[0]
                    
                    rotate(new_cube, index, chr(ord("X") + plane), (rotation + 1) * 90)

                    found = False
                    for visited_tuple in visited:
                        visited_cube = visited_tuple[0]
                        if np.all(visited_cube == new_cube):
                            found = True
                    
                    if not found:
                        move = str(index) + chr(ord("X") + plane) + str((rotation + 1) * 90)
                        search = search + [(new_cube_cost_cubieCost, moves + [move])]            

# Main function    
def main():
    global g_cube_size
    print("Enter the size of the cube (3-7; default is 3)")
    cube_size = input(">")
    if cube_size != "":
        try:
            g_cube_size = int(cube_size)
        except:
            # Failed to convert cube_size to int.
            exit_failure("cube size was not an integer.")

    if g_cube_size < 3 or g_cube_size > 7:
        # Cube size not between 3-7.
        exit_failure("cube size outside valid range.")

    print("Cube size: " + str(g_cube_size))
    
    global g_mode
    print("Enter mode (0-1; default is 0):")
    print("0 - Manual gameplay")
    print("1 - Tree-based AI")
    #print("2 - Baseline (random) AI")
    mode = input(">")
    if mode != "":
        try:
            g_mode = int(mode)
        except:
            exit_failure("mode was not an integer.")
    
    if g_mode < 0 or g_mode > 1: #g_mode > 2:
        exit_failure("mode was outside valid range.")
    
    cube_cost_cubieCost = generate_cube(g_cube_size)
    
    if g_mode != 0:
        moves = solve(cube_cost_cubieCost)
    
    # Create window for graphical cube.
    grp.createWin(g_cube_size, g_winWidth, g_winHeight)

    while (True):
        cube = cube_cost_cubieCost[0]
        cost = cube_cost_cubieCost[1]
        cubieCost = cube_cost_cubieCost[2]
        
        # Draw cube/print state.
        grp.drawCube(cube)
        print("State:")
        print("In order: Up, Front, Left, Right, Back, Down");
        print(cube)
        print("Cost: " + str(cost))
        print("Cost per cubie:")
        print(cubieCost)
        
        if g_mode == 1:
            print("Moves: " + str(moves))
        
        # Test if game is over.
        if is_game_over(cube):
            print("Cube solved!")
            break
            
        # Wait for user input.
        if g_mode == 1:
            cmd = input("Move (q to quit, enter for '" + moves[0] + "'): ")
            if cmd == "":
                cmd = moves.pop(0)
                parse_cmd(cube_cost_cubieCost, cmd)
            elif cmd.lower() == "q":
                break
        else:
            cmd = input("Move (q to quit): ")
            if cmd.lower() == "q":
                break
            parse_cmd(cube_cost_cubieCost, cmd)

if __name__ == "__main__":
    main()