'''

Kristel Tan (ktan@bu.edu)
CAS CS320 Fall 2015 - Professor Lapets
Assignment 4 - interpret.py
Skeleton code from Professor Lapets

'''

exec(open('parse.py').read())

from functools import reduce
import operator

Node = dict
Leaf = str

# Question 1a
# subst(s, a) takes a substitution and an abstract syntax tree and
# returns a new abstract syntax tree in which all valid variable
# substitutions according to 's' have been made

def subst(s, a):

    if type(a) == Node:

        for key in a:
            label = key
            children = a[label]
            if label != 'Variable':
                return {label: [subst(s, child) for child in children]}
            else:
                key = children[0]
                try:
                    return s[key]
                except:
                    return a

    elif (type(a) == Leaf) or (type(a) == int):
        return a

# Question 1b
# unify(s, a) takes two syntax trees and returns the smallest substitution
# that satisfies the equation subst(s, a) == subst(s, b)

def unify(a, b):

    if (a == b) and (type(a) == Leaf or type(a) == int):
        return {}

    elif (type(a) == Node) and 'Variable' in a:
        return {a['Variable'][0]: b}

    elif (type(b) == Node) and 'Variable' in b:
        return {b['Variable'][0]: a}

    elif (type(a) == Node) and (type(b) == Node):

        for keyA in a:
            for keyB in b:
                labelA, labelB = keyA, keyB

        if 'Variable' in [labelA, labelB]:
            if labelA == 'Variable':
                return {a[labelA][0]: b}
            else:
                return {b[labelB][0]: a}

        elif (labelA == labelB) and (len(a[labelA]) == len(b[labelB])):
            childrenA = a[labelA]
            childrenB = b[labelB]
            zipped = list(zip(childrenA, childrenB))
            sub = {}
            for x, y in zipped:
                u = unify(x, y)
                if u is None:
                    return None
                elif u:
                    if u.keys() == sub.keys():
                        return None
                    else:
                        sub.update(u)
                else:
                    pass

            return sub

# Question 2a
# build(m, d) takes a finite map and a declaration parse tree and
# returns the finite map that represents the module definition according
# to the operational semantics given

def build(m, d):

    if type(d) == Leaf and d == 'End':
        return m

    elif type(d) == Node:

        for label in d:

            children = d[label]

            name = children[0]['Variable'][0]
            ptrn = children[1]
            exp = children[2]
            rest = children[3]
            t = (ptrn, exp)

            if name in m:
                m[name] += [t]
            else:
                m.update({name: [t]})

            return build(m, rest)

# Question 2b
# evaluate(m, env e) takes a module, environment, and an expression abstract
# syntax tree and returns the value that corresponds to the evaluation
# of the abstract syntax tree 'e' as determined by the operational semantics

def evaluate(m, env, e):

    if type(e) == Node:

        for label in e:

            children = e[label]

            if label == 'ConInd':
                con = children[0]
                v1 = evaluate(m, env, children[1])
                v2 = evaluate(m, env, children[2])
                return {'ConInd': [con, v1, v2]}

            elif label == 'ConBase' or label == 'Number':
                return e

            elif label == 'Variable':
                var = children[0]
                if var in env:
                    return env[var]
                else:
                    print(var + ' is unbound')
                    exit()

            elif label == 'Mult':
                left = children[0]
                right = children[1]
                n1 = evaluate(m, env, left)
                n2 = evaluate(m, env, right)
                return n1 * n2

            elif label == 'Apply':
                name = children[0]['Variable'][0]
                v1 = evaluate(m, env, children[1])
                if name in m:
                    for i in m[name]:
                        u = unify(v1, i[0])
                        if not u is None:
                            return evaluate(m, u, i[1])

def interact(s):
    # Build the module definition.
    m = build({}, parser(grammar, 'declaration')(s))

    # Interactive loop.
    while True:
        # Prompt the user for a query.
        s = input('> ') 
        if s == ':quit':
            break
        
        # Parse and evaluate the query.
        e = parser(grammar, 'expression')(s)
        if not e is None:
            print(evaluate(m, {}, e))
        else:
            print("Unknown input.")

#eof