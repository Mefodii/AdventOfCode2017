# --- Day 11: Hex Ed ---
# Crossing the bridge, you've barely reached the other side of the stream when a program comes up to you, clearly in
# distress. "It's my child process," she says, "he's gotten lost in an infinite grid!"
#
# Fortunately for her, you have plenty of experience with infinite grids.
#
# Unfortunately for you, it's a hex grid.
#
# The hexagons ("hexes") in this grid are aligned such that adjacent hexes can be found to the north, northeast,
# southeast, south, southwest, and northwest:
#
#   \ n  /
# nw +--+ ne
#   /    \
# -+      +-
#   \    /
# sw +--+ se
#   / s  \
# You have the path the child process took. Starting where he started, you need to determine the fewest number of steps
# required to reach him. (A "step" means to move from the hex you are in to any adjacent hex.)
#
# For example:
#
#   -   ne,ne,ne is 3 steps away.
#   -   ne,ne,sw,sw is 0 steps away (back where you started).
#   -   ne,ne,s,s is 2 steps away (se,se).
#   -   se,sw,se,sw,sw is 3 steps away (s,s,sw).
#
#######################################################################################################################
# Prepare libs
#######################################################################################################################
import time

#######################################################################################################################
# Functions
#######################################################################################################################
def find_child_process(commands):
    my_coords = {"X": 0, "Y": 0}
    child_coords = follow_path(commands)
    # print(child_coords)

    distance = calculate_hex_distance(my_coords, child_coords)
    # print(distance)

    return distance


def follow_path(commands):
    x = 0
    y = 0

    for command in commands:
        if command == "n":
            y += 1
        elif command == "ne":
            x += 1
        elif command == "nw":
            x -= 1
            y += 1
        elif command == "s":
            y -= 1
        elif command == "se":
            x += 1
            y -= 1
        elif command == "sw":
            x -= 1

    return {"X": x, "Y": y}


def calculate_hex_distance(initial_coords, final_coords):
    dist_x = final_coords.get("X") - initial_coords.get("X")
    dist_y = final_coords.get("Y") - initial_coords.get("Y")
    dist_x_abs = abs(dist_x)
    dist_y_abs = abs(dist_y)

    if dist_y < 0 < dist_x or dist_x < 0 < dist_y:
        distance = min(dist_x_abs, dist_y_abs) + abs(dist_x_abs - dist_y_abs)
    else:
        distance = dist_x_abs + dist_y_abs

    return distance



#######################################################################################################################
# Main function
#######################################################################################################################
def __main__(input_file):
    for input_line in input_file:
        min_distance = find_child_process(input_line.replace("\n",'').split(","))
        print("##--RESULT--##")
        print("Distance to child:", min_distance)

#######################################################################################################################
# Process
#######################################################################################################################
if __name__ == "__main__":
    # Start time of the program
    start = time.time()

    # Input file
    input_file = open('../Input/Day11.txt', 'r')

    # Main functionality
    __main__(input_file)

    # End time of the program
    end = time.time()
    # Running time of the program
    print("Program ran for: ", end - start, "seconds.")


