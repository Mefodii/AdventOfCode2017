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


#######################################################################################################################
# Main function
#######################################################################################################################
def __main__(input_file):
    # 1. One result <-> More lines
    # result = some_function(input_file)

    # 2. One result <-> One line
    result = disk_fragmentation_used_cells(input_file.read())

    print("##--RESULT--##")
    print("Used cells:", result)

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


