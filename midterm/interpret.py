'''

Kristel Tan (ktan@bu.edu)
CAS CS320 Fall 2015 - Professor Lapets
Midterm - interpret.py
Skeleton code from Professor Lapets

'''

exec(open('parse.py').read())

Node = dict
Leaf = str

def evalExpression(env, e):

    if type(e) == Leaf:
        if e == 'True':
            return 'True'
        if e == 'False':
            return 'False'

    if type(e) == Node:

        for label in e:
            children = e[label]

            if label == 'Number':
                e1 = children[0]
                return {'Number': [e1]}

            elif label == 'Variable':
                e1 = children[0]
                if e1 in env:
                    return env[e1]
                else:
                    print(e1 + ' is unbound')
                    exit()

            elif label == 'Element':
                var = children[0]['Variable'][0]
                i = children[1]
                e = evalExpression(env, i)
                if e in env:
                    if 0 <= e <= 2:
                        return env[var][e]

            elif label == 'Plus':
                e1 = children[0]
                e2 = children[1]
                v1 = evalExpression(env, e1)
                v2 = evalExpression(env, e2)
                return {'Number': [v1['Number'][0] + v2['Number'][0]]}

def execProgram(env, s):

    if type(s) == Leaf:
        if s == 'End':
            return env, []

    elif type(s) == Node:

        for label in s:
            children = s[label]

            if label == 'Print':
                [e,p] = s[label]
                v = evalExpression(env, e)
                (env, o) = execProgram(env, p)
                return env, [v] + o

            elif label == 'Assign':
                var = children[0]['Variable'][0]
                i1 = evalExpression(env, children[1])
                i2 = evalExpression(env, children[2])
                i3 = evalExpression(env, children[3])
                env[var] = [i1, i2, i3]
                (env, o) = execProgram(env, children[4])
                return env, o

            elif label == 'Loop':
                var = children[0]['Variable'][0]
                num = children[1]
                body = children[2]
                rest = children[3]
                if num < 0:
                    (env2, o1) = execProgram(env, body)
                    return env2, o1
                else:
                    num -= 1
                    env[var] = num
                    (env2, o1) = execProgram(env, body)
                    (env3, o2) = execProgram(env, {'Loop': [var, num, body, rest]})
                    return env3, o1 + o2

def interpret(s):
    (env, o) = execProgram({}, tokenizeAndParse(s))
    return o

#eof