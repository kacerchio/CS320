'''

Kristel Tan (ktan@bu.edu)
CAS CS320 Fall 2015 - Professor Lapets
interpret.py

'''

exec(open('parse.py').read())
import re

# Question 2a

# evalTerm() returns the value that corresponds to the
# evaluation of parse tree t given environment env

def evalTerm(env, t):


    if type(t) == dict:

        for label in t:

            children = t[label]

            if label == 'Number':
                e1 = children[0]
                return t

            elif label == 'Variable':
                e1 = children[0]
                return env[e1]

            elif label == "Parens":
                e1 = children[0]
                return evalTerm(env, e1)

            elif label == "If":
                e1 = children[0]
                e2 = children[1]
                v1 = evalTerm(env, e1) != evalTerm(env, e2)
                if v1 == True:
                    return e2
                else:
                    return e1

            elif label == "Plus":
                e1 = children[0]
                e2 = children[1]
                v1 = evalTerm(env, e1)
                v2 = evalTerm(env, e2)
                return {'Number':[v1['Number'][0] + v2['Number'][0]]}

            elif label == "Mult":
                e1 = children[0]
                e2 = children[1]
                v1 = evalTerm(env, e1)
                v2 = evalTerm(env, e2)
                return {'Number':[v1['Number'][0] * v2['Number'][0]]}

# Question 2b

# evalFormula() returns the value that corresponds to the
# evaluation of parse tree f given environment env

def evalFormula(env, f):

    if type(f) == dict:

        for label in f:

            children = f[label]

            if label == 'Variable':
                e1 = children[0]
                if e1 in env:
                    return env[e1]
                else:
                    print(e1 + 'is unbound.')
                    exit()

            elif label == 'Nonzero':
                e1 = children[0]
                if e1 != 0:
                    return 'True'
                else:
                    return 'False'

            elif label == 'Not':
                e1 = children[0]
                return not evalFormula(env, e1)

            elif label == "And":
                e1 = children[0]
                e2 = children[1]
                v1 = evalFormula(env, e1)
                v2 = evalFormula(env, e2)
                return vand(v1, v2)
    else:

        if f == 'True':
            return 'True'

        if f == 'False':
            return 'False'

# Helper function for 'and' operation
def vand(v1, v2):

    if v1 == 'True' and v2 == 'True': return 'True'
    if v1 == 'True' and v2 == 'False': return 'False'
    if v1 == 'False' and v2 == 'True': return 'False'
    if v1 == 'False' and v2 == 'False': return 'False'

# Question 2c

# execProgram() returns the a tuple containing the output and an updated
# environment that represents the result of the execution of the program
# as determined by the operational semantics

def execProgram(env, s):

    if type(s) == str:
        if s == 'End':
            return env, []

    elif type(s) == dict:

        for label in s:

            if label == 'Print':
                children = s[label]
                c1 = children[0]
                c2 = children[1]
                e = execExpression(env, c1)
                env2, s2 = execProgram(env, c2)
                return env2, [e] + s2

            elif label == 'Assign':
                children = s[label]
                c1 = children[0]['Variable'][0]
                c2 = children[1]
                c3 = children[2]
                e = execExpression(env, c2)
                env[c1] = e
                env2, s2 = execProgram(env, c3)
                return env2, s2

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

            elif label == 'DoUntil':
                [cond, body, rest] = s[label]
                e = execExpression(env, body)
                if e == 'True':
                    (env2, o1) = execProgram(env, cond)
                    (env3, o2) = execProgram(env2, rest)
                    return env3, o1 + o2
                if e == 'False':
                    (env2, o1) = execProgram(env, cond)
                    (env3, o2) = execProgram(env2, {'DoUntil':[cond, body, rest]})
                    return env3, o1 + o2

    else:
        return None

# Helper function to execute program
def execExpression(env, e):

    evalT = evalTerm(env, e)
    evalF = evalFormula(env, e)

    if evalF != None:
        return evalF

    if evalT != None:
        return evalT

# Question 2d
# interpret() tokenizes a given string and parses it to generate a parse tree

def regexp(tokenlist):

    str = "|".join(tokenlist)
    str = str.replace('+', '\+')
    str = str.replace('*', '\*')
    str = str.replace('(', '\(')
    str = str.replace(')', '\)')

    return str

def tokenize(terminals, s):

    tokens = re.split(r"(\s+|"+ regexp(terminals) +"|,|\(|\))", s.replace(' ',''))
    return [t for t in tokens if not t.isspace() and not t == ""]

def interpret(s):

    terminals = ['and', 'nonzero', 'not', 'true', 'false', '(', ')', '+', '*', 'if', 'print', 'assign', ';', ':=',
                 '{', '}', 'do', 'until']
    tokens = tokenize(terminals, s)
    print('tokens = ', tokens)

    if len(tokens) == 0:
        return []
    p = program(tokens)
    print('p = ', p)
    if not p is None:
        output = execProgram({}, p[0])
        if output is not None:
            return output[1]
