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
# --- Part Two ---
# The programs explain the situation: they can't get down. Rather, they could get down, if they weren't expending all
# of their energy trying to keep the tower balanced. Apparently, one program has the wrong weight, and until it's
# fixed, they're stuck here.
#
# For any program holding a disc, each program standing on that disc forms a sub-tower. Each of those sub-towers are
# supposed to be the same weight, or the disc itself isn't balanced. The weight of a tower is the sum of the weights
# of the programs in that tower.
#
# In the example above, this means that for ugml's disc to be balanced, gyxo, ebii, and jptl must all have the same
# weight, and they do: 61.
#
# However, for tknk to be balanced, each of the programs standing on its disc and all programs above it must each
# match. This means that the following sums must all be the same:
#
# ugml + (gyxo + ebii + jptl) = 68 + (61 + 61 + 61) = 251
# padx + (pbga + havc + qoyq) = 45 + (66 + 66 + 66) = 243
# fwft + (ktlj + cntj + xhth) = 72 + (57 + 57 + 57) = 243
# As you can see, tknk's disc is unbalanced: ugml's stack is heavier than the other two. Even though the nodes above
# ugml are balanced, ugml itself is too heavy: it needs to be 8 units lighter for its stack to weigh 243 and keep the
# towers balanced. If this change were made, its weight would be 60.
#
# Given that exactly one program is the wrong weight, what would its weight need to be to balance the entire tower?

# Prepare libs
import time

# Functions
def tower_index_by_name(name, tower_list):
    index = -1
    for i in range(0, len(tower_list)):
        if tower_list[i]['Name'] == name:
            index = i

    return index


def tower_by_name(name, tower_list):
    index = -1
    for i in range(0, len(tower_list)):
        if tower_list[i]['Name'] == name:
            index = i

    return tower_list[index]


def calculate_children_weight(tower, tower_list):
    children_weight = 0
    for child_name in tower.get('Children'):
        child = tower_by_name(child_name, tower_list)

        child['Children weight'] = calculate_children_weight(child, tower_list)
        child['Total weight'] = child['Weight'] + child['Children weight']

        children_weight += child['Total weight']

    return children_weight


def calculate_balance_weight(tower, tower_list):
    balance_weight = 0
    processed_children_number = 0

    first_unique_child = None
    second_unique_child = None
    unbalanced_tower = None
    balanced_tower = None

    for child_name in tower.get('Children'):
        child = tower_by_name(child_name, tower_list)

        if processed_children_number == 0:
            # First child is always saved in first unique
            first_unique_child = child
            processed_children_number += 1
        elif processed_children_number == 1:
            # Saved second child in second unique if it's value differs from first unique
            if first_unique_child.get('Total weight') != child.get('Total weight'):
                second_unique_child = child
            processed_children_number += 1
        else:
            # If both unique values are found then current child will detect unbalanced tower
            if second_unique_child is None:
                # If total weight of first unique is equals to current child, then search further.
                # Otherwise child is unbalanced
                if first_unique_child.get('Total weight') == child.get('Total weight'):
                    pass
                else:
                    unbalanced_tower = child
                    balanced_tower = first_unique_child
            else:
                # If first unique TW equals to child TW then second unique is unbalanced.
                # Otherwise first unique is unbalanced
                if first_unique_child.get('Total weight') == child.get('Total weight'):
                    unbalanced_tower = second_unique_child
                    balanced_tower = first_unique_child
                else:
                    unbalanced_tower = first_unique_child
                    balanced_tower = second_unique_child
            processed_children_number += 1

        # If unbalanced tower is found break the loop. No more search is required.
        if unbalanced_tower:
            break

    if unbalanced_tower:
        balance_result = calculate_balance_weight(unbalanced_tower, tower_list)
        if balance_result == 0:
            difference = unbalanced_tower.get('Total weight') - balanced_tower.get('Total weight')
            balance_weight = unbalanced_tower.get('Weight') - difference
        else:
            balance_weight = balance_result

    return balance_weight


# Prepare input
start = time.time()
f = open('../Input/Day7.txt', 'r')

# Process
towers = []

# Build towers (nodes)
for input_line in f:
    input_data = input_line.split()

    tower = {'Name': input_data[0], 'Weight': int(input_data[1][1:-1]), 'Children weight': None, 'Total weight': None,
             'Children': [], 'Parent': None}
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
            towers[child_index]['Parent'] = tower.get('Name')

# Get bottom tower
bottom_tower = None
for tower in towers:
    if tower.get('Parent') == None:
        bottom_tower = tower
        break

bottom_tower['Children weight'] = calculate_children_weight(bottom_tower, towers)
bottom_tower['Total weight'] = bottom_tower['Weight'] + bottom_tower['Children weight']

# Obtain tower weight for balance
balance_weight = calculate_balance_weight(bottom_tower, towers)

print("##--RESULT--##")
print("Weight needed for balance: " + str(balance_weight))

# Execution time
end = time.time()
print(end - start)