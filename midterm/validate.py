'''

Kristel Tan (ktan@bu.edu)
CAS CS320 Fall 2015 - Professor Lapets
Midterm - validate.py
Skeleton code from Professor Lapets

'''

exec(open('analyze.py').read())
exec(open('interpret.py').read())
exec(open('compile.py').read())

Node = dict
Leaf = str

def convertValue(v):

    if type(v) == Leaf:
        if v == 'True':
            return 1
        elif v == 'False':
            return 0

    if type(v) == Node:
        for label in v:
            children = v[label]
            if v == 'Number':
                return children[0]

# Converts an output (a list of values) from the
# value representation to the machine representation
def convert(o):
    return [convertValue(v) for v in o]

def expressions(n):
    if n <= 0:
        return []
    elif n == 1:
        return ['True', 'False']
    else:
        es = expressions(n-1)
        esN = [{'Element': [{'Variable': ['x']}, e]} for e in es]
        esN += [{'Variable': ['x']}]
        esN += [{'Number': [1]}]
        return es + esN

def programs(n):
    if n <= 0:
        return []
    elif n == 1:
        return ['End']
    else:
        ps = programs(n-1)
        es = expressions(n-1)
        psN = []
        psN += [{'Print': [e1, p]} for e1 in es for p in ps]
        psN += [{'Assign': [{'Variable': ['a']}, e2, e2, e2, p]} for p in ps for e2 in es]
        psN += [{'Loop': [{'Variable': ['x']}, {'Number': [1]}, p1, p2]} for p1 in ps for p2 in ps]
        return ps + psN
   
# Compute the formula that defines correct behavior for the
# compiler for all program parse trees of depth at most k.
# Any outputs indicate that the behavior of the compiled
# program does not match the behavior of the interpreted
# program.

def exhaustive(k):
    for p in programs(k):
        try:
            if simulate(compileProgram({}, p)[1]) != convert(execProgram({}, p)[1]):
                print('\nIncorrect behavior on: ' + str(p))
        except:
            print('\nError on: ' + str(p))

print(exhaustive(2))

#eof