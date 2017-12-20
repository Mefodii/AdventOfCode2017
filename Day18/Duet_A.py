# --- Day 18: Duet ---
# You discover a tablet containing some strange assembly code labeled simply "Duet". Rather than bother the sound card
# with it, you decide to run the code yourself. Unfortunately, you don't see any documentation, so you're left to figure
# out what the instructions mean on your own.
#
# It seems like the assembly is meant to operate on a set of registers that are each named with a single letter and that
# can each hold a single integer. You suppose each register should start with a value of 0.
#
# There aren't that many instructions, so it shouldn't be hard to figure out what they do. Here's what you determine:
#
#   -   snd X plays a sound with a frequency equal to the value of X.
#   -   set X Y sets register X to the value of Y.
#   -   add X Y increases register X by the value of Y.
#   -   mul X Y sets register X to the result of multiplying the value contained in register X by the value of Y.
#   -   mod X Y sets register X to the remainder of dividing the value contained in register X by the value of Y (that
#       is, it sets X to the result of X modulo Y).
#   -   rcv X recovers the frequency of the last sound played, but only when the value of X is not zero. (If it is zero,
#       the command does nothing.)
#   -   jgz X Y jumps with an offset of the value of Y, but only if the value of X is greater than zero. (An offset of
#       2 skips the next instruction, an offset of -1 jumps to the previous instruction, and so on.)
#
# Many of the instructions can take either a register (a single letter) or a number. The value of a register is the
# integer it contains; the value of a number is that number.
#
# After each jump instruction, the program continues with the instruction to which the jump jumped. After any other
# instruction, the program continues with the next instruction. Continuing (or jumping) off either end of the program
# terminates it.
#
# For example:
#
# set a 1
# add a 2
# mul a a
# mod a 5
# snd a
# set a 0
# rcv a
# jgz a -1
# set a 1
# jgz a -2
#
#   -   The first four instructions set a to 1, add 2 to it, square it, and then set it to itself modulo 5, resulting
#       in a value of 4.
#   -   Then, a sound with frequency 4 (the value of a) is played.
#   -   After that, a is set to 0, causing the subsequent rcv and jgz instructions to both be skipped (rcv because a
#       is 0, and jgz because a is not greater than 0).
#   -   Finally, a is set to 1, causing the next jgz instruction to activate, jumping back two instructions to another
#       jump, which jumps again to the rcv, which ultimately triggers the recover operation.
#
# At the time the recover operation is executed, the frequency of the last sound played is 4.
#
# What is the value of the recovered frequency (the value of the most recently played sound) the first time a rcv
# instruction is executed with a non-zero value?


#######################################################################################################################
# Prepare libs
#######################################################################################################################
import time


#######################################################################################################################
# Functions
#######################################################################################################################
def build_command(command_text):
    command_split = command_text.split()

    if len(command_split) == 2:
        return {"Function": command_split[0], "First parameter": command_split[1]}
    else:
        return {"Function": command_split[0], "First parameter": command_split[1], "Second parameter": command_split[2]}


def initialize_register(command_list):
    register_dict = {}
    for command in command_list:
        register_name = command.get("First parameter")
        if not register_name.isdigit():
            if register_name not in register_dict:
                register_dict[register_name] = 0

    return register_dict


def recover(command_list):
    register_dict = initialize_register(command_list)

    last_snd = None
    recovered_snd = None
    index = 0

    run = True
    while run and index < len(command_list):
        command_function = command_list[index].get("Function")

        first_parameter = command_list[index].get("First parameter")
        result_value = None
        jump_value = None

        is_register = False
        is_jump = False

        if first_parameter.lstrip("-").isdigit():
            first_value = int(first_parameter)
        else:
            first_value = int(register_dict.get(first_parameter))
            is_register = True

        if command_function == "snd" or command_function == "rcv":
            result_value = first_value
            if command_function == "snd":
                if result_value > 0:
                    last_snd = result_value
            else:
                if result_value > 0:
                    run = False
                    recovered_snd = last_snd
        else:
            second_parameter = command_list[index].get("Second parameter")
            if second_parameter.lstrip("-").isdigit():
                second_value = int(second_parameter)
            else:
                second_value = int(register_dict.get(second_parameter))

            if command_function == "set":
                result_value = second_value
            elif command_function == "add":
                result_value = first_value + second_value
            elif command_function == "mul":
                result_value = first_value * second_value
            elif command_function == "mod":
                result_value = first_value % second_value
            elif command_function == "jgz":
                result_value = first_value
                if first_value > 0:
                    is_jump = True
                    jump_value = second_value

        if is_jump:
            index += jump_value
        else:
            if is_register:
                register_dict[first_parameter] = result_value

            index += 1


    return recovered_snd


#######################################################################################################################
# Root function
#######################################################################################################################
def duet(input_file):
    command_list = []

    for input_line in input_file:
        command_list.append(build_command(input_line.replace("\n","")))

    first_rcv = recover(command_list)

    return first_rcv



#######################################################################################################################
# Main function
#######################################################################################################################
def __main__(input_file):
    # 1. One result <-> More lines
    result = duet(input_file)

    # 2. One result <-> One line
    # result = some_function(input_file.read())

    print("##--RESULT--##")
    print("Some result:", result)

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
    input_file = open('../Input/Day18.txt', 'r')

    # Main functionality
    __main__(input_file)

    # End time of the program
    end = time.time()
    # Running time of the program
    print("Program ran for: ", end - start, "seconds.")
