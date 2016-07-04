'''

Kristel Tan (ktan@bu.edu)
CAS CS320 Fall 2015 - Professor Lapets
Assignment 3 - compile.py
Skeleton code from Professor Lapets

'''

exec(open('parse.py').read())
exec(open('machine.py').read())

Node = dict
Leaf = str

# Question 3a
# compileTerm() returns a tuple with a sequence of machine language instructions
# that perform the computation of represented by the parse tree, the address to of
# the result, and an integer representing the top of the heap after the computation is performed

def compileTerm(env, t, heap):

    insts = []
    if type(t) == Node:
        for label in t:
            children = t[label]

            if label == 'Variable':
                heap += 1
                if children[0] in env:
                    insts += copy(env[children[0]], heap)
                return insts, heap, heap

            elif label == 'Number':
                heap += 1
                insts = ['set ' + str(heap) + ' ' + str(children[0])]
                return insts, heap, heap

            elif label == 'Plus':
                heap += 1
                (insts1, t1, heap) = compileTerm(env, children[0], heap)
                (insts2, t2, heap) = compileTerm(env, children[1], heap)
                instsPlus = copy(t1, 1) + copy(t2, 2) + ['add '] + copy(0, heap)
                return (insts1 + insts2 + instsPlus), heap, heap

# Question 3b
# compileFormula() does the same thing as compileTerm() except that handles
# formula parse trees

def compileFormula(env, f, heap):

    insts = []
    if type(f) == Node:
        for label in f:
            children = f[label]

            if label == 'Variable':
                if children[0] in env:
                    insts += copy(env[children[0]], heap)
                return insts, heap, heap

            elif label == 'Not':
                (insts1, f1, heap) = compileFormula(env, children[0], heap)
                heap += 1
                instsNot = [
                            'branch not_setZero' + str(heap) + ' ' + str(f1),
                            'set ' + str(heap) + ' 1',
                            'goto not_Finish' + str(heap),
                            'label not_setZero' + str(heap),
                            'set ' + str(heap) + ' 0',
                            'label not_Finish' + str(heap)
                            ]
                return (insts1 + instsNot), f1, heap

            elif label == 'Xor':
                (insts1, f1, heap) = compileFormula(env, children[0], heap)
                (insts2, f2, heap) = compileFormula(env, children[1], heap)
                heap += 1
                instsXor = copy(f1, 1) + copy(f2, 2) + \
                           [
                            'add',
                            'branch xor_NonZero' + str(heap) + ' 0',
                            'goto xor_False' + str(heap),
                            'label xor_NonZero' + str(heap),
                           ] + decrement(0) + [
                            'branch xor_False' + str(heap) + ' 0',
                            'set ' + str(heap) + ' 1',
                            'goto xor_Finish' + str(heap),
                            'label xor_False' + str(heap),
                            'set ' + str(heap) + ' 0',
                            'label xor_Finish' + str(heap)
                           ]
                return (insts1 + insts2 + instsXor), heap, heap

            elif label == 'AndShort':
                (insts1, f1, heap) = compileFormula(env, children[0], heap)
                (insts2, f2, heap) = compileFormula(env, children[1], heap)
                heap += 1
                instsAnd = [
                            'branch andShort_False1' + str(heap) + str(f1),
                            'set ' + str(heap) + ' 0'
                            'goto andShort_Finish' + str(heap),
                            'label finish' + str(heap)
                            ]
                return (insts1 + insts2 + instsAnd), heap, heap


            elif label == 'And':
                (insts1, f1, heap) = compileFormula(env, children[0], heap)
                (insts2, f2, heap) = compileFormula(env, children[1], heap)
                heap += 1
                instsAnd = [
                            'set 2 -2',
                            'add ',
                            'branch and_False' + str(heap) + ' 0',
                            'set 0 1',
                            'goto and_Finish' + str(heap),
                            'label and_False' + str(heap),
                            'set 0 0',
                            'label and_Finish' + str(heap)
                            ]
                instsAnd += copy(0, heap)
                return (insts1 + insts2 + instsAnd), heap, heap

    if type(f) == Leaf:

        if f == 'True':
            heap += 1
            inst = ['set ' + str(heap) + ' 1']
            return inst, heap, heap

        if f == 'False':
            heap += 1
            inst = ['set '+ str(heap) + ' 0']
            return inst, heap, heap

# Question 3c
# compileProgram() returns a tuple with the an updated environment, a sequence of
# machine language instructions that perform the computation represented by the parse
# tree, and an integer representing the top of the heap after the computation is performed

def compileProgram(env, s, heap):

    if type(s) == Node:
        for label in s:
            children = s[label]

            if label == 'Assign':
                var = children[0]['Variable'][0]
                (insts1, s1, heap) = compileTerm(env, children[1], heap) or compileFormula(env, children[1], heap)

                if var in env:
                    insts1 += copy(s1, env[var])
                else:
                    env[var] = s1

                (env, insts2, heap) = compileProgram(env, children[2], heap)
                return env, (insts1 + insts2), heap

            elif label == 'Procedure':
                name = children[0]['Variable'][0]
                (envBody, instsBody, heapBody) = compileProgram(env, children[1], heap)
                instsProc = procedure(name, instsBody)
                (envRest, instsRest, heapRest) = compileProgram(envBody, children[2], heapBody)
                return envRest, instsProc + instsRest, heapRest

            elif label == 'Call':
                name = children[0]['Variable'][0]
                instsCall = call(name)
                (envRest, instsRest, heapRest) = compileProgram(env, children[1], heap)
                return envRest, instsCall + instsRest, heapRest

            elif label == 'Print':
                (insts1, s1, heap) = compileTerm(env, children[0], heap) or compileFormula(env, children[0], heap)
                insts2 = copy(heap, 5)
                (envRest, instsRest, heapRest) = compileProgram(env, children[1], heap)
                return envRest, (insts1 + insts2 + instsRest), heapRest

            elif label == 'If':
                (insts1, s1, heap) = compileTerm(env, children[0], heap) or compileFormula(env, children[0], heap)
                (env, insts2, heap) = compileProgram(env, children[1], heap)

                insts3 = [
                          'branch if_True' + str(heap) + ' ' + str(s1),
                          'goto if_Finish' + str(heap),
                          'label if_True' + str(heap)
                         ] + insts2 + \
                         [
                          'label if_Finish' + str(heap)
                         ]

                (env, insts3, heap) = compileProgram(env, children[2], heap)
                return env, (insts1 + insts2 + insts3), heap

            elif label == 'Until':
                (insts1, s1, heap) = compileTerm(env, children[0], heap) or compileFormula(env, children[0], heap)
                (env, insts2, heap) = compileProgram(env, children[1], heap)

                insts3 = [
                          'label until_Start' + str(heap),
                          'branch until_Finish' + str(heap) + ' ' + str(s1),
                          'goto until_Start' + str(heap),
                          'label until_Finish' + str(heap)
                          ]

                (env, insts3, heap) = compileProgram(env, children[2], heap)
                return env, (insts1 + insts2 + insts3), heap

    elif type(s) == Leaf:
        if s == 'End':
            return env, [], heap

# Question 3d
# compile() returns the compiied form (a sequence of instructions in the target machine
# language) of the string s

def compile(s):
    (env, insts, heap) = compileProgram({}, tokenizeAndParse(s), 8)
    return ['set 7 0'] + insts

#eof
