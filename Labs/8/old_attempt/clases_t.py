## Alumno: Renato Postigo
## Clases terminales gramatica

'''
E  := T Ep
Ep := + T Ep 
Ep := - T Ep
Ep := lambda
T  := F Tp
Tp := * F Tp  |  /  F Tp  | lambda
F  := ( E ) | num | id
'''

class Terminal:
    def __init__(self, name):
        self.label = name

    def interpret(self):
        return self.label

class Num(Terminal):
    def __init__(self, value):
        super().__init__(value)
