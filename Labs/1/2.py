###Ejercicio 2

vowels = ['a','e','i','o','u']
special_cases = ['reir', 'pedir', 'sentir', 'servir', 'venir', 'mentir']
special_cases_ans = ['riendo', 'pidiendo', 'sintiendo', 'sirviendo',
                     'viniendo', 'mintiendo']

def check_gerundio(text):
    words = text.split(' ')
    verb = words[0]

    if verb in special_cases:
        gerund = special_cases_ans[special_cases.index(verb)]
    elif verb.endswith('ar'):
        gerund = verb[:len(verb)-2] + "ando"
    elif verb.endswith('er') or verb.endswith('ir'):
        if verb[-3] in vowels:
            gerund = verb[:len(verb)-2] + "yendo"
        else:
            gerund = verb[:len(verb)-2] + "iendo"

    if gerund == words[1]:
        print("SI")
    else:
        print("NO")

text = input('Ingrese el texto ')
check_gerundio(text)
