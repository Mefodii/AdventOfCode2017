# --- Day 20: Particle Swarm ---
# Suddenly, the GPU contacts you, asking for help. Someone has asked it to simulate too many particles, and it won't be
# able to finish them all in time to render the next frame at this rate.
#
# It transmits to you a buffer (your puzzle input) listing each particle in order (starting with particle 0, then
# particle 1, particle 2, and so on). For each particle, it provides the X, Y, and Z coordinates for the particle's
# position (p), velocity (v), and acceleration (a), each in the format <X,Y,Z>.
#
# Each tick, all particles are updated simultaneously. A particle's properties are updated in the following order:
#
#   -   Increase the X velocity by the X acceleration.
#   -   Increase the Y velocity by the Y acceleration.
#   -   Increase the Z velocity by the Z acceleration.
#   -   Increase the X position by the X velocity.
#   -   Increase the Y position by the Y velocity.
#   -   Increase the Z position by the Z velocity.
#
# Because of seemingly tenuous rationale involving z-buffering, the GPU would like to know which particle will stay
# closest to position <0,0,0> in the long term. Measure this using the Manhattan distance, which in this situation is
# simply the sum of the absolute values of a particle's X, Y, and Z position.
#
# For example, suppose you are only given two particles, both of which stay entirely on the X-axis (for simplicity).
# Drawing the current states of particles 0 and 1 (in that order) with an adjacent a number line and diagram of current
# X positions (marked in parenthesis), the following would take place:
#
# p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
# p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>                         (0)(1)
#
# p=< 4,0,0>, v=< 1,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
# p=< 2,0,0>, v=<-2,0,0>, a=<-2,0,0>                      (1)   (0)
#
# p=< 4,0,0>, v=< 0,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
# p=<-2,0,0>, v=<-4,0,0>, a=<-2,0,0>          (1)               (0)
#
# p=< 3,0,0>, v=<-1,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
# p=<-8,0,0>, v=<-6,0,0>, a=<-2,0,0>                         (0)
#
# At this point, particle 1 will never be closer to <0,0,0> than particle 0, and so, in the long run, particle 0 will
# stay closest.
#
# Which particle will stay closest to position <0,0,0> in the long term?


#######################################################################################################################
# Prepare libs
#######################################################################################################################
import time
import sys
import copy


#######################################################################################################################
# Functions
#######################################################################################################################
def dict_copy(dict_list):
    copy_list = []
    for dict_elem in dict_list:
        dict_elem_copy = copy.deepcopy(dict_elem)
        copy_list.append(dict_elem_copy)

    return copy_list


def build_particles(input_data):
    particle_list = []

    for input_line in input_data:
        particle_id = len(particle_list)
        particle_data = input_line.replace("\n", "").split(", ")

        particle_position = build_coords(particle_data[0][3:-1])
        particle_velocity = build_coords(particle_data[1][3:-1])
        particle_acceleration = build_coords(particle_data[2][3:-1])

        particle_total_acceleration = absolute_sum(particle_acceleration)
        particle_total_velocity = absolute_sum(particle_velocity)

        particle = {"ID": particle_id, "Position": particle_position,
                    "Velocity": particle_velocity, "Total velocity": particle_total_velocity,
                    "Acceleration": particle_acceleration, "Total acceleration": particle_total_acceleration}
        particle_list.append(particle)

    return particle_list


def absolute_sum(coords):
    x = coords.get("X")
    y = coords.get("Y")
    z = coords.get("Z")

    return abs(x) + abs(y) + abs(z)


def build_coords(text_coords):
    x, y, z = [int(i) for i in text_coords.split(",")]
    return {"X": x, "Y": y, "Z": z}


def get_slowest_particles(particle_list):
    particle_list_slowest_acc = []
    value_min = float("inf")

    for particle in particle_list:
        particle_total_acceleration = particle.get("Total acceleration")
        if particle_total_acceleration < value_min:
            particle_list_slowest_acc = [particle]
            value_min = particle_total_acceleration
        elif particle_total_acceleration == value_min:
            particle_list_slowest_acc.append(particle)

    particle_list_slowest = []
    value_min = float("inf")

    for particle in particle_list_slowest_acc:
        particle_total_velocity = particle.get("Total velocity")
        if particle_total_velocity < value_min:
            particle_list_slowest = [particle]
            value_min = particle_total_velocity
        elif particle_total_velocity == value_min:
            particle_list_slowest.append(particle)

    return particle_list_slowest


def get_closest_particle(particle_list):

    particle_list_slowest = get_slowest_particles(particle_list)
    closest_particle = particle_list_slowest[0].get("ID")

    return closest_particle


def sum_coords(first_coords, second_coords):
    x_first = first_coords.get("X")
    y_first = first_coords.get("Y")
    z_first = first_coords.get("Z")

    x_second = second_coords.get("X")
    y_second = second_coords.get("Y")
    z_second = second_coords.get("Z")

    x = x_first + x_second
    y = y_first + y_second
    z = z_first + z_second

    return {"X": x, "Y": y, "Z": z}


def next_velocity(particle):
    return sum_coords(particle.get("Velocity"), particle.get("Acceleration"))


def next_position(particle):
    return sum_coords(particle.get("Velocity"), particle.get("Position"))


def compare_particle_positions(particle_first, particle_second):
    return compare_coords(particle_first.get("Position"), particle_second.get("Position"))


def compare_coords(first_coords, second_coords):
    x_first = first_coords.get("X")
    y_first = first_coords.get("Y")
    z_first = first_coords.get("Z")

    x_second = second_coords.get("X")
    y_second = second_coords.get("Y")
    z_second = second_coords.get("Z")

    if x_first == x_second and y_first == y_second and z_first == z_second:
        return True
    else:
        return False


def next_second(particle_list):
    for particle in particle_list:
        particle["Velocity"] = next_velocity(particle)
        particle["Position"] = next_position(particle)

    i = 0
    while i < len(particle_list):
        collision = False
        j = i + 1
        while j < len(particle_list):
            if compare_particle_positions(particle_list[i], particle_list[j]):
                collision = True
                del particle_list[j]
                j -= 1
            j += 1

        if collision:
            collision = False
            del particle_list[i]
            i -= 1
        i += 1

    return particle_list


def simulate_particles(particle_list):
    loop_detector = 0
    previous_length = -1
    remained_particles = dict_copy(particle_list)

    while loop_detector < 20:
        remained_particles = next_second(dict_copy(remained_particles))

        if len(remained_particles) != previous_length:
            previous_length = len(remained_particles)
            loop_detector = 0
        else:
            loop_detector += 1

    return remained_particles


#######################################################################################################################
# Root function
#######################################################################################################################
def particle_swarm(input_data):
    particle_list = build_particles(input_data)

    remained_particles = simulate_particles(particle_list)

    return len(remained_particles)


#######################################################################################################################
# Main function
#######################################################################################################################
def __main__(input_data):
    # 1. One result <-> More lines
    result = particle_swarm(input_data)

    # 2. One result <-> One line
    # result = some_function(input_data.read())

    print("##--RESULT--##")
    print("Some result:", result)

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
    input_file = open('../Input/Day20.txt', 'r')

    # Main functionality
    __main__(input_file)

    # End time of the program
    end = time.time()
    # Running time of the program
    print("Program ran for: ", end - start, "seconds.")
