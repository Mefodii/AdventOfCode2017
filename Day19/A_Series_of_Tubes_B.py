# --- Day 19: A Series of Tubes ---
# Somehow, a network packet got lost and ended up here. It's trying to follow a routing diagram (your puzzle input), but
# it's confused about where to go.
#
# Its starting point is just off the top of the diagram. Lines (drawn with |, -, and +) show the path it needs to take,
# starting by going down onto the only line connected to the top of the diagram. It needs to follow this path until it
# reaches the end (located somewhere within the diagram) and stop there.
#
# Sometimes, the lines cross over each other; in these cases, it needs to continue going the same direction, and only
# turn left or right when there's no other option. In addition, someone has left letters on the line; these also don't
# change its direction, but it can use them to keep track of where it's been. For example:
#
#      |
#      |  +--+
#      A  |  C
#  F---|----E|--+
#      |  |  |  D
#      +B-+  +--+
#
# Given this diagram, the packet needs to take the following path:
#
#   -   Starting at the only line touching the top of the diagram, it must go down, pass through A, and continue onward
# to the first +.
#   -   Travel right, up, and right, passing through B in the process.
#   -   Continue down (collecting C), right, and up (collecting D).
#   -   Finally, go all the way left through E and stopping at F.
#
# Following the path to the end, the letters it sees on its path are ABCDEF.
#
# The little packet looks up at you, hoping you can help it find the way. What letters will it see (in the order it
# would see them) if it follows the path? (The routing diagram is very wide; make sure you view it without line
# wrapping.)
# --- Part Two ---
# The packet is curious how many steps it needs to go.
#
# For example, using the same routing diagram from the example above...
#
#      |
#      |  +--+
#      A  |  C
#  F---|--|-E---+
#      |  |  |  D
#      +B-+  +--+
#
# ...the packet would go:
#
#   -   6 steps down (including the first line at the top of the diagram).
#   -   3 steps right.
#   -   4 steps up.
#   -   3 steps right.
#   -   4 steps down.
#   -   3 steps right.
#   -   2 steps up.
#   -   13 steps left (including the F it stops on).
#
# This would result in a total of 38 steps.
#
# How many steps does the packet need to go?


#######################################################################################################################
# Prepare libs
#######################################################################################################################
import time
import sys


#######################################################################################################################
# Functions
#######################################################################################################################
def build_maze(input_data):
    maze = []
    for row in input_data:
        line = row.replace("\n", "")
        row_data = []
        for cell in line:
            row_data.append(cell)
        maze.append(row_data)

    return maze


def get_start_position(maze_top_line):
    for i in range(len(maze_top_line)):
        if maze_top_line[i] == "|":
            return {"X": i, "Y": 0}

    return -1


def get_position_value(position, maze):
    return maze[position.get("Y")][position.get("X")]


def is_dead_end(x, y, maze):
    x_len = len(maze[0])
    y_len = len(maze)
    if x < 0 or x >= x_len or y < 0 or y >= y_len:
        return True
    else:
        if maze[y][x] == " ":
            return True
        else:
            return False


def next_direction(x, y, direction, maze):
    if direction == "D" or direction == "U":
        if maze[y][x+1] != " ":
            return "R"
        else:
            return "L"
    else:
        if maze[y+1][x] != " ":
            return "D"
        else:
            return "U"


def next_turn(position, direction, maze):
    letters = []
    steps_takes = 0

    x_inc = 0
    y_inc = 0

    if direction == "D":
        y_inc = 1
    elif direction == "U":
        y_inc = -1
    elif direction == "R":
        x_inc = 1
    elif direction == "L":
        x_inc = -1
    else:
        sys.exit("No such direction!")

    x = position.get("X") + x_inc
    y = position.get("Y") + y_inc

    dead_end = is_dead_end(x, y, maze)
    while maze[y][x] != "+" and not dead_end:
        steps_takes += 1
        if 64 < ord(maze[y][x]) < 91:
            letters.append(maze[y][x])
        x += x_inc
        y += y_inc
        dead_end = is_dead_end(x, y, maze)

    if not dead_end:
        steps_takes += 1
        position["X"] = x
        position["Y"] = y
        direction = next_direction(x, y, direction, maze)

    return [letters, position, direction, dead_end, steps_takes]


def follow_maze(maze):
    letters = []
    steps_taken = 1

    direction = "D"
    position = get_start_position(maze[0])

    if position == -1:
        sys.exit("No start point in that maze!")
    else:
        run = True
        while run:
            position_value = get_position_value(position, maze)
            if 64 < ord(position_value) < 91:
                letters.append(position_value)

            results = next_turn(position, direction, maze)
            letters += results[0]
            steps_taken += results[4]
            if results[3] is True:
                run = False
            else:
                position = results[1]
                direction = results[2]

    return steps_taken


#######################################################################################################################
# Root function
#######################################################################################################################
def tube_walk(input_data):

    maze = build_maze(input_data)

    steps_taken = follow_maze(maze)

    return steps_taken


#######################################################################################################################
# Main function
#######################################################################################################################
def __main__(input_data):
    # 1. One result <-> More lines
    result = tube_walk(input_data)

    # 2. One result <-> One line
    # result = some_function(input_data.read())

    print("##--RESULT--##")
    print("Letters encountered:", result)

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
    input_file = open('../Input/Day19.txt', 'r')

    # Main functionality
    __main__(input_file)

    # End time of the program
    end = time.time()
    # Running time of the program
    print("Program ran for: ", end - start, "seconds.")
