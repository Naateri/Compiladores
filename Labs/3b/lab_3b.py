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

class Produccion:

    def __init__(self, texto):
        # Separar izquierda de derecha
        split_result = texto.split(':=')
        self.left = split_result[0].strip()

        total_rules = split_result[1].split('|')
        self.right = [rule.strip() for rule in total_rules]

    def __str__(self):
        return self.left + ' := ' + str(self.right)

class Gramatica:
    # Impresion de la tabla
    PADDING = 7
    producciones = []
    # Ventaja de usar lista:
    # poder meter más de una vez de manera sencilla
    # producción que empieza
    # con el mismo no terminal, ej (uno después del otro):
    # Gramatica.cargar("Ep := A|B")
    # Gramatica.cargar("Ep := C|D")
    terminales = set()
    noterminales = set()

    TablaSintactica = dict()

    dolar = '$'

    def __init__(self):
        #terminales = ['+', '-', '*', '/', '(', ')', 'num', 'id', '$']
        #noterminales = ['E', 'Ep', 'T', 'Tp', 'F']
        self.nodoInicial = None

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

    def getProducciones(self):
        # retornar elementos de la derecha en forma de una lista
        producciones = list()
        for nodo in self.noterminales:
            producciones.append(self.getProduccion(nodo))
        return producciones

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
            siguientes[noterminal] = list()
        
        siguientes[self.nodoInicial].append(self.dolar)
        to_fill = list() # valores que no tienen nodo a la derecha
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
                    
                    if tokens[i+1] not in siguientes[tokens[i]]:
                        siguientes[tokens[i]].append(tokens[i+1])

                    # Si el almacenado es un no terminal, se actualizará
                    # Con el siguiente correspondiente (el de ese no terminal)
                    # después
                        
                # Si el ultimo es no terminal, no tiene
                # nadie a su derecha, lo guardamos en la lista
                # to_fill para actualizarlo posteriormente
                if tokens[-1] in self.noterminales:
                    # Solo si no tiene elementos en sus siguientes
                    if len(siguientes[tokens[-1]]) < 1:
                       to_fill.append(tokens[-1])

        # Llenando no terminales
        # Que no tenían nodo a su derecha
        for filler in to_fill:
            # Encontrando quien lo genera
            generated_by = self.find_generator(filler)
            # Reemplazando con los siguientes del generador
            if len(generated_by) == 1 and len(siguientes[filler]) < 1:
                gen_by = list(generated_by)[0]
                siguientes[filler] = siguientes[gen_by]

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
                            siguientes[key].append(element)
                    # eliminamos no terminal de los siguientes
                    siguientes[key].remove(siguiente)
                    
        return siguientes

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

    def insertarTabla(self, non_term, term, prod):
        # Revisar si existe terminal en el diccionario
        if non_term not in self.TablaSintactica:
            # si no existe, crearlo
            self.TablaSintactica[non_term] = dict()
        # Insertar arreglo en la entrada
        self.TablaSintactica[non_term][term] = prod

        # Actualizar lista de terminales y no terminales
        if non_term not in self.noterminales:
            self.noterminales.add(non_term)

        if term not in self.terminales:
            self.terminales.add(term)

    def imprimirTabla(self):
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
                if term not in self.TablaSintactica[non_term]:
                    print(" ".ljust(self.PADDING), end = ' ')
                else:
                    # Imprimir produccion si hay valor
                    produccion = ""
                    for value in self.TablaSintactica[non_term][term]:
                        produccion += value + " "
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

    gramatica.insertarTabla('E', '(', ['T', 'Ep'])
    gramatica.insertarTabla('E', 'num', ['T', 'Ep'])
    gramatica.insertarTabla('E', 'id', ['T', 'Ep'])

    gramatica.insertarTabla('Ep', '+', ['+', 'T', 'Ep'])
    gramatica.insertarTabla('Ep', '-', ['-', 'T', 'Ep'])
    gramatica.insertarTabla('Ep', ')', ['lambda'])
    gramatica.insertarTabla('Ep', '$', ['lambda'])

    gramatica.insertarTabla('T', '(', ['F', 'Tp'])
    gramatica.insertarTabla('T', 'num', ['F', 'Tp'])
    gramatica.insertarTabla('T', 'id', ['F', 'Tp'])

    gramatica.insertarTabla('Tp', '+', ['lambda'])
    gramatica.insertarTabla('Tp', '-', ['lambda'])
    gramatica.insertarTabla('Tp', '*', ['*', 'F', 'Tp'])
    gramatica.insertarTabla('Tp', '/', ['/', 'F', 'Tp'])
    gramatica.insertarTabla('Tp', ')', ['lambda'])
    gramatica.insertarTabla('Tp', '$', ['lambda'])

    gramatica.insertarTabla('F', '(', ['(', 'E', ')'])
    gramatica.insertarTabla('F', 'num', ['num'])
    gramatica.insertarTabla('F', 'id', ['id'])

    #print(gramatica.TablaSintactica)
    gramatica.imprimirTabla()
    print()

if __name__ == '__main__':
    main()
