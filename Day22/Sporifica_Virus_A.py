# --- Day 22: Sporifica Virus ---
# Diagnostics indicate that the local grid computing cluster has been contaminated with the Sporifica Virus. The grid
# computing cluster is a seemingly-infinite two-dimensional grid of compute nodes. Each node is either clean or infected
# by the virus.
#
# To prevent overloading the nodes (which would render them useless to the virus) or detection by system administrators,
# exactly one virus carrier moves through the network, infecting or cleaning nodes as it moves. The virus carrier is
# always located on a single node in the network (the current node) and keeps track of the direction it is facing.
#
# To avoid detection, the virus carrier works in bursts; in each burst, it wakes up, does some work, and goes back to
# sleep. The following steps are all executed in order one time each burst:
#
#   -   If the current node is infected, it turns to its right. Otherwise, it turns to its left. (Turning is done
# in-place; the current node does not change.)
#   -   If the current node is clean, it becomes infected. Otherwise, it becomes cleaned. (This is done after the node
# is considered for the purposes of changing direction.)
#   -   The virus carrier moves forward one node in the direction it is facing.
#
# Diagnostics have also provided a map of the node infection status (your puzzle input). Clean nodes are shown as .;
# infected nodes are shown as #. This map only shows the center of the grid; there are many more nodes beyond those
# shown, but none of them are currently infected.
#
# The virus carrier begins in the middle of the map facing up.
#
# For example, suppose you are given a map like this:
#
# ..#
# #..
# ...
# Then, the middle of the infinite grid looks like this, with the virus carrier's position marked with [ ]:
#
# . . . . . . . . .
# . . . . . . . . .
# . . . . . . . . .
# . . . . . # . . .
# . . . #[.]. . . .
# . . . . . . . . .
# . . . . . . . . .
# . . . . . . . . .
# The virus carrier is on a clean node, so it turns left, infects the node, and moves left:
#
# . . . . . . . . .
# . . . . . . . . .
# . . . . . . . . .
# . . . . . # . . .
# . . .[#]# . . . .
# . . . . . . . . .
# . . . . . . . . .
# . . . . . . . . .
# The virus carrier is on an infected node, so it turns right, cleans the node, and moves up:
#
# . . . . . . . . .
# . . . . . . . . .
# . . . . . . . . .
# . . .[.]. # . . .
# . . . . # . . . .
# . . . . . . . . .
# . . . . . . . . .
# . . . . . . . . .
# Four times in a row, the virus carrier finds a clean, infects it, turns left, and moves forward, ending in the same
# place and still facing up:
#
# . . . . . . . . .
# . . . . . . . . .
# . . . . . . . . .
# . . #[#]. # . . .
# . . # # # . . . .
# . . . . . . . . .
# . . . . . . . . .
# . . . . . . . . .
# Now on the same node as before, it sees an infection, which causes it to turn right, clean the node, and move forward:
#
# . . . . . . . . .
# . . . . . . . . .
# . . . . . . . . .
# . . # .[.]# . . .
# . . # # # . . . .
# . . . . . . . . .
# . . . . . . . . .
# . . . . . . . . .
# After the above actions, a total of 7 bursts of activity had taken place. Of them, 5 bursts of activity caused an
# infection.
#
# After a total of 70, the grid looks like this, with the virus carrier facing up:
#
# . . . . . # # . .
# . . . . # . . # .
# . . . # . . . . #
# . . # . #[.]. . #
# . . # . # . . # .
# . . . . . # # . .
# . . . . . . . . .
# . . . . . . . . .
# By this time, 41 bursts of activity caused an infection (though most of those nodes have since been cleaned).
#
# After a total of 10000 bursts of activity, 5587 bursts will have caused an infection.
#
# Given your actual map, after 10000 bursts of activity, how many bursts cause a node to become infected? (Do not count
# nodes that begin infected.)


#######################################################################################################################
# Prepare libs
#######################################################################################################################
import time
import sys


#######################################################################################################################
# Functions
#######################################################################################################################
def build_matrix(input_data):
    matrix = []
    for input_line in input_data:
        matrix.append(list(input_line.replace("\n", "")))

    return matrix


def turn(direction_current, command):
    if direction_current == "U":
        if command == "R":
            return "R"
        else:
            return "L"
    elif direction_current == "D":
        if command == "R":
            return "L"
        else:
            return "R"
    elif direction_current == "R":
        if command == "R":
            return "D"
        else:
            return "U"
    elif direction_current == "L":
        if command == "R":
            return "U"
        else:
            return "D"
    else:
        sys.exit("Really!? Now you messed up with the direction")


def step(x, y, direction):
    if direction == "U":
        return {"X": x, "Y": y-1}
    elif direction == "D":
        return {"X": x, "Y": y+1}
    elif direction == "R":
        return {"X": x+1, "Y": y}
    elif direction == "L":
        return {"X": x-1, "Y": y}
    else:
        sys.exit("Dude!? You cannot step in non existent direction")


def move(position, direction, matrix):
    x = position.get("X")
    y = position.get("Y")

    if matrix[y][x] == ".":
        direction_next = turn(direction, "L")
    elif matrix[y][x] == "#":
        direction_next = turn(direction, "R")
    else:
        sys.exit("The fuck!? You are not supposed to have value <" + matrix[y][x] + "> in the matrix, dummy!")

    position_next = step(x, y, direction_next)

    return {"Position": position_next, "Direction": direction_next}


def out_of_bounds(position, limit):
    x = position.get("X")
    y = position.get("Y")

    if x < 0 or x >= limit or y < 0 or y >= limit:
        return True
    else:
        return False


def expand_matrix(matrix):
    matrix_expanded = []
    new_len = len(matrix) + 2

    matrix_expanded.append(["."] * new_len)
    for row in matrix:
        row_expanded = ["."] + row + ["."]
        matrix_expanded.append(row_expanded)
    matrix_expanded.append(["."] * new_len)

    return matrix_expanded


def burst(position, direction, matrix):
    infected = False

    results = move(position, direction, matrix)
    position_next = results.get("Position")
    direction_next = results.get("Direction")

    x = position.get("X")
    y = position.get("Y")
    if matrix[y][x] == ".":
        matrix[y][x] = "#"
        infected = True
    else:
        matrix[y][x] = "."

    if out_of_bounds(position_next, len(matrix)):
        matrix = expand_matrix(matrix)
        x = position_next.get("X") + 1
        y = position_next.get("Y") + 1
        position_next = {"X": x, "Y": y}

    return {"Position": position_next, "Direction": direction_next, "Matrix": matrix, "Infected": infected}


#######################################################################################################################
# Root function
#######################################################################################################################
def sporifica(input_data):
    infected_cells = 0

    matrix = build_matrix(input_data)
    position = {"X": int(len(matrix) / 2), "Y": int(len(matrix) / 2)}
    direction = "U"

    burst_index = 0
    while burst_index < 10000:
        results = burst(position, direction, matrix)
        matrix = results.get("Matrix")
        position = results.get("Position")
        direction = results.get("Direction")

        if results.get("Infected"):
            infected_cells += 1

        burst_index += 1

    return infected_cells


#######################################################################################################################
# Main function
#######################################################################################################################
def __main__(input_data):
    # 1. One result <-> More lines
    result = sporifica(input_data)

    # 2. One result <-> One line
    # result = some_function(input_data.read())

    print("##--RESULT--##")
    print("Number of cells infected:", result)

    # 2.1 For test purposes
    # for input_line in input_data:
    #     result = some_function(input_line.replace("\n", ""))
    #     print("##--RESULT--##")
    #     print("Some result:", result)


#######################################################################################################################
# Process
#######################################################################################################################
if __name__ == "__main__":
    # Start time of the program
    start = time.time()

    # Input file
    input_file = open('../Input/Day22.txt', 'r')

    # Main functionality
    __main__(input_file)

    # End time of the program
    end = time.time()
    # Running time of the program
    print("Program ran for: ", end - start, "seconds.")
