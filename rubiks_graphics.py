
import numpy as np
import graphics as grp

class RubiksGraphics:
    def __init__(self):
        self.num_cubies = 0
        self.cubie_width = 64
        self.cubie_angle_width = 20
        self.win = None
        self.front = None
        self.left = None
        self.top = None
        self.top_margin = self.cubie_width
        self.left_margin = self.cubie_width
        self.bottom_margin = self.cubie_width
        self.right_margin = self.cubie_width
    
    def color_to_str(self, color_val):
        switch = {
            0: "white",
            1: "red",
            2: "blue",
            3: "green",
            4: "orange",
            5: "yellow"
        }
        return switch.get(int(color_val))


    def create_win(self, num_cubies, width, height):
        self.num_cubies = num_cubies
        
        self.win = grp.GraphWin("Rubik's Cube", width, height)
        # Set the coordinates such that the cube allows for one cubie_width's space on the left
        # and top sides. 
        self.win.setCoords(0, 0, self.left_margin + (self.num_cubies * (self.cubie_width + self.cubie_angle_width)) + self.right_margin,\
            self.bottom_margin + (self.num_cubies * (self.cubie_width + self.cubie_angle_width)) + self.top_margin)
        self.front = np.full((num_cubies, num_cubies), grp.Polygon())
        self.left = np.full((num_cubies, num_cubies), grp.Polygon())
        self.top = np.full((num_cubies, num_cubies), grp.Polygon())

    def draw_cubie_front(self, x, y, z, color):
        self.front[x][y].undraw()
        x_lower_left = self.left_margin + (self.num_cubies * self.cubie_angle_width) + (x * self.cubie_width) - (z * self.cubie_angle_width)
        y_lower_left = self.bottom_margin + (y * self.cubie_width) + (z * self.cubie_angle_width)
        self.front[x][y] = grp.Polygon(\
        grp.Point(x_lower_left, y_lower_left), \
        grp.Point(x_lower_left + self.cubie_width, y_lower_left), \
        grp.Point(x_lower_left + self.cubie_width, y_lower_left + self.cubie_width), \
        grp.Point(x_lower_left, y_lower_left + self.cubie_width))
        self.front[x][y].setFill(color)
        self.front[x][y].draw(self.win)

    def draw_cubie_left(self, x, y, z, color):
        self.left[y][z].undraw()
        x_lower_right = self.left_margin + (self.num_cubies * self.cubie_angle_width) + (x * self.cubie_width) - (z * self.cubie_angle_width)
        y_lower_right = self.bottom_margin + (y * self.cubie_width) + (z * self.cubie_angle_width)
        self.left[y][z] = grp.Polygon(\
        grp.Point(x_lower_right, y_lower_right), \
        grp.Point(x_lower_right, y_lower_right + self.cubie_width), \
        grp.Point(x_lower_right - self.cubie_angle_width, y_lower_right + self.cubie_width + self.cubie_angle_width), \
        grp.Point(x_lower_right - self.cubie_angle_width, y_lower_right + self.cubie_angle_width))
        self.left[y][z].setFill(color)
        self.left[y][z].draw(self.win)
        
    def draw_cubie_top(self, x, y, z, color):
        self.top[x][z].undraw()
        x_lower_left = self.left_margin + (self.num_cubies * self.cubie_angle_width) + (x * self.cubie_width) - (z * self.cubie_angle_width)
        y_lower_left = self.bottom_margin + ((y + 1) * self.cubie_width) + (z * self.cubie_angle_width)
        self.top[x][z] = grp.Polygon(\
        grp.Point(x_lower_left, y_lower_left), \
        grp.Point(x_lower_left + self.cubie_width, y_lower_left), \
        grp.Point(x_lower_left + self.cubie_width - self.cubie_angle_width, y_lower_left + self.cubie_angle_width), \
        grp.Point(x_lower_left - self.cubie_angle_width, y_lower_left + self.cubie_angle_width))
        self.top[x][z].setFill(color)
        self.top[x][z].draw(self.win)
        
    def draw_cube(self, cube):
        try:
            cube_size = cube.shape[1]
            for i in range(0, cube_size):
                for j in range(0, cube_size):
                    self.draw_cubie_front(i, j, 0, self.color_to_str(cube[1][cube_size - 1 - j][i]))
                    self.draw_cubie_left(0, i, j, self.color_to_str(cube[2][cube_size - 1 - i][cube_size - 1 - j]))
                    self.draw_cubie_top(i, cube_size - 1, j, self.color_to_str(cube[0][cube_size - 1 - j][i]))
        except:
            # TODO: Log?
            print("Failed to draw cube.")


    
