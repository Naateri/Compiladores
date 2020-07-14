## Alumno:
## Renato Luis Postigo Avalos

'''
E  := T Ep
Ep := + T Ep 
Ep := - T Ep
Ep := lambda
T  := F Tp
Tp := * F Tp  | lambda
F  := ( E ) | num
'''

def find_pos(array, element):
    for i in range(len(array)):
        if array[i] == element:
            return i

    return -1

class NNTerminal:
    def __init__(self, name):
        self.label = name
        self.prod = dict()

class E(NNTerminal):
    def __init__(self):
        super().__init__('E')
        self.prod['T'] = None
        self.prod['Ep'] = None

    def split_multi_suma(self, tokens):
        multi = list() # T
        suma = list() # Ep

        append_multi = True

        for token in tokens:
            if token == '+' or token == '-':
                append_multi = False
            
            if append_multi:
                multi.append(token)
            else:
                suma.append(token)

        return multi, suma

    def interpret(self, text):

        cur_t = T()

        print('T Ep')

        cur_text = text.split()

        # cur_text[0]: T
        # el resto: Ep

        self.prod['T'] = cur_t

        #self.prod['T'].interpret(text[0])

        self.prod['Ep'] = Ep()

        multi, suma = self.split_multi_suma(cur_text)
        #print('multi', multi)
        #print('suma', suma)

        # Ep: suma o resta
        # text[0] (multi): anterior, interpretado por T
        # text[1] (suma): resto de la operacion incluyendo el operador
        # Ep es el encargado de interpretar a T (anterior)

        #if len(cur_text) > 1:
        if len(suma) > 1: # Suma o resta
            #return self.prod['Ep'].interpret(cur_text[0], cur_text[1:])
            return self.prod['Ep'].interpret(multi, suma)
        else: # Pasar cadena vacía (lambda)
            #return self.prod['Ep'].interpret(cur_text[0], '')
            return self.prod['Ep'].interpret(multi, '')


class Ep(NNTerminal):
    def __init__(self):
        super().__init__('Ep')
        self.prod['+'] = None
        self.prod['-'] = None
        self.prod['T'] = None
        self.prod['Ep'] = None
        self.prod['lambda'] = None

    # anterior: suma acumulada
    # text: lo que sigue
    def interpret(self, anterior, text):
        self.prod['T'] = T()
        valorT = self.prod['T'].interpret(anterior)

        self.prod['Ep'] = Ep()
        
        # creacion de instancia según sea necesario
        if text == '':
            self.prod['lambda'] = Lambda()
        elif text[0] == '+':
            self.prod['+'] = Plus()
        elif text[0] == '-':
            self.prod['-'] = Minus()
        
        if self.prod['+'] != None:
            print('+ T Ep')
            self.prod['+'].interpret()
            #print('Ep text', text)
            # si sigue más texto: pasarlo
            if len(text) > 2:
                # Si hay más sumas o restas, Ep no es lambda
                if '+' in text[1:] or '-' in text[1:]:
                    # buscar + o - para saber que enviar
                    # consideracion: parte a la izquierda de la suma = T
                    op_pos = find_pos(text[1:], '+')
                    # no encontro +, probar con -
                    if op_pos == -1:
                        op_pos = find_pos(text[1:], '-')
                    return valorT + self.prod['Ep'].interpret(text[1], text[2:])
                else:
                # Si no quedan sumas o restas, Ep es lambda
                    return valorT + self.prod['Ep'].interpret(text[1:], '')
            # si no, pasar cadena vacía
            else:
                return valorT + self.prod['Ep'].interpret(text[1], '')

        elif self.prod['-'] != None:
            print('- T Ep')
            self.prod['-'].interpret()
            # si sigue más texto: pasarlo
            if len(text) > 2:
                # Si hay más sumas o restas, Ep no es lambda
                if '+' in text[1:] or '-' in text[1:]:
                    # buscar + o - para saber que enviar
                    # consideracion: parte a la izquierda de la suma = T
                    op_pos = find_pos(text[1:], '+')
                    # no encontro +, probar con -
                    if op_pos == -1:
                        op_pos = find_pos(text[1:], '-')
                    return valorT - self.prod['Ep'].interpret(text[1], text[2:])
                else:
                # Si no quedan sumas o restas, Ep es lambda
                    return valorT - self.prod['Ep'].interpret(text[1:], '')
            # si no, pasar cadena vacía
            else:
                return valorT - self.prod['Ep'].interpret(text[1], '')
        # si no hay mas texto, retornar lo acumulado
        elif self.prod['lambda'] != None:
            #print('lambda')
            self.prod['lambda'].interpret()
            return valorT

class T(NNTerminal):
    def __init__(self):
        super().__init__('T')
        self.prod['F'] = None
        self.prod['Tp'] = None

    def split_multi_num(self, tokens):
        num = list() # F
        multi = list() # Tp

        append_num = True

        for token in tokens:
            if token == '*':
                append_num = False
            
            if append_num:
                num.append(token)
            else:
                multi.append(token)

        return num, multi

    def interpret(self, text):
        cur_f = F()

        print('F Tp')

        self.prod['F'] = cur_f

        self.prod['Tp'] = Tp()

        if type(text) != list:
            cur_text = text.split()
        else:
            cur_text = text

        num, multi = self.split_multi_num(cur_text)

        #print('num', num)
        #print('multi', multi)

        # Tp: multiplicacion o division
        # text[0] (num): anterior, interpretado por F
        # text[1] (multi): resto de la operacion incluyendo el operador
        # Tp es el encargado de interpretar a F (anterior)

        #if len(cur_text) > 1: # Multiplicacion
        if len(multi) > 1: # Multiplicacion
            #return self.prod['Tp'].interpret(cur_text[0], cur_text[1:])
            return self.prod['Tp'].interpret(num[0], multi)
        else: # Pasar cadena vacía (lambda), posible numero
            #return self.prod['Tp'].interpret(cur_text[0], '')
            return self.prod['Tp'].interpret(num[0], '')
        

class Tp(NNTerminal):
    def __init__(self):
        super().__init__('Tp')
        self.prod['*'] = None
        self.prod['F'] = None
        self.prod['Tp'] = None
        self.prod['lambda'] = None

    def interpret(self, anterior, text):
        self.prod['F'] = F()
        valorF = self.prod['F'].interpret(anterior)

        self.prod['Tp'] = Tp()

        if text == '':
            self.prod['lambda'] = Lambda()
        elif text[0] == '*':
            self.prod['*'] = Product()

        if self.prod['*'] != None:
            print('* F Tp')
            #suma = int(anterior) + valorT
            self.prod['*'].interpret()
            # si sigue más texto: pasarlo
            if len(text) > 2:
                return valorF * self.prod['Tp'].interpret(text[1], text[2:])
            # si no, pasar cadena vacía
            else:
                return valorF * self.prod['Tp'].interpret(text[1], '')

        # si no hay mas texto, retornar lo acumulado
        elif self.prod['lambda'] != None:
            #print('lambda')
            self.prod['lambda'].interpret()
            return valorF

class F(NNTerminal):
    def __init__(self):
        super().__init__('F')
        self.prod['('] = None
        self.prod['E'] = None
        self.prod[')'] = None
        self.prod['num'] = None
        self.prod['id'] = None

    def interpret(self, valor):

        if valor[0] == '(': # Composición
            self.prod['E'] = E()
        elif valor[0].isdigit(): # Número
            self.prod['num'] = Num(int(valor))
        
        if self.prod['E'] != None:
            return self.prod['E'].interpret()
        elif self.prod['num'] != None:
            return self.prod['num'].interpret()

class Terminal:
    def __init__(self, name):
        self.label = name
        #print('(Tree)', self.label)

    def interpret(self):
        print('(Tree)', self.label)
        return self.label

class Num(Terminal):
    def __init__(self, value):
        print('num')
        super().__init__(value)

class Plus(Terminal):
    def __init__(self):
        super().__init__('+')

class Minus(Terminal):
    def __init__(self):
        super().__init__('-')

class Product(Terminal):
    def __init__(self):
        super().__init__('*')

class Lambda(Terminal):
    def __init__(self):
        super().__init__('lambda')

def main():
    
    #cadena = '10 * 2 + 2'
    #cadena = '10 + 2 * 2'
    cadena = '1 + 1'
    #cadena = '2 * 3'
    temp = E()
    print(cadena, '=', temp.interpret(cadena))

if __name__ == '__main__':
    main()
