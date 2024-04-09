class Grilla:
    def __init__(self, nombre_archivo):
        if nombre_archivo == None:
        # Esto es solo para poder hacer clones y responder correctamente 
        # a la especificación de resolver_nurikabe.
            self.matriz = []
            self.dimensiones = (0, 0)
            self.cantidad_paredes = 0
            self.hay_2x2_paredes = False
            self.suma_numeros = 0
            self.cantidad_permitida_paredes = 0
        else:
            self.matriz = convertir(nombre_archivo)
            self.dimensiones = calcular_dimensiones(self.matriz)
            self.cantidad_paredes = contar_paredes(self.matriz)
            self.hay_2x2_paredes = buscar_2x2_paredes(self.matriz)
            self.suma_numeros = sumar_numeros(self.matriz)
            self.cantidad_permitida_paredes = self.dimensiones[0]*self.dimensiones[1] - self.suma_numeros

    def es_posicion_valida(self, pos):
        return es_valida_en_rango(pos, self.dimensiones)
    
    def es_numero(self, pos):
        simbolo = self.matriz[pos[0]][pos[1]]
        esNumero = True
        if simbolo == '#' or simbolo == '.':
            esNumero = False
        return esNumero
    
    def es_pared(self, pos):
        simbolo = self.matriz[pos[0]][pos[1]]
        esPared = False
        if simbolo == '#':
            esPared = True
        return esPared
    
    def valor(self, pos):
        return int(self.matriz[pos[0]][pos[1]])
    
    def alto(self):
        return self.dimensiones[0]
     
    def ancho(self):
        return self.dimensiones[1]
    
    def cantidad_no_paredes(self):
        cantidad = self.ancho()*self.alto() - self.cantidad_paredes
        return cantidad
    
    def hay_cuadrado(self):
        return self.hay_2x2_paredes
    
    def listar_numeros(self):
        lista, fila = [], 0
        while fila < self.dimensiones[0]:
            columna = 0
            while columna < self.dimensiones[1]:
                if self.es_numero((fila,columna)):
                    lista.append((fila, columna))
                columna = columna + 1
            fila = fila + 1
        return lista
    
    def islas_validas(self):
        #Trabajamos sobre una copia de la matriz para no modificar el atributo.
        copia = copiar(self.matriz)
        numeros = self.listar_numeros()
        son_validas, i = True, 0
        while i < len(numeros) and son_validas:
            isla = []
            isla.append(numeros[i])
            son_validas = es_isla_valida(copia, isla)
            i = i + 1
        return son_validas
    
    def pared_conexa(self):
        copia = copiar(self.matriz)
        if self.cantidad_paredes == 0:
            es_conexa = True
        else:
        #Comparamos la cantidad total de paredes con la de la componente conexa
        #de una pared cualquiera.
            es_conexa = cantidad_componente_paredes(copia) == self.cantidad_paredes
        return es_conexa
 
    def listar_blancas(self):
        #Listamos las posiciones que contienen "."
        lista_de_blancas = []
        fila = 0 
        while fila < self.dimensiones[0]:
            columna = 0
            while columna < self.dimensiones[1]:
                if not self.es_pared((fila,columna)) and not self.es_numero((fila,columna)):
                    lista_de_blancas.append((fila,columna))
                columna = columna + 1
            fila = fila + 1
        return lista_de_blancas
    
    def generar_clon(self):
        clon = Grilla(None)
        clon.matriz = copiar(self.matriz)
        clon.dimensiones = self.dimensiones
        clon.cantidad_paredes = self.cantidad_paredes
        clon.hay_2x2_paredes = self.hay_2x2_paredes
        clon.suma_numeros = self.suma_numeros
        clon.cantidad_permitida_paredes = self.cantidad_permitida_paredes
        return clon
    
    def poner_pared(self, posicion):
        #Pre: La grilla no contiene cuadrados de 2x2 de paredes.        
        #Además, las posiciones inmediata a la derecha e inmediata abajo 
        #de la dada, de ser válidas, no son paredes.
        #(Podemos asumir esto por la forma en que recorremos las posiciones 
        #al hacer backtracking.)
        if not self.es_pared(posicion):
            self.matriz[posicion[0]][posicion[1]] = '#'
            self.cantidad_paredes = self.cantidad_paredes + 1
            if self.es_posicion_valida((posicion[0]-1,posicion[1]-1)):
                cuadrado = cuadrado2x2((posicion[0]-1,posicion[1]-1))
                self.hay_2x2_paredes = son_paredes(cuadrado, self.matriz)
    
    def sacar_pared(self, posicion):
        #Pre: La grilla no contiene cuadrados de 2x2 de paredes excepto, quizás,
        #el cuadrado cuya esquina inferior derecha es la posición dada.
        if self.es_pared(posicion):
            self.matriz[posicion[0]][posicion[1]] = '.'
            self.cantidad_paredes = self.cantidad_paredes - 1
            self.hay_2x2_paredes = False
 
    def es_solucion_valida(self):
        return self.islas_validas() and self.pared_conexa() and not self.hay_2x2_paredes and self.cantidad_paredes == self.cantidad_permitida_paredes
    
    def resolver_nurikabe_con_backtracking(self, blancas, contador):
        if contador == len(blancas):
            resultado = False
        else:
            self.poner_pared(blancas[contador])
            if self.hay_2x2_paredes:
                resultado = False
            elif self.cantidad_paredes == self.cantidad_permitida_paredes:
                resultado = self.es_solucion_valida()
            else:
                resultado = self.resolver_nurikabe_con_backtracking(blancas, contador + 1)
            if not resultado:
                self.sacar_pared(blancas[contador])
                resultado = self.resolver_nurikabe_con_backtracking(blancas, contador + 1)
        return resultado
    
    def resolver_nurikabe(self, nombre_archivo_salida):
        #Clonamos la grilla, para no modificar la original.
        clon = self.generar_clon()
        archivo_a_crear = open(nombre_archivo_salida, 'w')
        blancas = clon.listar_blancas()
        if clon.resolver_nurikabe_con_backtracking(blancas, 0):
            grilla_a_devolver = clon
            fila = 0
            while fila < clon.dimensiones[0]:
                columna = 0
                while columna < clon.dimensiones[1]:
                    archivo_a_crear.write(clon.matriz[fila][columna])
                    columna = columna + 1
                if fila < clon.dimensiones[0] - 1:
                    archivo_a_crear.write('\n')
                fila = fila + 1
        else:
            grilla_a_devolver = Grilla(None)
            print('La grilla dada no tiene solución. \n')
        return grilla_a_devolver