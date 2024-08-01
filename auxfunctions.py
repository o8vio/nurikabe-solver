def line_to_list(line):

    rv_list = []

    current = 0
    while current < len(line):

        if not line[current] == '\n':
            rv_list.append(line[current])
        current += 1

    return rv_list


def text_to_matrix(text_file):

    read = open(text_file, 'r')
    lines_list = read.readlines()
    matrix = []
    current_line = 0

    while current_line < len(lines_list):

        line_list = line_to_list(lines_list[current_line])
        matrix.append(line_list)
        current_line += 1

    return matrix


def dimensions(matrix):
    if len(matrix) == 0:
        dims = 0, 0
    else:
        dims = len(matrix), len(matrix[0])
    return dims


def walls_in_matrix(matrix):

    dims = dimensions(matrix)
    count, current_row = 0, 0

    while current_row < dims[0]:

        current_column = 0
        while current_column < dims[1]:

            if matrix[current_row][current_column] == '#':
                count += 1

            current_column += 1
        current_row += 1

    return count


def square2x2(position):
    square = [position]
    square.append((position[0]+1, position[1]))
    square.append((position[0], position[1]+1))
    square.append((position[0]+1, position[1]+1))
    return square


def walls(positions, matrix):

    walls = True
    current_pos = 0

    while current_pos < len(positions) and walls:

        if matrix[positions[current_pos][0]][positions[current_pos][1]] != '#':
            walls = False
        current_pos += 1

    return walls


def contains_2x2wall(matrix):

    dims = dimensions(matrix)
    contains = False
    current_row = 0

    while current_row < dims[0] - 1 and not contains:

        current_column = 0
        while current_column < dims[1] - 1 and not contains:

            if walls(square2x2((current_row, current_column)), matrix):
                contains = True

            current_column += 1
        current_row += 1

    return contains


def is_valid_position(position, dims):
    return 0 <= position[0] < dims[0] and 0 <= position[1] < dims[1]


def clone_matrix(matrix):

    dims = dimensions(matrix)
    clone, current_row = [], 0

    while current_row < dims[0]:

        clone.append([])

        current_column = 0
        while current_column < dims[1]:

            clone[current_row].append(matrix[current_row][current_column])

            current_column += 1
        current_row += 1

    return clone


def cross(position):
    cross = []
    cross.append((position[0]+1, position[1]))
    cross.append((position[0]-1, position[1]))
    cross.append((position[0], position[1]+1))
    cross.append((position[0], position[1]-1))
    return cross


def is_valid_island(matrix, island):

    dims = dimensions(matrix)
    number = int(matrix[island[0][0]][island[0][1]])
    is_valid, checkpoint, complete = True, 0, False
    matrix[island[0][0]][island[0][1]] = '#'

    while not complete and is_valid:

        adjacent_positions = cross(island[checkpoint])
        checkpoint += 1
        current = 0

        while current < len(adjacent_positions) and is_valid:

            current_position = adjacent_positions[current]

            if is_valid_position(current_position, dims):

                current_cell = matrix[current_position[0]][current_position[1]]

                if current_cell == '.':
                    island.append(current_position)
                    matrix[current_position[0]][current_position[1]] = '#'

                elif current_cell == '#':
                    pass

                else:
                    is_valid = False

            current += 1

        if len(island) > number:
            is_valid = False

        if checkpoint == len(island):
            complete = True

    if len(island) < number:
        is_valid = False

    return is_valid


def find_wall(matrix):

    dims, found = dimensions(matrix), False
    current_row = 0

    while current_row < dims[0] and not found:

        current_column = 0
        while current_column < dims[1] and not found:

            if matrix[current_row][current_column] == '#':
                wall = (current_row, current_column)
                found = True

            current_column += 1
        current_row += 1

    return wall


def connected_wall_size(matrix):

    dims = dimensions(matrix)

    init_wall = find_wall(matrix)
    connected_wall = [init_wall]

    matrix[init_wall[0]][init_wall[1]] = '.'

    complete, checkpoint = False, 0
    while not complete:

        adjacent_positions = cross(connected_wall[checkpoint])
        checkpoint += 1
        current = 0

        while current < 4:

            current_position = adjacent_positions[current]
            if is_valid_position(current_position, dims) and matrix[current_position[0]][current_position[1]] == '#':
                connected_wall.append(current_position)
                matrix[current_position[0]][current_position[1]] = '.'

            current += 1

        if checkpoint == len(connected_wall):
            complete = True

    return len(connected_wall)


def numbers_sum(matrix):

    dims = dimensions(matrix)
    rv_sum, current_row = 0, 0
    while current_row < dims[0]:

        current_column = 0
        while current_column < dims[1]:

            if matrix[current_row][current_column] != '#' and matrix[current_row][current_column] != '.':
                rv_sum += int(matrix[current_row][current_column])

            current_column += 1
        current_row += 1

    return rv_sum
