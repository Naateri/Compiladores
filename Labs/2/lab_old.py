#####Alumno: Renato Luis Postigo Avalos

operators = ['+','-','*','/','=']

def analizadorLexico(linea):
    tokens = list()
    cur_token = "" #Variables
    for letra in linea: #recorrer linea
        if letra in operators: #token de operacion

            if cur_token != "": #Variable encontrada
                tokens.append(cur_token)

            tokens.append(letra) #metiendo token de operacion
            cur_token = ""
        else: #variable
            if letra == " ":
                if cur_token != "":
                    tokens.append(cur_token)
                    cur_token = ""
            else:
                cur_token += letra

    if cur_token != "": #variable al final de la linea
        tokens.append(cur_token)

    return tokens

linea = "variable = tmp0 + 20"
tokens = analizadorLexico(linea)

print(tokens)
