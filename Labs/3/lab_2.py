import re

var_regex = '[a-zA-Z][a-zA-Z0-9_]*$'


p = re.compile(var_regex)
var = "sum_result"

if p.match(var):
    print("Nombre de variable valido")
else:
    print("No es un nombre de variable valido")
