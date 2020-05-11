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
        self.left = split_result[0]

        total_rules = split_result[1].split('|')
        self.right = total_rules

class Gramatica:
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

    def __init__(self):
        #terminales = ['+', '-', '*', '/', '(', ')', 'num', 'id', '$']
        #noterminales = ['E', 'Ep', 'T', 'Tp', 'F']
        pass

    def getProduccion(self, izq):
        # Buscando en el conjunto de producciones
        ret_value = list()
        for produccion in self.producciones:
            # Eliminando espacios en blanco
            # En caso sea necesario
            # Si coincide, retornar produccion
            if produccion.left.replace(' ', '') == izq:
                #print(produccion.left, ":=", end = ' ')
                #print(produccion.right)

                ret_value.append(produccion.right)
                
                # No se rompe el bucle porque puede que
                # Un valor a la izquierda tenga múltiples
                # valores a la derecha
        return ret_value

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
        if term not in self.TablaSintactica:
            # si no existe, crearlo
            self.TablaSintactica[term] = dict()
        # Insertar arreglo en la entrada
        self.TablaSintactica[term][non_term] = prod

        # Actualizar lista de terminales y no terminales
        if non_term not in self.noterminales:
            self.noterminales.add(non_term)

        if term not in self.terminales:
            self.terminales.add(term)

    def imprimirTabla(self):
        # Todos los strings tienen len=7
        # Para que se vea ordenado
        print(" ".ljust(7), end = ' ')
        # Imprimir terminales arriba
        for term in self.terminales:
            print(term.ljust(7), end = ' ')

        print()
        # Recorriendo tabla
        for non_term in self.noterminales:
            # Imprimir no terminal a la izquierda
            print(non_term.ljust(7), end = ' ')
            for term in self.terminales:
                # Si no hay valor en la casilla
                # Imprimir vacío
                if non_term not in self.TablaSintactica[term]:
                    print(" ".ljust(7), end = ' ')
                else:
                    # Imprimir produccion si hay valor
                    produccion = ""
                    for value in self.TablaSintactica[term][non_term]:
                        produccion += value + " "
                    print(produccion.ljust(7), end = ' ')
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

    print("no terminales", gramatica.noterminales)
    print("terminales", gramatica.terminales)

if __name__ == '__main__':
    main()
