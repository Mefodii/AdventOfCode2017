# --- Part Two ---
# As a stress test on the system, the programs here clear the grid and then store the value 1 in square 1.
# Then, in the same allocation order as shown above, they store the sum of the values in all adjacent squares,
# including diagonals.
#
# So, the first few squares' values are chosen as follows:
#
# Square 1 starts with the value 1.
# Square 2 has only one adjacent filled square (with value 1), so it also stores 1.
# Square 3 has both of the above squares as neighbors and stores the sum of their values, 2.
# Square 4 has all three of the aforementioned squares as neighbors and stores the sum of their values, 4.
# Square 5 only has the first and fourth squares as neighbors, so it gets the value 5.
# Once a square is written, its value does not change. Therefore, the first few squares would receive the
# following values:
#
# 147  142  133  122   59
# 304    5    4    2   57
# 330   10    1    1   54
# 351   11   23   25   26
# 362  747  806--->   ...
# What is the first value written that is larger than your puzzle input?
#
# Your puzzle input is still 312051.

# Prepare input

f = open('../Input/Day3-B.txt', 'r')


# Process
def position_to_coords(element_position, matrix_range):
    # Standard mathematical XY axes orientation was chosen.
    # Value 1 is located at the center of the matrix. (Both X and Y positive values)
    current_x = 0
    current_y = 0
    if element_position >= 0:
        # Calculate coordinates for current number
        if 0 <= element_position < matrix_range - 2:
            current_x = matrix_range - 1
            current_y = element_position + 1
        elif matrix_range - 2 <= element_position < matrix_range * 2 - 2:
            current_x = 2 * matrix_range - element_position - 3
            current_y = matrix_range - 1
        elif matrix_range * 2 - 2 <= element_position < matrix_range * 3 - 4:
            current_x = 0
            current_y = 3 * matrix_range - element_position - 4
        else:
            current_x = element_position - (3 * matrix_range - 4)
            current_y = 0

    return {'X': current_x, 'Y': current_y}


def coords_to_element_index(coordinates, current_range):
    if current_range == 1:
        return 0
    else:
        # Calculate position on edge for current coordinates
        if coordinates['X'] == current_range - 1:
            if coordinates['Y'] == 0:
                current_position = current_range * 4 - 5
            else:
                current_position = coordinates['Y'] - 1
        elif coordinates['X'] == 0:
            current_position = current_range * 3 - 4 - coordinates['Y']
        elif coordinates['Y'] == 0:
            current_position = current_range * 3 - 4 + coordinates['X']
        else:
            current_position = current_range * 2 - 3 - coordinates['X']

        # Convert calculated position on edge to index
        prev_range = current_range - 2
        current_index = prev_range ** 2 + current_position
        print("COOR - " + str(coordinates), end=' ')
        print("POS - " + str(current_position), "IND - " + str(current_index), "RAN - " + str(current_range))

        return current_index


def get_adjacent_indexes(element_coordinates, element_range):
    indexes = []
    up = True
    down = True
    right = True
    left = True

    # PROBABLY START FIX HERE
    if element_coordinates['X'] == element_range - 1:
        right = False
    if element_coordinates['X'] == 0:
        left = False
    if element_coordinates['Y'] == element_range - 1:
        up = False
    if element_coordinates['Y'] == 0:
        down = False

    if up:
        results = move_coordinates("U", element_coordinates, element_range)
        res_coord = results[0]
        res_range = element_range - results[1]
        indexes.append(coords_to_element_index(res_coord, res_range))
    if down:
        results = move_coordinates("D", element_coordinates, element_range)
        res_coord = results[0]
        res_range = element_range - results[1]
        indexes.append(coords_to_element_index(res_coord, res_range))
    if right:
        results = move_coordinates("R", element_coordinates, element_range)
        res_coord = results[0]
        res_range = element_range - results[1]
        indexes.append(coords_to_element_index(res_coord, res_range))
    if left:
        results = move_coordinates("L", element_coordinates, element_range)
        res_coord = results[0]
        res_range = element_range - results[1]
        indexes.append(coords_to_element_index(res_coord, res_range))
    if up and right:
        results = move_coordinates("UR", element_coordinates, element_range)
        res_coord = results[0]
        res_range = element_range - results[1]
        indexes.append(coords_to_element_index(res_coord, res_range))
    if up and left:
        results = move_coordinates("UL", element_coordinates, element_range)
        res_coord = results[0]
        res_range = element_range - results[1]
        indexes.append(coords_to_element_index(res_coord, res_range))
    if down and right:
        results = move_coordinates("DR", element_coordinates, element_range)
        res_coord = results[0]
        res_range = element_range - results[1]
        indexes.append(coords_to_element_index(res_coord, res_range))
    if down and left:
        results = move_coordinates("DL", element_coordinates, element_range)
        res_coord = results[0]
        res_range = element_range - results[1]
        indexes.append(coords_to_element_index(res_coord, res_range))

    # Debug variables
    print("UP = " + str(up), "DOWN = " + str(down), "RIGHT = " + str(right), "LEFT = " + str(left), sep='\t')
    print("X = " + str(element_coordinates['X']), "Y = " + str(element_coordinates['Y']), sep='\t')
    print(indexes)

    return indexes


def move_coordinates(direction, coordinates, element_range):
    next_coordinates = coordinates.copy()
    shrink = 0

    if direction == "U":
        if 0 < next_coordinates['X'] < element_range - 1:
            next_coordinates['X'] = next_coordinates['X'] - 1
            shrink = 2
        else:
            next_coordinates['Y'] = next_coordinates['Y'] + 1
    if direction == "D":
        if 0 < next_coordinates['X'] < element_range - 1:
            next_coordinates['X'] = next_coordinates['X'] - 1
            next_coordinates['Y'] = next_coordinates['Y'] - 2
            shrink = 2
        else:
            next_coordinates['Y'] = next_coordinates['Y'] - 1
    if direction == "R":
        if 0 < next_coordinates['Y'] < element_range - 1:
            next_coordinates['Y'] = next_coordinates['Y'] - 1
            shrink = 2
        else:
            next_coordinates['X'] = next_coordinates['X'] + 1
    if direction == "L":
        if 0 < next_coordinates['Y'] < element_range - 1:
            next_coordinates['X'] = next_coordinates['X'] - 2
            next_coordinates['Y'] = next_coordinates['Y'] - 1
            shrink = 2
        else:
            next_coordinates['X'] = next_coordinates['X'] - 1

    if direction == "UR":
        if next_coordinates['Y'] == element_range - 2 or (next_coordinates['Y'] == 0 and next_coordinates['X'] == element_range - 2):
            next_coordinates['Y'] = next_coordinates['Y'] + 1
            next_coordinates['X'] = next_coordinates['X'] + 1
        else:
            shrink = 2
    if direction == "UL":
        if next_coordinates['Y'] == element_range - 2 or (next_coordinates['Y'] == 0 and next_coordinates['X'] == 1):
            next_coordinates['Y'] = next_coordinates['Y'] + 1
            next_coordinates['X'] = next_coordinates['X'] - 1
        else:
            next_coordinates['X'] = next_coordinates['X'] - 2
            shrink = 2
    if direction == "DR":
        if next_coordinates['X'] == element_range - 2 or (next_coordinates['X'] == 0 and next_coordinates['Y'] == 1):
            next_coordinates['Y'] = next_coordinates['Y'] - 1
            next_coordinates['X'] = next_coordinates['X'] + 1
        else:
            next_coordinates['Y'] = next_coordinates['Y'] - 2
            shrink = 2
    if direction == "DL":
        if next_coordinates['X'] == 1 or (next_coordinates['Y'] == 1 and next_coordinates['X'] == element_range - 1):
            next_coordinates['Y'] = next_coordinates['Y'] - 1
            next_coordinates['X'] = next_coordinates['X'] - 1
        else:
            next_coordinates['Y'] = next_coordinates['Y'] - 2
            next_coordinates['X'] = next_coordinates['X'] - 2
            shrink = 2

    return next_coordinates, shrink


def calculate_position(element_index, element_range):
    return element_index - ((element_range - 2) ** 2)


def calculate_range(value):
    border_range = 3
    while border_range ** 2 - 1 < value:
        border_range += 2
    return border_range


def calculate_next_value(values):

    print("##--DEBUG--##")
    element_index = len(values)
    element_range = calculate_range(element_index)

    # Calculate position of the element
    element_position = calculate_position(element_index, element_range)
    element_coordinates = position_to_coords(element_position, element_range)

    # Get indexes of adjacent elements (if exists)
    adjacent_indexes = get_adjacent_indexes(element_coordinates, element_range)

    # Calculate value for the value
    element_value = 0
    for index in adjacent_indexes:
        if index < element_index:
            element_value += values[index]

    # Debug variables
    print("Element index = " + str(element_index))
    print("Element position = " + str(element_position))
    print("Element range = " + str(element_range))
    print("Element coordinates = " + str(element_coordinates))
    print("Inserted value = " + str(element_value))
    print()
    return element_value


for square in f:
    values_list = [1]
    targetValue = int(square)

    while values_list[-1] < targetValue:
        values_list.append(calculate_next_value(values_list))

    print("##--RESULT--##")
    print("Next value is: " + str(values_list[-1]))
