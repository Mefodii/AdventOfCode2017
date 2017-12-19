# --- Day 15: Dueling Generators ---
# Here, you encounter a pair of dueling generators. The generators, called generator A and generator B, are trying to
# agree on a sequence of numbers. However, one of them is malfunctioning, and so the sequences don't always match.
#
# As they do this, a judge waits for each of them to generate its next value, compares the lowest 16 bits of both
# values, and keeps track of the number of times those parts of the values match.
#
# The generators both work on the same principle. To create its next value, a generator will take the previous value it
# produced, multiply it by a factor (generator A uses 16807; generator B uses 48271), and then keep the remainder of
# dividing that resulting product by 2147483647. That final remainder is the value it produces next.
#
# To calculate each generator's first value, it instead uses a specific starting value as its "previous value" (as
# listed in your puzzle input).
#
# For example, suppose that for starting values, generator A uses 65, while generator B uses 8921. Then, the first five
# pairs of generated values are:
#
# --Gen. A--  --Gen. B--
#    1092455   430625591
# 1181022009  1233683848
#  245556042  1431495498
# 1744312007   137874439
# 1352636452   285222916
# In binary, these pairs are (with generator A's value first in each pair):
#
# 00000000000100001010101101100111
# 00011001101010101101001100110111
#
# 01000110011001001111011100111001
# 01001001100010001000010110001000
#
# 00001110101000101110001101001010
# 01010101010100101110001101001010
#
# 01100111111110000001011011000111
# 00001000001101111100110000000111
#
# 01010000100111111001100000100100
# 00010001000000000010100000000100
#
# Here, you can see that the lowest (here, rightmost) 16 bits of the third value match: 1110001101001010. Because of
# this one match, after processing these five pairs, the judge would have added only 1 to its total.
#
# To get a significant sample, the judge would like to consider 40 million pairs. (In the example above, the judge
# would eventually find a total of 588 pairs that match in their lowest 16 bits.)
#
# After 40 million pairs, what is the judge's final count?


#######################################################################################################################
# Prepare libs
#######################################################################################################################
import time


#######################################################################################################################
# Functions
#######################################################################################################################
def next_value(value, factor):
    divide_const = 2147483647
    return (value * factor) % divide_const


def analyse_round(value_a, value_b):
    value_a_bin = bin(value_a)[2:].zfill(32)
    value_b_bin = bin(value_b)[2:].zfill(32)

    if value_a_bin[16:] == value_b_bin[16:]:
        return True
    else:
        return False


#######################################################################################################################
# Root function
#######################################################################################################################
def duel(first_robot_initial_line, second_robot_initial_line):
    robot_a_value = int(first_robot_initial_line.split()[-1])
    robot_b_value = int(second_robot_initial_line.split()[-1])
    factor_a = 16807
    factor_b = 48271

    good_rounds = 0
    for i in range(40000000):
        robot_a_value = next_value(robot_a_value, factor_a)
        robot_b_value = next_value(robot_b_value, factor_b)

        if analyse_round(robot_a_value, robot_b_value):
            good_rounds += 1

    return good_rounds



#######################################################################################################################
# Main function
#######################################################################################################################
def __main__(input_file):
    # 1. One result <-> More lines
    # result = some_function(input_file)

    # 2. One result <-> One line
    result = duel(input_file.readline().replace("\n",""), input_file.readline().replace("\n",""))

    print("##--RESULT--##")
    print("Good round count:", result)

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
    input_file = open('../Input/Day15.txt', 'r')

    # Main functionality
    __main__(input_file)

    # End time of the program
    end = time.time()
    # Running time of the program
    print("Program ran for: ", end - start, "seconds.")
