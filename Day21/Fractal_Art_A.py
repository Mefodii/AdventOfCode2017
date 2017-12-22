# --- Day 21: Fractal Art ---
# You find a program trying to generate some art. It uses a strange process that involves repeatedly enhancing the
# detail of an image through a set of rules.
#
# The image consists of a two-dimensional square grid of pixels that are either on (#) or off (.). The program always
# begins with this pattern:
#
# .#.
# ..#
# ###
# Because the pattern is both 3 pixels wide and 3 pixels tall, it is said to have a size of 3.
#
# Then, the program repeats the following process:
#
# If the size is evenly divisible by 2, break the pixels up into 2x2 squares, and convert each 2x2 square into a 3x3
# square by following the corresponding enhancement rule.
# Otherwise, the size is evenly divisible by 3; break the pixels up into 3x3 squares, and convert each 3x3 square into
# a 4x4 square by following the corresponding enhancement rule.
# Because each square of pixels is replaced by a larger one, the image gains pixels and so its size increases.
#
# The artist's book of enhancement rules is nearby (your puzzle input); however, it seems to be missing rules. The
# artist explains that sometimes, one must rotate or flip the input pattern to find a match. (Never rotate or flip the
# output pattern, though.) Each pattern is written concisely: rows are listed as single units, ordered top-down, and
# separated by slashes. For example, the following rules correspond to the adjacent patterns:
#
# ../.#  =  ..
#           .#
#
#                 .#.
# .#./..#/###  =  ..#
#                 ###
#
#                         #..#
# #..#/..../#..#/.##.  =  ....
#                         #..#
#                         .##.
# When searching for a rule to use, rotate and flip the pattern as necessary. For example, all of the following patterns
# match the same rule:
#
# .#.   .#.   #..   ###
# ..#   #..   #.#   ..#
# ###   ###   ##.   .#.
# Suppose the book contained the following two rules:
#
# ../.# => ##./#../...
# .#./..#/### => #..#/..../..../#..#
# As before, the program begins with this pattern:
#
# .#.
# ..#
# ###
# The size of the grid (3) is not divisible by 2, but it is divisible by 3. It divides evenly into a single square; the
# square matches the second rule, which produces:
#
# #..#
# ....
# ....
# #..#
# The size of this enhanced grid (4) is evenly divisible by 2, so that rule is used. It divides evenly into four
# squares:
#
# #.|.#
# ..|..
# --+--
# ..|..
# #.|.#
# Each of these squares matches the same rule (../.# => ##./#../...), three of which require some flipping and rotation
# to line up with the rule. The output for the rule is the same in all four cases:
#
# ##.|##.
# #..|#..
# ...|...
# ---+---
# ##.|##.
# #..|#..
# ...|...
# Finally, the squares are joined into a new grid:
#
# ##.##.
# #..#..
# ......
# ##.##.
# #..#..
# ......
# Thus, after 2 iterations, the grid contains 12 pixels that are on.
#
# How many pixels stay on after 5 iterations?


#######################################################################################################################
# Prepare libs
#######################################################################################################################
import time
import sys
import math


#######################################################################################################################
# Functions
#######################################################################################################################
def rotate(matrix, degree):
    if degree not in [0, 90, 180, 270, 360]:
        sys.exit("WRONG! Check value degree value again.")
    if degree == 0:
        return matrix
    elif degree > 0:
        return rotate([list(a) for a in zip(*matrix[::-1])], degree-90)


def build_matrix():
    # return [list(".#."), list("..#"), list("###")]
    return [list("...."), list(".#.#"), list("...."), list(".#.#")]


def build_rules(input_data):
    rule_list = []

    for input_line in input_data:
        pattern_input, pattern_output = input_line.replace("\n", "").split(" => ")

        rule = {"Input": [list(row) for row in pattern_input.split("/")],
                "Output": [list(row) for row in pattern_output.split("/")]}
        rule_list.append(rule)

    return rule_list


def split_matrix(grid, matrix):

    matrix_split = []

    for i in range(len(matrix) // grid):
        for j in range(len(matrix) // grid):
            matrix_block = []

            index_column_low = j * grid
            index_column_high = index_column_low + grid

            for k in range(grid):
                index_row = grid * i + k
                matrix_block.append(matrix[index_row][index_column_low:index_column_high])
            matrix_split.append(matrix_block)

    return matrix_split


def merge_matrix(grid, matrix):
    matrix_merged = []
    matrix_merged_length = int(math.sqrt(len(matrix)))

    for i in range(matrix_merged_length):
        matrix_block_row = i * matrix_merged_length

        for j in range(grid):
            matrix_block_element_row = j
            matrix_merged_row = []

            for k in range(matrix_merged_length):
                matrix_block_index = matrix_block_row + k
                matrix_merged_row += matrix[matrix_block_index][matrix_block_element_row]
            matrix_merged.append(matrix_merged_row)

    return matrix_merged


def expand_matrix(matrix, rule_list):

    if len(matrix) % 2 == 0:
        grid = 2
    else:
        grid = 3

    matrix_split = split_matrix(grid, matrix)

    matrix_expanded_raw = []
    for m in matrix_split:
        run = True
        index = 0
        while run and index < len(rule_list):
            pattern_input = rule_list[index].get("Input")
            if m == pattern_input:
                matrix_expanded_raw.append(rule_list[index].get("Output"))
                run = False
            index += 1

    matrix_expanded = merge_matrix(grid + 1, matrix_expanded_raw)

    return matrix_expanded


def count_pixels_on(matrix):
    count = 0
    for row in matrix:
        for cell in row:
            if cell == "#":
                count += 1
    return count


#######################################################################################################################
# Root function
#######################################################################################################################
def fractal_art(input_data):
    rule_list = build_rules(input_data)

    matrix = build_matrix()

    run_index = 0
    while run_index < 1:
        matrix = expand_matrix(matrix, rule_list)
        run_index += 1

    pixels_on = count_pixels_on(matrix)

    return pixels_on


#######################################################################################################################
# Main function
#######################################################################################################################
def __main__(input_data):
    # 1. One result <-> More lines
    result = fractal_art(input_data)

    # 2. One result <-> One line
    # result = some_function(input_data.read())

    print("##--RESULT--##")
    print("Number of pixels on:", result)

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
    input_file = open('../Input/Day21-Test.txt', 'r')

    # Main functionality
    __main__(input_file)

    # End time of the program
    end = time.time()
    # Running time of the program
    print("Program ran for: ", end - start, "seconds.")
