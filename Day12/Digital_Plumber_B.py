# --- Day 12: Digital Plumber ---
# Walking along the memory banks of the stream, you find a small village that is experiencing a little confusion: some
# programs can't communicate with each other.
#
# Programs in this village communicate using a fixed system of pipes. Messages are passed between programs using these
# pipes, but most programs aren't connected to each other directly. Instead, programs pass messages between each other
# until the message reaches the intended recipient.
#
# For some reason, though, some of these messages aren't ever reaching their intended recipient, and the programs
# suspect that some pipes are missing. They would like you to investigate.
#
# You walk through the village and record the ID of each program and the IDs with which it can communicate directly
# (your puzzle input). Each program has one or more programs with which it can communicate, and these pipes are
# bidirectional; if 8 says it can communicate with 11, then 11 will say it can communicate with 8.
#
# You need to figure out how many programs are in the group that contains program ID 0.
#
# For example, suppose you go door-to-door like a travelling salesman and record the following list:
#
# 0 <-> 2
# 1 <-> 1
# 2 <-> 0, 3, 4
# 3 <-> 2, 4
# 4 <-> 2, 3, 6
# 5 <-> 6
# 6 <-> 4, 5
# In this example, the following programs are in the group that contains program ID 0:
#
#   -   Program 0 by definition.
#   -   Program 2, directly connected to program 0.
#   -   Program 3 via program 2.
#   -   Program 4 via program 2.
#   -   Program 5 via programs 6, then 4, then 2.
#   -   Program 6 via programs 4, then 2.
#
# Therefore, a total of 6 programs are in this group; all but program 1, which has a pipe that connects it to itself.
#
# How many programs are in the group that contains program ID 0?
#
# --- Part Two ---
# There are more programs than just the ones in the group containing program ID 0. The rest of them have no way of
# reaching that group, and still might have no way of reaching each other.
#
# A group is a collection of programs that can all communicate via pipes either directly or indirectly. The programs
# you identified just a moment ago are all part of the same group. Now, they would like you to determine the total
# number of groups.
#
# In the example above, there were 2 groups: one consisting of programs 0,2,3,4,5,6, and the other consisting solely
# of program 1.
#
# How many groups are there in total?
#
#######################################################################################################################
# Prepare libs
#######################################################################################################################
import time


#######################################################################################################################
# Functions
#######################################################################################################################
def program_index_by_name(name, program_list):
    for i in range(0, len(program_list)):
        if program_list[i]['Name'] == name:
            return i

    return -1


def programs_reset(programs):
    for program in programs:
        program["Visited"] = False

    return programs


def add_program(raw_input):
    processed_input = process_input(raw_input)
    program_name = processed_input[0]
    children = processed_input[1]
    visited_flag = False

    return {"Name": program_name, "Children": children, "Visited": visited_flag}


def process_input(raw_input):
    split = raw_input.split(" <-> ")
    node_name = split[0]
    children = split[1].split(", ")

    return [node_name, children]


def calculate_groups(programs):
    groups=0

    for program in programs:
        if not program.get("Visited"):
            groups += 1
            visit_group(program, programs)

    return groups


def visit_group(current_program, programs):
    current_program["Visited"] = True

    for child in current_program.get("Children"):
        program_child = programs[program_index_by_name(child, programs)]
        if not program_child.get("Visited"):
            visit_group(program_child, programs)





def calculate_connections_to_program(destination_program_name, programs):
    connections = 0

    for program in programs:
        programs_copy = programs_reset(programs)
        index = program_index_by_name(program.get("Name"), programs)
        current_program = programs_copy[index]
        if check_connection_to_program(current_program, destination_program_name, programs_copy):
            connections += 1

    return connections


def check_connection_to_program(current_program, destination_program_name, programs):
    current_program["Visited"] = True

    if current_program.get("Name") == destination_program_name:
        return True
    else:
        for child in current_program.get("Children"):
            program_child = programs[program_index_by_name(child, programs)]
            if not program_child.get("Visited"):
                if check_connection_to_program(program_child, destination_program_name, programs):
                    return True

    return False


#######################################################################################################################
# Main function
#######################################################################################################################
def __main__(input_file):
    programs = []
    for input_line in input_file:
        programs.append(add_program(input_line.replace("\n", "")))

    groups = calculate_groups(programs)

    print("##--RESULT--##")
    print("Number of groups:", groups)


#######################################################################################################################
# Process
#######################################################################################################################
if __name__ == "__main__":
    # Start time of the program
    start = time.time()

    # Input file
    input_file = open('../Input/Day12.txt', 'r')

    # Main functionality
    __main__(input_file)

    # End time of the program
    end = time.time()
    # Running time of the program
    print("Program ran for: ", end - start, "seconds.")
