# --- Day 8: I Heard You Like Registers ---
# You receive a signal directly from the CPU. Because of your recent assistance with jump instructions, it would like
# you to compute the result of a series of unusual register instructions.
#
# Each instruction consists of several parts: the register to modify, whether to increase or decrease that register's
# value, the amount by which to increase or decrease it, and a condition. If the condition fails, skip the instruction
# without modifying the register. The registers all start at 0. The instructions look like this:
#
# b inc 5 if a > 1
# a inc 1 if b < 5
# c dec -10 if a >= 1
# c inc -20 if c == 10
# These instructions would be processed as follows:
#
#   -   Because a starts at 0, it is not greater than 1, and so b is not modified.
#   -   a is increased by 1 (to 1) because b is less than 5 (it is 0).
#   -   c is decreased by -10 (to 10) because a is now greater than or equal to 1 (it is 1).
#   -   c is increased by -20 (to -10) because c is equal to 10.
#
# After this process, the largest value in any register is 1.
#
# You might also encounter <= (less than or equal to) or != (not equal to). However, the CPU doesn't have the bandwidth
# to tell you what all the registers are named, and leaves that to you to determine.
#
# What is the largest value in any register after completing the instructions in your puzzle input?

# Prepare libs
import time

# Functions
def build_command(parameters):
    register = parameters[0]
    operation = parameters[1]
    value = int(parameters[2])
    compare_parameter_left = parameters[4]
    compare_condition = parameters[5]
    compare_parameter_right = int(parameters[6])

    command = {"Register": register, "Operation": operation, "Value": value,
               "Left parameter": compare_parameter_left, "Right parameter": compare_parameter_right,
               "Condition": compare_condition}

    return command


def command_check_availability(right_parameter, left_parameter, condition, registers):
    command_execute_flag = False
    left_parameter_value = registers[left_parameter]

    if condition == "<":
        if left_parameter_value < right_parameter:
            command_execute_flag = True
    elif condition == "<=":
        if left_parameter_value <= right_parameter:
            command_execute_flag = True
    elif condition == ">":
        if left_parameter_value > right_parameter:
            command_execute_flag = True
    elif condition == ">=":
        if left_parameter_value >= right_parameter:
            command_execute_flag = True
    elif condition == "==":
        if left_parameter_value == right_parameter:
            command_execute_flag = True
    elif condition == "!=":
        if left_parameter_value != right_parameter:
            command_execute_flag = True

    return command_execute_flag


def command_execute(command, registers):
    # Add register to list if missing
    if registers.get(command.get("Register")) is None:
        registers[command.get("Register")] = 0
    if registers.get(command.get("Left parameter")) is None:
        registers[command.get("Left parameter")] = 0

    command_execute_flag = command_check_availability(command.get("Right parameter"), command.get("Left parameter"),
                                                      command.get("Condition"), registers)

    if command_execute_flag:
        operation = command.get("Operation")
        register_name = command.get("Register")
        value = command.get("Value")
        if operation == "inc":
            registers[register_name] += value
        else:
            registers[register_name] -= value


def registers_max_value(registers):
    max_value = 0

    for register in registers:
            max_value = max(max_value, registers[register])

    return max_value

# Main function
def __main__(input_file):
    registers = {}
    for input_line in input_file:
        command = build_command(input_line.split())
        command_execute(command, registers)

    max_value = registers_max_value(registers)

    print("##--RESULT--##")
    print("Register maximum value:", max_value)

# Process
if __name__ == "__main__":
    # Start time of the program
    start = time.time()

    # Input file
    input_file = open('../Input/Day8-A.txt', 'r')

    # Main functionality
    __main__(input_file)

    # End time of the program
    end = time.time()
    # Running time of the program
    print("Program ran for: ", end - start, "seconds.")
