#####Alumno: Renato Luis Postigo Avalos

operators = ['+','-','*','/','=']

#####PREGUNTA 5: IMPRIMIR INFORMACION DEL TOKEN

class Token:
    palabra = ""
    indice = -1
    tipo = ""

    def __init__(self, palabra, indice, tipo):
        self.palabra = palabra
        self.indice = indice
        self.tipo = tipo
    
    def __str__(self): #print(Token)
        return "Token[{0}]: pos = {1}, tipo = {2}".format(
            self.palabra, self.indice, self.tipo)

    def toString(self):
        return str(self)

#####PREGUNTA 2 y 3: RECONOCER NUMERO Y VARIABLE

def reconoceNumero(linea, idx):
    start_idx = idx #Para constructor de Token
    token = ""
    while idx < len(linea) and linea[idx].isdigit(): #mientras sea digito
        token += linea[idx] #Agregar al token
        idx += 1

    token_obj = Token(int(token), start_idx, "E") #Creacion del token
    return token_obj,idx

def reconoceVariable(linea, idx):
    start_idx = idx #Para constructor de token
    token = ""
    while idx < len(linea) and linea[idx] not in operators and linea[idx] != " ":
        #mientras no sea un operador ni un espacio
        token += linea[idx] #Agregar al token
        idx += 1

    token_obj = Token(token, start_idx, "V") #Creacion del token
    return token_obj,idx

####PREGUNTA 1: ANALIZADOR LEXICO

def analizadorLexico(linea):
    tokens = list()
    index = 0
    while index < len(linea): #Recorriendo string

        if linea[index].isdigit(): #Es un numero
            token,index = reconoceNumero(linea, index)
            tokens.append(token) #Guardar token

        elif linea[index].isalpha(): #Es una palabra
            token,index = reconoceVariable(linea, index)
            tokens.append(token) #Guardar token

        elif linea[index] in operators: #Operadores
            token = linea[index] 
            token_obj = Token(token, index, "O") #Creacion del token
            tokens.append(token_obj) #Guardar token
            index += 1

        elif linea[index] == " ": #Espacio
            index += 1 #Omitir

    return tokens

linea = "variable = tmp0 + 20"
tokens = analizadorLexico(linea)

for token in tokens:
    print (token.toString())
