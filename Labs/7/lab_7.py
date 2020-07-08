## Alumno:
## Renato Luis Postigo Avalos

'''
E  := T Ep
Ep := + T Ep 
Ep := - T Ep
Ep := lambda
T  := F Tp
Tp := * F Tp  |  /  F Tp  | lambda
F  := ( E ) | num | id
'''

### Arbol sintáctico ###

class Nodo:
    etiqueta = ''
    hijos = list() # lista de referencias a los nodos hijos
    padre = None
    siguiente = None # hermano

    def __init__(self, label):
        self.etiqueta = label


def opera1(pivote, literales):
    # adicionar cada literal al nodo pivote
    for cur_child in range(len(literales)):
        pivote.hijos.append(Nodo(literales[cur_child]))
    # hermanos
    for cur_child in range(len(literales)-1):
        pivote.hijos[cur_child].siguiente = pivote.hijos[cur_child]
    # retornar referencia al primer hijo (por la izq)
    return pivote.hijos[0]

def opera2(pivote):
    # retornar referencia al siguiente hermano
    if pivote.siguiente is not None:
        return pivote.siguiente
    # si no hay: retornar siguiente del hermano del padre
    if pivote.padre is not None:
    # si no hay continuar hasta encontrar
        return opera2(pivote.padre)
    # un hermano o el nodo raiz
    # en el ultimo caso retornar vacio (None)
    return None

def opera3(pivote):
    # adicionar el operador lambda en el nodo donde se encuentre
    pivote.hijos.append('lambda')
    # retornar opera2(pivote)
    return opera2(pivote)

#########################
# Funcion para validar  #
# validate_str(), linea #
#         377           #
#########################

class Produccion:

    def __init__(self, texto):
        # Separar izquierda de derecha
        split_result = texto.split(':=')
        self.left = split_result[0].strip()

        total_rules = split_result[1].split('|')
        self.right = [rule.strip() for rule in total_rules]

    def __str__(self):
        return self.left + ' := ' + str(self.right)

class TablaSintactica:

    def __init__(self):
        self.tabla = dict()
        self.PADDING = 8
        self.terminales = {'$', 'lambda'}
        self.noterminales = set()
    
    def insertar(self, noterminal, terminal, value):
        if noterminal not in self.tabla:
            # si no existe, crearlo
            self.tabla[noterminal] = dict()
            self.noterminales.add(noterminal)
        # Insertar arreglo en la entrada    
        self.tabla[noterminal][terminal] = value
        self.terminales.add(terminal)
    
    # print(tablaSintactica)
    def __str__(self):
        ret_str = ''
        # Todos los strings tienen len=padding
        # Para que se vea ordenado
        ret_str += " ".ljust(self.PADDING)
        # Imprimir terminales arriba
        terminal_list = list(self.terminales)
        for term in terminal_list:
            ret_str += term.ljust(self.PADDING)

        ret_str += '\n'

        # Recorriendo tabla
        for non_term in list(self.noterminales):
            # Imprimir no terminal a la izquierda
            ret_str += non_term.ljust(self.PADDING)
            for term in terminal_list:
                # Si no hay valor en la casilla
                # Imprimir vacío
                if term not in self.tabla[non_term]:
                    ret_str += " ".ljust(self.PADDING)
                else:
                    # Imprimir produccion si hay valor
                    produccion = ""
                    for value in self.tabla[non_term][term]:
                        produccion += value
                    ret_str += produccion.ljust(self.PADDING)
            ret_str += '\n'
        
        return ret_str

class Gramatica:
    # Impresion de la tabla
    PADDING = 8
    producciones = []
    # Ventaja de usar lista:
    # poder meter más de una vez de manera sencilla
    # producción que empieza
    # con el mismo no terminal, ej (uno después del otro):
    # Gramatica.cargar("Ep := A|B")
    # Gramatica.cargar("Ep := C|D")
    terminales = set()
    noterminales = set()
    siguientes = None # siguientes de no terminales
    dolar = '$'

    def __init__(self):
        #terminales = ['+', '-', '*', '/', '(', ')', 'num', 'id', '$']
        #noterminales = ['E', 'Ep', 'T', 'Tp', 'F']
        self.nodoInicial = None
        self.tablaSintactica = None
        self.terminales.add('$') # Fin de cadena

    # getIzquierdaFromDerecha:
    # encontrar generador de la izquierda a partir de toda
    # una oracion a la derecha
    def getIzquierdaFromDerecha(self, right_sent):
        # Buscando en todas las producciones
        for produccion in self.producciones:
            # En las derechas
            for right in produccion.right:
                # Si la derecha coincide
                if right.strip() == right_sent.strip():
                    # Hicimos match
                    return produccion.left.replace(' ', '')

    # getProduccion: lado derecho generado por
    # valor a la izquierda (izq)
    def getProduccion(self, izq):
        # Buscando en el conjunto de producciones
        ret_value = list()
        for produccion in self.producciones:
            # Eliminando espacios en blanco
            # En caso sea necesario
            # Si coincide, retornar produccion
            if produccion.left.replace(' ', '') == izq:
                for right in produccion.right:
                    ret_value.append(right)
                
                # No se rompe el bucle porque puede que
                # Un valor a la izquierda tenga múltiples
                # valores a la derecha
        return ret_value

    # get producciones: todos los elementos de la derecha
    # de la gramatica
    def getProducciones(self):
        # retornar elementos de la derecha en forma de una lista
        producciones = list()
        for nodo in self.noterminales:
            producciones.append(self.getProduccion(nodo))
        return producciones

    # Find generator: generar no terminal que genere el valor
    # indicado en right
    def find_generator(self, right):
        # Encontrar no terminales que generen un valor (right)
        generators = set()
        for produccion in self.producciones:
            # values = arreglo de "derechas"
            values = produccion.right
            # value = string de la produccion
            for value in values:
                if right in value:
                    generators.add(produccion.left)
        # Eliminando a si mismo como su generador en caso se encuentre
        if right in generators:
            generators.remove(right)

        return generators

    def buildTerminals(self):
        # Construye conjunto de terminales
        # Y no terminales segun contenido actual de la
        # Gramatica
        for produccion in self.producciones:
            cur_left = produccion.left.replace(' ','')
            # izquierda siempre es no terminal
            if cur_left not in self.noterminales:
                self.noterminales.add(cur_left)

            # eliminamos en caso este en terminales
            if cur_left in self.terminales:
                self.terminales.remove(cur_left)
            
            for cur_right in produccion.right:
                tokens = cur_right.strip().split(' ')
                for token in tokens:
                    if len(token) < 1:
                        continue
                    # si token esta en no terminales
                    # no se mete a terminales
                    if token not in self.noterminales:
                        self.terminales.add(token)

    # Retornar primeros de un no terminal
    def getPrimero(self, izq):
        primeros = list()

        # Buscamos en las producciones 
        for produccion in self.producciones:
            # Hasta encontrar presencia a la izquierda
            if produccion.left.replace(' ', '') == izq:
                # Buscamos en los resultados a la derecha
                for right in produccion.right:
                    # right.strip(): eliminar espacios en blanco
                    # al inicio y al final
                    tokens = right.strip().split(' ')
                    # si primer nodo/token a la derecha es terminal, es primero
                    if tokens[0] in self.terminales:
                        primeros.append(tokens[0])
                    # si no, getprimero a ese nodo
                    else:
                        nt_primeros = self.getPrimero(tokens[0])
                        primeros = primeros + nt_primeros

        return primeros

    def getPrimeros(self):
        # retorna los primeros de cada nodo
        # no terminal de la gramatica
        primeros = dict()
        for nodo in self.noterminales:
            cur_primeros = self.getPrimero(nodo)
            primeros[nodo] = cur_primeros

        return primeros

    def getSiguientes(self):
        siguientes = dict()

        # Inicializar diccionario
        for noterminal in self.noterminales:
            siguientes[noterminal] = set()
        
        siguientes[self.nodoInicial].add(self.dolar)
        to_fill = list() # valores que no tienen nodo a la derecha
        derechas = list() # valores completos a la derecha de aquellos
        # nodos que no tengan nodo a la derecha (hallar generador correcto)

        for nodo in self.getProducciones():
            # nodo: arreglo con valores a la derecha
            # de un no terminal
            for right_prods in nodo:
                #right_prods: string (un valor a la derecha)
                tokens = right_prods.split()
                for i in range(len(tokens)-1):
                    # Si el token actual es terminal, ignorar
                    if tokens[i] in self.terminales:
                        continue
                    
                    # Si el token siguiente es terminal, es el siguiente (?)
                    # Ej: siguientes de E: {$, (, +, -} (sacado de la practicac)
                    if tokens[i+1] in self.terminales:
                        siguientes[tokens[i]].add(tokens[i+1])
                    else:
                        # El siguiente de un nodo es el primero de su derecha
                        primeros = self.getPrimero(tokens[i+1])
                        for primero in primeros:
                            if primero.strip() != 'lambda':
                                siguientes[tokens[i]].add(primero)
                            # Si un primero es el elemento vacío
                            # El siguiente será el siguiente del lado izquierdo
                            # De su produccion original
                            else:
                                # En nuestro caso, guardamos el no terminal
                                # Para actualizarlo posteriormente con su siguiente
                                siguientes[tokens[i]].add(tokens[i+1])

                    # Si el almacenado es un no terminal, se actualizará
                    # Con el siguiente correspondiente (el de ese no terminal)
                    # después
                        
                # Si el ultimo es no terminal, no tiene
                # nadie a su derecha, lo guardamos en la lista
                # to_fill para actualizarlo posteriormente
                # Regla: su siguiente será el siguiente del lado
                # izquierdo de su produccion original
                if tokens[-1] in self.noterminales:
                    # Solo si no tiene elementos en sus siguientes
                    if len(siguientes[tokens[-1]]) < 1:
                       to_fill.append(tokens[-1])
                       derechas.append(right_prods)

        # Llenando no terminales
        # Que no tenían nodo a su derecha
        for i in range(len(to_fill)):
            # Encontrando quien lo genera
            generated_by = self.getIzquierdaFromDerecha(derechas[i])
            # Reemplazando con los siguientes del generador
            siguientes_generator = siguientes[generated_by]
            for siguiente in siguientes_generator:
                siguientes[to_fill[i]].add(siguiente)

        # Actualizando los que tenían un "siguiente"
        # No terminal con los siguientes de dicho
        # No terminal
        for key in siguientes:
            siguientes_key_copy = list(siguientes[key])
            for siguiente in siguientes_key_copy:
                # si uno de los siguientes es un no terminal
                if siguiente in self.noterminales:
                    # metemos los siguientes de ese no terminal
                    for element in siguientes[siguiente]:
                        if element not in siguientes[key]:
                            siguientes[key].add(element)
                    # eliminamos no terminal de los siguientes
                    siguientes[key].remove(siguiente)

        self.siguientes = siguientes
        return siguientes


    def buscar_produccion(self, noterminal, terminal):
        producciones = self.getProduccion(noterminal)
        # Si solo se genera una producción
        # Retornar esa producción
        if (len(producciones) <= 1):
            return producciones[0]
        # En las producciones generadas por no terminal
        for produccion in producciones:
            # Retornar la que contenga al terminal
            if produccion.find(terminal) != -1:
                return produccion

    def crearTabla(self):
        self.tablaSintactica = TablaSintactica()

        for nodoNt in self.noterminales:
            for nodoT in self.getPrimero(nodoNt):
                if nodoT != 'lambda':
                    self.tablaSintactica.insertar(nodoNt, nodoT,
                        self.buscar_produccion(nodoNt, nodoT))
                else:
                    for nodoT2 in self.siguientes[nodoNt]:
                       self.tablaSintactica.insertar(nodoNt, nodoT2,
                           'lambda')

    def tokenize_array(self, array):
        ret_str = ''
        for value in array:
            ret_str += (value + ' ')
        
        return ret_str

    # Validar String
    def validate_str(self, cadena):
        queue = cadena.split()
        stack = list()

        stack.append(self.dolar)
        stack.append(self.nodoInicial)
        queue.append(self.dolar)

        tabla_arbol = [['pila', 'entrada', 'operacion', 'adicionar']]

        raiz = Nodo(self.nodoInicial)
        pivote = raiz

        while (len(stack) > 0 and len(queue) > 0):
            fila_tabla = list()
            fila_tabla.append(self.tokenize_array(stack))
            fila_tabla.append(self.tokenize_array(queue))
            # Si queue.top es igual a stack.top()
            if queue[0] == stack[-1]:
                # pop a cada estructura
                queue.pop(0)
                stack.pop()
                pivote = opera2(pivote)
                fila_tabla.append('2') # operacion 2
                fila_tabla.append(' ')
            else:
                # pop a stack
                temp = stack.pop()
                try:
                    # Buscar en la tabla
                    valor_tabla = self.tablaSintactica.tabla[temp][queue[0]]
                    tokens_vtabla = valor_tabla.split()
                    tokens_vtabla.reverse()

                    adicionar_str = '' # adiciones al stack

                    # Visitar tabla en reversa
                    for x in tokens_vtabla:
                        # si existe cadena vacía, la metemos al stack 
                        if x.strip() != 'lambda':
                            stack.append(x)
                            adicionar_str += (x + ' ')
                    
                    if adicionar_str == '':
                        pivote = opera3(pivote)
                        fila_tabla.append('3') # operacion 3
                        fila_tabla.append('lambda')
                    else:
                        pivote = opera1(pivote, adicionar_str.split())
                        fila_tabla.append('1') # operacion 1
                        
                        # Poniendo el orden de los terminales/noterminales
                        # al revés
                        reverse_adicionar = adicionar_str.split()
                        adicionar_str = ''
                        
                        for valor in reverse_adicionar[::-1]:
                            adicionar_str += (valor + ' ')

                        fila_tabla.append(adicionar_str)

                except KeyError:
                    # Si no se encontró valor en la tabla
                    # Se halló un error de sintaxis
                    print("Error de sintaxis")
                    return False
            tabla_arbol.append(fila_tabla)
        
        for fila in tabla_arbol:
            for columna in fila:
                print(columna.ljust(20), end = ' ')
            print()

        return len(stack) == 0 and len(queue) == 0

    def cargar(self, texto):
        check_newlines = texto.split('\n')
        # Si es multilinea: separando cada linea
        for word in check_newlines:
            if len(word) <= 1:
                continue
            # Armando produccion
            produccion = Produccion(word)
            # Almacenando produccion
            self.producciones.append(produccion)
            if (len(self.producciones) == 1):
                self.nodoInicial = produccion.left.strip()

        self.buildTerminals()

    # print(Gramatica)
    def __str__(self):
        # String a ser retornado
        return_string = ""
        # Recorriendo producciones
        for produccion in self.producciones:
            return_string += (produccion.left + " := ")
            for i in range(len(produccion.right)):
                # Dando formato al resultado
                # Ultimo elemento: no imprimir |
                if i == len(produccion.right) - 1:
                    return_string += (produccion.right[i])
                # No es ultimo elemento: imprimir |
                else:
                    return_string += (produccion.right[i]) + " | "
            return_string += '\n'

        return return_string

    # Deprecated
    # Usar print(tabla)
    def imprimirTabla(self):

        tabla = self.tablaSintactica.tabla
        # Todos los strings tienen len=padding
        # Para que se vea ordenado
        print(" ".ljust(self.PADDING), end = ' ')
        # Imprimir terminales arriba
        terminal_list = list(self.terminales)
        for term in terminal_list:
            print(term.ljust(self.PADDING), end = ' ')

        print()
        # Recorriendo tabla
        for non_term in list(self.noterminales):
            # Imprimir no terminal a la izquierda
            print(non_term.ljust(self.PADDING), end = ' ')
            for term in terminal_list:
                # Si no hay valor en la casilla
                # Imprimir vacío
                if term not in tabla[non_term]:
                    print(" ".ljust(self.PADDING), end = ' ')
                else:
                    # Imprimir produccion si hay valor
                    produccion = ""
                    for value in tabla[non_term][term]:
                        produccion += value
                    print(produccion.ljust(self.PADDING), end = ' ')
            print()
    

def main():

    gramatica = Gramatica()
    #gramatica.cargar("Ep := prueba")
    gramatica.cargar("""
E  := T Ep
Ep := + T Ep 
Ep := - T Ep
Ep := lambda
T  := F Tp
Tp := * F Tp  |  /  F Tp  | lambda
F  := ( E ) | num | id
""")
    print(gramatica)

    print("Ep := ", gramatica.getProduccion('Ep'))
    print()

    print("no terminales", gramatica.noterminales)
    print("terminales", gramatica.terminales, '\n')

    #primeros = gramatica.getPrimero('F')
    primeros = gramatica.getPrimeros()
    print("primeros")
    print(primeros)
    print()

    siguientes = gramatica.getSiguientes()
    print("siguientes")
    print(siguientes)
    print()

    gramatica.crearTabla()
    #gramatica.imprimirTabla()
    print(gramatica.tablaSintactica)
    
    '''
    cadenas = ['num + num + num + num', '( num + num ) + ( num + num )',
            'num * ( num * num )', '( num * ) num', 'id - num + ( id )']
    
    for cadena in cadenas:
        print("Cadena a validar:", cadena)
        if gramatica.validate_str(cadena) == True:
            print("Válida")
        else:
            print("No válida")
    '''
    cadena = 'id + id * id'
    if gramatica.validate_str(cadena) == True:
        print("Válida")
    else:
        print("No válida")

if __name__ == '__main__':
    main()
