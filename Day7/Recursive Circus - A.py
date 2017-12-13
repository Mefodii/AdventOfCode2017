# --- Day 7: Recursive Circus ---
# Wandering further through the circuits of the computer, you come upon a tower of programs that have gotten themselves
# into a bit of trouble. A recursive algorithm has gotten out of hand, and now they're balanced precariously in a
# large tower.
#
# One program at the bottom supports the entire tower. It's holding a large disc, and on the disc are balanced several
# more sub-towers. At the bottom of these sub-towers, standing on the bottom disc, are other programs, each holding
# their own disc, and so on. At the very tops of these sub-sub-sub-...-towers, many programs stand simply keeping the
# disc below them balanced but with no disc of their own.
#
# You offer to help, but first you need to understand the structure of these towers. You ask each program to yell out
# their name, their weight, and (if they're holding a disc) the names of the programs immediately above them balancing
# on that disc. You write this information down (your puzzle input). Unfortunately, in their panic, they don't do this
# in an orderly fashion; by the time you're done, you're not sure which program gave which information.
#
# For example, if your list is the following:
#
# pbga (66)
# xhth (57)
# ebii (61)
# havc (66)
# ktlj (57)
# fwft (72) -> ktlj, cntj, xhth
# qoyq (66)
# padx (45) -> pbga, havc, qoyq
# tknk (41) -> ugml, padx, fwft
# jptl (61)
# ugml (68) -> gyxo, ebii, jptl
# gyxo (61)
# cntj (57)
# ...then you would be able to recreate the structure of the towers that looks like this:
#
#                 gyxo
#               /
#          ugml - ebii
#        /      \
#       |         jptl
#       |
#       |         pbga
#      /        /
# tknk --- padx - havc
#      \        \
#       |         qoyq
#       |
#       |         ktlj
#        \      /
#          fwft - cntj
#               \
#                 xhth
# In this example, tknk is at the bottom of the tower (the bottom program), and is holding up ugml, padx, and fwft.
# Those programs are, in turn, holding up other programs; in this example, none of those programs are holding up any
# other programs, and are all the tops of their own towers. (The actual tower balancing in front of you is much larger.)
#
# Before you're ready to help them, you need to make sure your information is correct. What is the name of the
# bottom program?

# Prepare libs
import time

# Functions
def tower_index_by_name(name, tower_list):
    index = -1
    for i in range(0, len(tower_list)):
        if tower_list[i]['Name'] == name:
            index = i

    return index

# Prepare input
start = time.time()
f = open('../Input/Day7-A.txt', 'r')

# Process
towers = []

# Build towers (nodes)
for input_line in f:
    input_data = input_line.split()

    tower = {'Name': input_data[0], 'Weight': int(input_data[1][1:-1]), 'Children': [], 'Parent': None}
    if len(input_data) > 2:
        for i in range(3,len(input_data)):
            child = {'Name': input_data[i]}
            tower['Children'].append(input_data[i].replace(",", ""))

    towers.append(tower)

# Connect towers (nodes)
for tower in towers:
    if len(tower['Children']) > 0:
        for child in tower['Children']:
            child_index = tower_index_by_name(child, towers)
            # child['Node'] = towers[child_index]
            towers[child_index]['Parent'] = tower.get('Name')

# Get bottom tower
botton_tower = None
for tower in towers:
    if tower.get('Parent') == None:
        botton_tower = tower
        break

print("##--RESULT--##")
print("Bottom tower: " + str(botton_tower.get('Name')))

# Execution time
end = time.time()
print(end - start)
