import re

name = '((\s)?[A-Z]([a-z]|\s)*)+'
last_name = name
dni = '(\s)?([0-9]){8}(\s)?'
age = '(\s)?[0-9]{0,3}(\s)?'
school = '([A-Za-z]|[0-9]|\s)*'
    
var_regex = name + '\|' + last_name + '\|' + dni + '\|' + age + '\|' + school

tests = ['Julio Manuel|Guzman Gutierrez|12345678||Colegio 2424 SSAA',
'Liz|Linh|00000001|19|',
'Armando | Manzanero | 99999999 | 101 |',
'||||',
'||12345678||',
'Carmen|De la Vega|23|23|Micole.com',
'Un|Mal dni|1234567|errorletras|cole',
'Numeros 444 | en nombre o apellido11 |letras|99|Lucha libre']

p = re.compile(var_regex)

for test in tests:
    print(test)
    if p.match(test):
        print("Entrada válida")
    else:
        print("Entrada inválida")

