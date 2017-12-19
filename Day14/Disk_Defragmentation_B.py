# --- Day 14: Disk Defragmentation ---
# Suddenly, a scheduled job activates the system's disk defragmenter. Were the situation different, you might sit and
# watch it for a while, but today, you just don't have that kind of time. It's soaking up valuable system resources that
# are needed elsewhere, and so the only option is to help it finish its task as soon as possible.
#
# The disk in question consists of a 128x128 grid; each square of the grid is either free or used. On this disk, the
# state of the grid is tracked by the bits in a sequence of knot hashes.
#
# A total of 128 knot hashes are calculated, each corresponding to a single row in the grid; each hash contains 128 bits
# which correspond to individual grid squares. Each bit of a hash indicates whether that square is free (0) or used (1).
#
# The hash inputs are a key string (your puzzle input), a dash, and a number from 0 to 127 corresponding to the row.
# For example, if your key string were flqrgnkx, then the first row would be given by the bits of the knot hash of
# flqrgnkx-0, the second row from the bits of the knot hash of flqrgnkx-1, and so on until the last row, flqrgnkx-127.
#
# The output of a knot hash is traditionally represented by 32 hexadecimal digits; each of these digits correspond to
# 4 bits, for a total of 4 * 32 = 128 bits. To convert to bits, turn each hexadecimal digit to its equivalent binary
# value, high-bit first: 0 becomes 0000, 1 becomes 0001, e becomes 1110, f becomes 1111, and so on; a hash that begins
# with a0c2017... in hexadecimal would begin with 10100000110000100000000101110000... in binary.
#
# Continuing this process, the first 8 rows and columns for key flqrgnkx appear as follows, using # to denote used
# squares, and . to denote free ones:
#
# ##.#.#..-->
# .#.#.#.#
# ....#.#.
# #.#.##.#
# .##.#...
# ##..#..#
# .#...#..
# ##.#.##.-->
# |      |
# V      V
# In this example, 8108 squares are used across the entire 128x128 grid.
#
# Given your actual key string, how many squares are used?
#
# Your puzzle input is ljoxqyyw.
# --- Part Two ---
# Now, all the defragmenter needs to know is the number of regions. A region is a group of used squares that are all
# adjacent, not including diagonals. Every used square is in exactly one region: lone used squares form their own
# isolated regions, while several adjacent squares all count as a single region.
#
# In the example above, the following nine regions are visible, each marked with a distinct digit:
#
# 11.2.3..-->
# .1.2.3.4
# ....5.6.
# 7.8.55.9
# .88.5...
# 88..5..8
# .8...8..
# 88.8.88.-->
# |      |
# V      V
# Of particular interest is the region marked 8; while it does not appear contiguous in this small view, all of the
# squares marked 8 are connected when considering the whole 128x128 grid. In total, in this example, 1242 regions are
# present.
#
# How many regions are present given your key string?


#######################################################################################################################
# Prepare libs
#######################################################################################################################
import time
import Day10.Knot_Hash_B as hash_knot


#######################################################################################################################
# Functions
#######################################################################################################################
def hex_to_binary(hex_string):
    binary_length = len(hex_string) * 4
    return bin(int(hex_string, 16))[2:].zfill(binary_length)


def binary_hash_to_dict_list(binary_hash):
    dict_list = []

    for cell in binary_hash:
        dict_cell = {"Value": cell, "Visited": False}
        dict_list.append(dict_cell)

    return dict_list


def visit_group(row, column, disk_matrix):
    current_cell = disk_matrix[row][column]
    current_cell["Visited"] = True

    # upper cell
    if row > 0:
        i = row - 1
        j = column
        next_cell = disk_matrix[i][j]
        if not next_cell.get("Visited") and next_cell.get("Value") == "1":
            visit_group(i, j, disk_matrix)
    # lower cell
    if row < len(disk_matrix) - 1:
        i = row + 1
        j = column
        next_cell = disk_matrix[i][j]
        if not next_cell.get("Visited") and next_cell.get("Value") == "1":
            visit_group(i, j, disk_matrix)
    # right cell
    if column < len(disk_matrix[row]) - 1:
        i = row
        j = column + 1
        next_cell = disk_matrix[i][j]
        if not next_cell.get("Visited") and next_cell.get("Value") == "1":
            visit_group(i, j, disk_matrix)
    # left cell
    if column > 0:
        i = row
        j = column - 1
        next_cell = disk_matrix[i][j]
        if not next_cell.get("Visited") and next_cell.get("Value") == "1":
            visit_group(i, j, disk_matrix)


#######################################################################################################################
# Root function
#######################################################################################################################
def disk_fragmentation_used_cells(input_line):
    disk_matrix = []

    for i in range(128):
        command = input_line + "-" + str(i)
        hex_hash = hash_knot.string_to_knot_hash(command)

        binary_hash = hex_to_binary(hex_hash)
        disk_matrix.append(binary_hash)

    used_cells = 0
    for row in disk_matrix:
        used_cells += row.count("1")

    return used_cells


def disk_fragmentation_count_groups(input_line):
    disk_matrix = []

    for i in range(128):
        command = input_line + "-" + str(i)
        hex_hash = hash_knot.string_to_knot_hash(command)

        binary_hash = hex_to_binary(hex_hash)
        binary_hash_dict = binary_hash_to_dict_list(binary_hash)
        disk_matrix.append(binary_hash_dict)

    groups_number = 0

    for i in range(len(disk_matrix)):
        for j in range(len(disk_matrix[i])):
            cell_value = disk_matrix[i][j].get("Value")
            cell_visited_flag = disk_matrix[i][j].get("Visited")

            if not cell_visited_flag and cell_value == "1":
                visit_group(i, j, disk_matrix)
                groups_number += 1

    return groups_number


#######################################################################################################################
# Main function
#######################################################################################################################
def __main__(input_file):
    # 1. One result <-> More lines
    # result = some_function(input_file)

    # 2. One result <-> One line
    result = disk_fragmentation_count_groups(input_file.read())

    print("##--RESULT--##")
    print("Groups number:", result)

    # 2.1 For test purposes
    # for input_line in input_file:
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
    input_file = open('../Input/Day14.txt', 'r')

    # Main functionality
    __main__(input_file)

    # End time of the program
    end = time.time()
    # Running time of the program
    print("Program ran for: ", end - start, "seconds.")


