## Alumno:
## Renato Luis Postigo Avalos

'''
E  := T Ep
Ep := + T Ep 
Ep := - T Ep
Ep := lambda
T  := F Tp
Tp := * F Tp  |  /  F Tp  | lambda
F  := ( E ) | num
'''

#from clases import E, Ep, T, Tp, F
#from clases_t import Num

class NNTerminal:
    def __init__(self, name):
        self.label = name
        self.prod = dict()

class E(NNTerminal):
    def __init__(self):
        super().__init__('E')
        self.prod['T'] = None
        self.prod['Ep'] = None

    def interpret(self, text):

        cur_t = T()

        print('T Ep')

        cur_text = text.split()

        # cur_text[0]: T
        # el resto: Ep

        self.prod['T'] = cur_t

        #self.prod['T'].interpret(text[0])

        self.prod['Ep'] = Ep()

        # Ep: suma o resta
        # text[0]: anterior
        # text[1]: resto de la operacion incluyendo el operador

        if len(cur_text) > 1: # Suma o resta
            return self.prod['Ep'].interpret(cur_text[0], cur_text[1:])
        else: # Pasar cadena vacía (lambda)
            return self.prod['Ep'].interpret(cur_text[0], '')


class Ep(NNTerminal):
    def __init__(self):
        super().__init__('Ep')
        self.prod['+'] = None
        self.prod['-'] = None
        self.prod['T'] = None
        self.prod['Ep'] = None
        self.prod['lambda'] = None

    def interpret(self, anterior, text):
        self.prod['T'] = T()
        valorT = self.prod['T'].interpret(anterior)

        self.prod['Ep'] = Ep()

        if text == '':
            self.prod['lambda'] = Lambda()
        elif text[0] == '+':
            self.prod['+'] = Plus()
        elif text[0] == '-':
            self.prod['-'] = Minus()
        
        if self.prod['+'] != None:
            print('+ T Ep')
            #suma = int(anterior) + valorT
            self.prod['+'].interpret()
            if len(text) > 2:
                return valorT + self.prod['Ep'].interpret(text[1], text[2:])
            else:
                return valorT + self.prod['Ep'].interpret(text[1], '')

        elif self.prod['-'] != None:
            print('- T Ep')
            resta = int(anterior) - valorT
            return self.prod['Ep'].interpret(resta)

        elif self.prod['lambda'] != None:
            #print('lambda')
            self.prod['lambda'].interpret()
            return valorT

class T(NNTerminal):
    def __init__(self):
        super().__init__('T')
        self.prod['F'] = None
        self.prod['Tp'] = None

    def interpret(self, text):
        cur_f = F()

        print('F Tp')

        self.prod['F'] = cur_f

        self.prod['Tp'] = Tp()

        cur_text = text.split()

        if len(cur_text) > 1: # Multiplicacion
            return self.prod['Tp'].interpret(cur_text[0], cur_text[1:])
        else: # Pasar cadena vacía (lambda), posible numero
            return self.prod['Tp'].interpret(cur_text[0], '')
        

class Tp(NNTerminal):
    def __init__(self):
        super().__init__('Tp')
        self.prod['*'] = None
        self.prod['/'] = None
        self.prod['F'] = None
        self.prod['Tp'] = None
        self.prod['lambda'] = None

    def interpret(self, anterior, text):
        self.prod['F'] = F()
        valorF = self.prod['F'].interpret(anterior)

        if text == '':
            self.prod['lambda'] = Lambda()
        elif text[0] == '*':
            self.prod['*'] = Product()
        elif text[0] == '':
            self.prod['lambda'] = Lambda()

        if self.prod['*'] != None:
            multi = anterior * valorF
            return self.prod['Tp'].interpret(multi)

        elif self.prod['/'] != None:
            divi = anterior / valorF
            return self.prod['Tp'].interpret(divi)

        elif self.prod['lambda'] != None:
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
    
    cadena = '10 + 15'
    #cadena = 'num + num'
    temp = E()
    print(cadena, '=', temp.interpret(cadena))

if __name__ == '__main__':
    main()
