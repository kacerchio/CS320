'''

Kristel Tan (ktan@bu.edu)
CAS CS320 Fall 2015 - Professor Lapets
Midterm - analyze.py
Skeleton code from Professor Lapets

'''

exec(open('parse.py').read())

Node = dict
Leaf = str

def typeExpression(env, e):

    if type(e) == Leaf:

        if e == 'True' or e == 'False':
            return 'TyBoolean'

    if type(e) == Node:

        for label in e:
            children = e[label]
            if label == 'Number':
                return 'TyNumber'

            elif label == 'Variable':
                var = children[0]
                return env[var]

            elif label == 'Element':
                [e1, e2] = e[label]
                e1 = e1['Variable'][0]
                t2 = typeExpression(env, e2)
                if e1 in env and e1 == 'TyArray' and t2 == 'TyNumber':
                    return 'TyNumber'

            elif label == 'Plus':
                [e1,e2] = e[label]
                t1 = typeExpression(env, e1)
                t2 = typeExpression(env, e2)
                if t1 == 'TyNumber' and t2 == 'TyNumber':
                    return 'TyNumber'

def typeProgram(env, s):

    if type(s) == Leaf:

        if s == 'End':
            return 'TyVoid'

    elif type(s) == Node:
        for label in s:
            if label == 'Print':
                [e, p] = s[label]
                t1 = typeExpression(env, e)
                t2 = typeProgram(env, p)
                if (t1 == 'TyBoolean' or t1 == 'TyBoolean') and t2 == 'TyVoid':
                    return 'TyVoid'

            if label == 'Assign':
                [xTree, e0, e1, e2, p] = s[label]
                x = xTree['Variable'][0]
                t1 = typeExpression(env, e0)
                t2 = typeExpression(env, e1)
                t3 = typeExpression(env, e2)
                if t1 == 'TyNumber' and t2 == 'TyNumber' and t3 == 'TyNumber':
                    env[x] = 'Array'
                    if typeProgram(env, p) == 'TyVoid':
                        return 'TyVoid'

            if label == 'Loop':
                [xTree, nTree, p1, p2] = s[label]
                x = xTree['Variable'][0]
                n = nTree['Number'][0]
                t1 = typeExpression(env, n)
                env[x] = t1
                t2 = typeProgram(env, p1)
                t3 = typeProgram(env, p2)
                if t1 == 'TyNumber' and t2 == 'TyVoid' and t3 == 'TyVoid':
                    return 'TyVoid'

#eof