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

def es_valida_en_rango(posicion, dimensiones):
    rv = False
    if 0 <= posicion[0] < dimensiones[0] and 0 <= posicion[1] < dimensiones[1]:
        rv = True
    return rv

def copiar(matriz):
    dimensiones = calcular_dimensiones(matriz)
    copia, fila = [], 0
    while fila < dimensiones[0]:
        copia.append([])
        columna = 0
        while columna < dimensiones[1]:
            copia[fila].append(matriz[fila][columna])
            columna = columna + 1
        fila = fila + 1
    return copia

def cruz(posicion):
#Devuelve la lista de posiciones adyacentes a la posición dada.
#Obs: puede devolver posiciones con coordenadas negativas o que se excedan
#de las dimensiones de la matriz que se esté considerando, pero estas serán
#posteriormente descartadas usando la función es_valida_en_rango.
    lista = []
    lista.append((posicion[0]+1,posicion[1]))
    lista.append((posicion[0]-1,posicion[1]))
    lista.append((posicion[0],posicion[1]+1))
    lista.append((posicion[0],posicion[1]-1))
    return lista

def es_isla_valida(matriz, isla):
#Pre: matriz corresponde al atributo matriz de una instancia del TAD Grilla. 
#‘isla’ es una lista que contiene la posición del número que se analizará 
#para determinar si forma o no una isla válida.
#Para esto, vamos agregando posiciones adyacentes que tengan '.' mientras 
#sea posible, y cambiamos su simbolo por '#' para no volver a analizarlas.
    dimensiones = calcular_dimensiones(matriz)
    numero = int(matriz[isla[0][0]][isla[0][1]])
    es_valida, checkpoint, completa = True, 0, False
    matriz[isla[0][0]][isla[0][1]] = '#'
    while not completa and es_valida:
        adyacentes = cruz(isla[checkpoint])
        checkpoint = checkpoint + 1
        i = 0
        while i < 4 and es_valida:
            if es_valida_en_rango(adyacentes[i], dimensiones):
                if matriz[adyacentes[i][0]][adyacentes[i][1]] == '.':
                    isla.append(adyacentes[i])
                    matriz[adyacentes[i][0]][adyacentes[i][1]] = '#'
                elif matriz[adyacentes[i][0]][adyacentes[i][1]] == '#':
                    pass
                else:
                    #si encontramos otro número en la isla, detenemos
                    #la construcción de la misma y devolvemos Falso
                    es_valida = False
            i = i + 1
        if len(isla) > numero:
            #también detenemos la construcción de la isla si su tamaño excede 
            #el de una isla válida
            es_valida = False
        if checkpoint == len(isla):
            completa = True
    if len(isla) < numero:
        es_valida = False
    return es_valida

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
