def linea_a_lista(linea):
    lista = []
    contador = 0
    while contador < len(linea):
        if not linea[contador] == '\n':
            lista.append(linea[contador])
        contador = contador + 1
    return lista

def convertir(archivo):
#Convierte un archivo de texto a una lista de listas. 
    lectura = open(archivo, 'r')
    lista_de_lineas = lectura.readlines()
    matriz = []
    fila = 0
    while fila < len(lista_de_lineas):
        matriz.append([])
        elementos_fila = linea_a_lista(lista_de_lineas[fila])
        columna = 0
        while columna < len(elementos_fila):
            matriz[fila].append(elementos_fila[columna])
            columna = columna + 1
        fila = fila + 1
    return matriz

def calcular_dimensiones(matriz):
    if len(matriz) == 0:
        dimensiones = 0, 0
    else:
        dimensiones = len(matriz), len(matriz[0])
    return dimensiones

def paredes_en_fila(fila):
#Cuenta la cantidad de apariciones del elemento '#' en fila.
    cantidad, columna = 0, 0
    while columna < len(fila):
        if fila[columna] == '#':
            cantidad = cantidad + 1
        columna = columna + 1
    return cantidad

def contar_paredes(matriz):
#Cuenta la cantidad de apariciones del elemento '#' en la matriz dada.
    cantidad, fila = 0, 0
    while fila < len(matriz):
        cantidad = cantidad + paredes_en_fila(matriz[fila])
        fila = fila + 1
    return cantidad

def cuadrado2x2(posicion):
#Devuelve la lista de posiciones que forman el cuadrado 
#cuya esquina superior izquierda es la posición dada.
    cuadrado = [posicion]
    cuadrado.append((posicion[0]+1,posicion[1]))
    cuadrado.append((posicion[0],posicion[1]+1))
    cuadrado.append((posicion[0]+1,posicion[1]+1))
    return cuadrado

def son_paredes(posiciones, matriz):
#Pre: ‘posiciones’ es una lista de posiciones válidas en ‘matriz’
    son_paredes = True
    i = 0
    while i < len(posiciones) and son_paredes:
        if matriz[posiciones[i][0]][posiciones[i][1]] != '#':
            son_paredes = False
        i = i + 1
    return son_paredes

def buscar_2x2_paredes(matriz):
#Devuelve True si y solo si matriz contiene un cuadrado de 2x2 de paredes.
#Para eso, recorremos todas las posiciones que son paredes y son esquinas 
#superiores de un cuadrado de 2x2, y nos fijamos si ese cuadrado es de paredes.
    dimensiones = calcular_dimensiones(matriz)
    hay_cuadrado = False
    fila = 0
    while fila < dimensiones[0] - 1 and not hay_cuadrado:
        columna = 0
        while columna < dimensiones[1] - 1 and not hay_cuadrado:
            if matriz[fila][columna] == '#' and son_paredes(cuadrado2x2((fila, columna)), matriz):
                hay_cuadrado = True
            columna = columna + 1
        fila = fila + 1
    return hay_cuadrado

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