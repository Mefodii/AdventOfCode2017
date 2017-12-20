# --- Day 16: Permutation Promenade ---
# You come upon a very unusual sight; a group of programs here appear to be dancing.
#
# There are sixteen programs in total, named a through p. They start by standing in a line: a stands in position 0, b
# stands in position 1, and so on until p, which stands in position 15.
#
# The programs' dance consists of a sequence of dance moves:
#
#   -   Spin, written sX, makes X programs move from the end to the front, but maintain their order otherwise. (For
# example,s3 on abcde produces cdeab).
#   -   Exchange, written xA/B, makes the programs at positions A and B swap places.
#   -   Partner, written pA/B, makes the programs named A and B swap places.
#
# For example, with only five programs standing in a line (abcde), they could do the following dance:
#
#   -   s1, a spin of size 1: eabcd.
#   -   x3/4, swapping the last two programs: eabdc.
#   -   pe/b, swapping programs e and b: baedc.
#
# After finishing their dance, the programs end up in order baedc.
#
# You watch the dance for a while and record their dance moves (your puzzle input). In what order are the programs
# standing after their dance?
# --- Part Two ---
# Now that you're starting to get a feel for the dance moves, you turn your attention to the dance as a whole.
#
# Keeping the positions they ended up in from their previous dance, the programs perform it again and again: including
# the first dance, a total of one billion (1000000000) times.
#
# In the example above, their second dance would begin with the order baedc, and use the same dance moves:
#
#   -   s1, a spin of size 1: cbaed.
#   -   x3/4, swapping the last two programs: cbade.
#   -   pe/b, swapping programs e and b: ceadb.
#
# In what order are the programs standing after their billion dances?


#######################################################################################################################
# Prepare libs
#######################################################################################################################
import time


#######################################################################################################################
# Functions
#######################################################################################################################
def dance_move_execute(dance_move, first_parameter, second_parameter, programs):
    if dance_move == "s":
        programs = spin(first_parameter, programs)
    elif dance_move == "x":
        programs = exchange(first_parameter, second_parameter, programs)
    elif dance_move == "p":
        programs = partner(first_parameter, second_parameter, programs)

    return programs


def compile_move(dance_move):
    dance_move_name = dance_move[0]
    first_parameter = None
    second_parameter = None
    if dance_move_name == "s":
        first_parameter = 16 - int(dance_move[1:])
    elif dance_move_name == "x":
        positions = dance_move[1:].split("/")
        first_parameter = int(positions[0])
        second_parameter = int(positions[1])
    elif dance_move_name == "p":
        partners = dance_move[1:].split("/")
        first_parameter = partners[0]
        second_parameter = partners[1]

    return [dance_move_name, first_parameter, second_parameter]


def spin(spin_center, programs):
    programs = programs[spin_center:len(programs)] + programs[0:spin_center]
    return programs


def exchange(first_position, second_position, programs):
    programs[second_position], programs[first_position] = programs[first_position], programs[second_position]
    return programs


def partner(first_partner, second_partner, programs):
    return exchange(programs.index(first_partner), programs.index(second_partner), programs)


def search_in_log(programs, dance_log):
    for i in range(len(dance_log)):
        if dance_log[i] == programs:
            return i

    return -1



#######################################################################################################################
# Root function
#######################################################################################################################
def dance(dance_moves):
    programs = [chr(i + ord("a")) for i in range(16)]

    dance_move_list = []
    for dance_move in dance_moves.split(","):
        dance_move_list.append(compile_move(dance_move))

    dance_log = []
    run = True
    run_number = 0
    total_run = 1000000000
    loop_start_index = -1

    while run and run_number < total_run:
        run_number += 1
        loop_start_index = search_in_log(''.join(programs), dance_log)
        if loop_start_index < 0:
            dance_log.append(''.join(programs))
            for dance_move in dance_move_list:
                programs = dance_move_execute(dance_move[0], dance_move[1], dance_move[2], programs)
        else:
            run = False

    dance_log_looped = dance_log[loop_start_index:]

    long_dance_result_programs_index = (total_run - run_number + 1) % len(dance_log_looped)
    long_dance_result_programs = dance_log_looped[long_dance_result_programs_index]

    return ''.join(long_dance_result_programs)

#######################################################################################################################
# Main function
#######################################################################################################################
def __main__(input_file):
    # 1. One result <-> More lines
    # result = dance(input_file)

    # 2. One result <-> One line
    result = dance(input_file.read())

    print("##--RESULT--##")
    print("Programs after dance:", result)

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
    input_file = open('../Input/Day16.txt', 'r')

    # Main functionality
    __main__(input_file)

    # End time of the program
    end = time.time()
    # Running time of the program
    print("Program ran for: ", end - start, "seconds.")
