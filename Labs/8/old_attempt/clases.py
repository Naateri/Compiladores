## Alumno: Renato Postigo
## Clases noterminales gramatica

'''
E  := T Ep
Ep := + T Ep 
Ep := - T Ep
Ep := lambda
T  := F Tp
Tp := * F Tp  |  /  F Tp  | lambda
F  := ( E ) | num | id
'''

class NNTerminal:
    def __init__(self, name):
        self.label = name
        self.prod = dict()

class E(NNTerminal):
    def __init__(self):
        super().__init__('E')
        self.prod['T'] = None
        self.prod['Ep'] = None

    def interpret(self):
        if self.prod['T'] != None:
            return self.prod['T'].interpret()
        elif self.prod['Ep'] != None:
            return self.prod['Ep'].interpret()


class Ep(NNTerminal):
    def __init__(self):
        super().__init__('Ep')
        self.prod['+'] = None
        self.prod['-'] = None
        self.prod['T'] = None
        self.prod['Ep'] = None
        self.prod['lambda'] = None

    def interpret(self, anterior):
        valorT = self.prod['T'].interpret()

        if self.prod['+'] != None:
            suma = anterior + valorT
            return self.prod['Ep'].interpret(suma)

        elif self.prod['-'] != None:
            resta = anterior - valorT
            return self.prod['Ep'].interpret(resta)

class T(NNTerminal):
    def __init__(self):
        super().__init__('T')
        self.prod['F'] = None
        self.prod['Tp'] = None

    def interpret(self, anterior):
        if self.prod['F'] != None:
            return self.prod['F']
        elif self.prod['Tp'] != None:
            return self.prod['Tp']
        

class Tp(NNTerminal):
    def __init__(self):
        super().__init__('Tp')
        self.prod['*'] = None
        self.prod['/'] = None
        self.prod['F'] = None
        self.prod['Tp'] = None
        self.prod['lambda'] = None

    def interpret(self, anterior):
        valorF = self.prod['F'].interpret()

        if self.prod['*'] != None:
            multi = anterior * valorF
            return self.prod['Tp'].interpret(multi)

        elif self.prod['/'] != None:
            divi = anterior / valorF
            return self.prod['Tp'].interpret(divi)

class F(NNTerminal):
    def __init__(self):
        super().__init__('F')
        self.prod['('] = None
        self.prod['E'] = None
        self.prod[')'] = None
        self.prod['num'] = None
        self.prod['id'] = None

    def interpret(self):
        if self.prod['E'] != None:
            return self.prod['E'].interpret()
        elif self.prod['num'] != None:
            return self.prod['num'].interpret()
        
