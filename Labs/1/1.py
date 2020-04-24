###Ejercicio 1

opening_brackets = ['[', '(']
closing_brackets = [']', ')']

def balanced_text(text):
    stack = list()
    text = text.replace(' ', '')

    for character in text:
        if character in opening_brackets:
            stack.append(character)
        else: #character in closing_brackets
            opening_bracket = stack.pop()
            position = opening_brackets.index(opening_bracket)
            if character != closing_brackets[position]:
                print("NO")
                return

    if len(stack) > 0:
        print("NO")
    else:
        print("SI")

text = input('Ingrese el texto ')

balanced_text(text)
