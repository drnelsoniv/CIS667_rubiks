import sys
import rubiks

def exit_failure(error_msg):
    print(error_msg)
    print("Usage: " + sys.argv[0] + " [cube_size (3-7; defaults to 3)]")
    exit(-1)

# Use 3 as the default cube size if no size is specified.
cube_size = 3

# Main function
if len(sys.argv) == 2:
    try:
        cube_size = int(sys.argv[1])
    except:
        # Failed to convert cube_size to int.
        exit_failure("cube_size was not an integer.")
elif len(sys.argv) >= 3:
    # Too many arguments specified.
    exit_failure("Too many arguments specified.")

if cube_size < 3 or cube_size > 7:
    # Cube size not between 3-7.
    exit_failure("cube_size outside valid range.")

# Run program.
print("Cube size: " + str(cube_size))
cost_cube_cubieCost = rubiks.generate_cube(cube_size)

while (True):
    print("Cost: " + str(cost_cube_cubieCost[0]))
    print("State:")
    print("In order: Up, Front, Left, Right, Back, Down");
    print(cost_cube_cubieCost[1])
    print("Cost per cubie:")
    print(cost_cube_cubieCost[2])
    cmd = input("Move (q to quit): ")
    if cmd.lower() == "q":
        break
    rubiks.parse_cmd(cost_cube_cubieCost, cmd)

