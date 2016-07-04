'''

Kristel Tan (ktan@bu.edu)
CAS CS320 Fall 2015 - Professor Lapets
Assignment 3 - interpret.py
Skeleton code from Professor Lapets

'''

exec(open('parse.py').read())

Node = dict
Leaf = str

# Question 1a
# evalTerm() returns the value that corresponds to the
# evaluation of parse tree t given environment env

def evalTerm(env, e):

    if type(e) == Node:

        for label in e:

            children = e[label]

            if label == 'Variable':
                e1 = children[0]
                if e1 in env:
                    return env[e1]
                else:
                    print(e1 + " is unbound.")
                    exit()

            elif label == 'Number':
                e1 = children[0]
                return {'Number':[e1]}

            elif label == 'Plus':
                e1 = children[0]
                e2 = children[1]
                v1 = evalTerm(env, e1)
                v2 = evalTerm(env, e2)
                return {'Number':[v1['Number'][0] + v2['Number'][0]]}

# Question 1b
# evalFormula() returns the value that corresponds to the
# evaluation of parse tree f given environment env

def evalFormula(env, e):

    if type(e) == Node:

        for label in e:

            children = e[label]

            if label == 'Variable':
                e1 = children[0]
                return evalFormula(env, env[e1])

            elif label == 'Not':
                e1 = children[0]
                if evalFormula(env, e1) == 'True':
                    return 'False'
                else:
                    return 'True'

            elif label == 'Xor':
                e1 = children[0]
                e2 = children[1]
                v1 = evalFormula(env, e1)
                v2 = evalFormula(env, e2)
                return xor(v1, v2)

            elif label == 'AndShort':
                e1 = children[0]
                e2 = children[1]
                v1 = evalFormula(env, e1)
                v2 = evalFormula(env, e2)
                if vand(v1, v2) == 'False':
                    return 'False'

            elif label == 'And':
                e1 = children[0]
                e2 = children[1]
                v1 = evalFormula(env, e1)
                v2 = evalFormula(env, e2)
                return vand(v1, v2)

    if type(e) == Leaf and e in ['True', 'False']:
        return e

# Helper function for 'xor' operation
def xor(v1, v2):

    if v1 == 'True' and v2 == 'True': return 'False'
    if v1 == 'True' and v2 == 'False': return 'True'
    if v1 == 'False' and v2 == 'True': return 'True'
    if v1 == 'False' and v2 == 'False': return 'False'

# Helper function for 'and' operation
def vand(v1, v2):

    if v1 == 'True' and v2 == 'True': return 'True'
    if v1 == 'True' and v2 == 'False': return 'False'
    if v1 == 'False' and v2 == 'True': return 'False'
    if v1 == 'False' and v2 == 'False': return 'False'

# Question 1c
# execProgram() returns the a tuple containing the output and an updated
# environment that represents the result of the execution of the program
# as determined by the operational semantics

# Useful helper function
def execExpression(env, e):

    t = evalTerm(env, e)
    f = evalFormula(env, e)

    if f != None:
        return f

    if t != None:
        return t

def execProgram(env, s):

    if type(s) == Leaf:

        if s == 'End':
            return env, []

    elif type(s) == Node:

        for label in s:

            if label == 'Assign' or label == 'Procedure':
                children = s[label]
                var = children[0]['Variable'][0]
                env[var] = children[1]
                return execProgram(env, children[2])

            elif label == 'Call':
                children = s[label]
                x = children[0]['Variable'][0]
                f = env[x]
                (env, p) = execProgram(env, f)
                (env, o) = execProgram(env, children[1])
                return env, p + o

            elif label == 'Print':
                children = s[label]
                x = children[0]
                f = children[1]
                v = execExpression(env, x)
                env2, o = execProgram(env, f)
                return env2, [v] + o

            elif label == 'If':
                children = s[label]
                c1 = children[0]
                c2 = children[1]
                c3 = children[2]
                e = execExpression(env, c1)
                if e == 'True':
                    env2, o1 = execProgram(env, c2)
                    env3, o2 = execProgram(env2, c3)
                    return env3, o1 + o2
                else:
                    env2, o1 = execProgram(env, c3)
                    return env2, c3

            elif label == 'Until':
                [cond, body, rest] = s[label]
                e = execExpression(env, cond)
                if e == 'True':
                    (env2, o1) = execProgram(env, body)
                    (env3, o2) = execProgram(env2, rest)
                    return env3, o2
                if e == 'False':
                    (env2, o1) = execProgram(env, body)
                    (env3, o2) = execProgram(env2, {'Until':[cond, body, rest]})
                    return env3, o1 + o2

    else:
        return None

def interpret(s):
    (env, o) = execProgram({}, tokenizeAndParse(s))
    return o

#eof


