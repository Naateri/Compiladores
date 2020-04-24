#Ejercicio 3

#Formula: P = U * I
concept = ['P', 'U', 'I']
prefix = ['m', 'k', 'M']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']
prefix_multiplier = ['0.001', '1000', '1000000']
units = ['W', 'V', 'A']

def solve_problem(problem, index):
    words = problem.split()
    datafields = list()
    for word in words:
        if '=' in word:
            datafields.append(word)

    results = {'P': 0, 'U': 0, 'I': 0}

    for datafield in datafields:
        parts = datafield.split('=') #[0]: concept [1]: prefix unit
        concept = parts[0] #P, U or I
        unit = parts[1]

        counter = 0
        value = ''
        for letter in unit:
            if letter in numbers:
                value += letter
                counter += 1
            else:
                break

        value = float(value) #Number
        
        prefix_unit = unit[counter:] #V, mV, MA, etc
        if prefix_unit[0] in prefix: #it has a prefix
            multiplier = prefix_multiplier[ prefix.index(prefix_unit[0]) ]
            value *= float(multiplier)

        results[concept] = value #add to dictionary

    if results['P'] == 0:
        #P = U * I
        result_concept = 'P'
        result = results['U'] * results['I']
        results_unit = units[0]
    elif results['U'] == 0:
        #U = P / I
        result_concept = 'U'
        result = results['P'] / results['I']
        results_unit = units[1]
    else: #results['I'] == 0
        #I = P / U
        result_concept = 'I'
        result = results['P'] / results['U']
        results_unit = units[2]

    print("Problem #{0}".format(index))
    print("{0}={1:.2f}{2}".format(result_concept, result, results_unit))

problems = list()
cases = input()

for i in range(int(cases)):
    problem = input()
    problems.append(problem)

cur_problem = 1
for problem in problems:
    solve_problem(problem, cur_problem)
    cur_problem += 1
    print()
