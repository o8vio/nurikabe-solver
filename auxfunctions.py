def line_to_list(line):
    
    list = []
    
    current = 0    
    while current < len(line):
        
        if not line[current] == '\n':
            list.append(line[current])
        current += 1
        
    return list


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
        dimensions = 0, 0
    else:
        dimensions = len(matrix), len(matrix[0])
    return dimensions


def walls_in_matrix(matrix):

    matrix_dims = dimensions(matrix)
    count, current_row = 0, 0    
    
    while current_row < matrix_dims[0]:
        
        current_column = 0
        while current_column < matrix_dims[1]:
            
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

    matrix_dims = dimensions(matrix)
    contains = False
    current_row = 0
    
    while current_row < matrix_dims[0] - 1 and not contains:
        
        current_column = 0
        while current_column < matrix_dims[1] - 1 and not contains:

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
            current_cell = matrix[current_position[0]][current_position[1]]
            
            if is_valid_position(current_position, dims):
                
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

def encontrar_pared(matriz):
#Devuelve la posición de una pared de matriz.
#Pre: matriz contiene por lo menos una pared.
    dimensiones, hay_pared = calcular_dimensiones(matriz), False
    fila = 0
    while fila < dimensiones[0] and not hay_pared:
        columna = 0
        while columna < dimensiones[1] and not hay_pared:
            if matriz[fila][columna] == '#':
                pared = (fila, columna)
                hay_pared = True
            columna = columna + 1
        fila = fila + 1
    return pared

def cantidad_componente_paredes(matriz):
#Pre: matriz tiene por lo menos una pared.
#De forma muy similar a lo hecho en es_isla_valida, construimos la componente
#conexa de una pared inicial de la matriz.
    dimensiones = calcular_dimensiones(matriz)
    pared_inicial = encontrar_pared(matriz)
    componente = [pared_inicial]
    matriz[pared_inicial[0]][pared_inicial[1]] = '.'
    completa, checkpoint = False, 0
    while not completa:
        adyacentes = cruz(componente[checkpoint])
        checkpoint = checkpoint + 1
        i = 0
        while i < 4:
            if es_valida_en_rango(adyacentes[i], dimensiones) and matriz[adyacentes[i][0]][adyacentes[i][1]] == '#':
                componente.append(adyacentes[i])
                matriz[adyacentes[i][0]][adyacentes[i][1]] = '.'
            i = i + 1
        if checkpoint == len(componente):
            completa = True
    return len(componente)

def sumar_numeros(matriz):
#Pre: matriz corresponde al atributo matriz de una instancia del TAD Grilla.
    dimensiones = calcular_dimensiones(matriz)
    suma, fila = 0, 0
    while fila < dimensiones[0]:
        columna = 0
        while columna < dimensiones[1]:
            if matriz[fila][columna] != '#' and matriz[fila][columna] != '.':
                suma = suma + int(matriz[fila][columna])
            columna = columna + 1
        fila = fila + 1
    return suma
