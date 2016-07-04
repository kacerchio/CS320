'''

Kristel Tan (ktan@bu.edu)
CAS CS320 Fall 2015 - Professor Lapets
Midterm - compile.py
Skeleton code from Professor Lapets

'''

from random import randint
exec(open('parse.py').read())
exec(open('interpret.py').read())
exec(open('optimize.py').read())
exec(open('machine.py').read())
exec(open('analyze.py').read())

Leaf = str
Node = dict

def freshStr():
    return str(randint(0,10000000))

def compileExpression(env, e, heap):

    if type(e) == Leaf:

        if e == 'True':
            heap += 1
            inst = ['set ' + str(heap) + ' 1']
            return inst, heap, heap

        if e == 'False':
            heap += 1
            inst = ['set ' + str(heap) + ' 0']
            return inst, heap, heap

    if type(e) == Node:

        for label in e:
            children = e[label]

            if label == 'Number':
                n = children[0]
                heap += 1
                return ['set ' + str(heap) + ' ' + str(n)], heap, heap

            elif label == 'Variable':
                heap += 1
                x = children[0]
                if x in env:
                    return [], env[x], heap
                else:
                    print(x + ' is unbound')
                    exit()

            elif label == 'Element':
                (insts1, addr1, heap) = compileExpression(env, children[0], heap)
                (insts2, addr2, heap) = compileExpression(env, children[1], heap)
                heap += 1
                instsElement = copy(addr2, 1) + \
                               ['set 2 ' + str(addr1), 'add '] + \
                               copyFromRef(0, heap)
                return (insts1 + insts2 + instsElement), heap, heap

            elif label == 'Plus':
                (insts1, addr1, heap) = compileExpression(env, children[0], heap)
                (insts2, addr2, heap) = compileExpression(env, children[1], heap)
                heap += 1
                instsPlus = copy(addr1, 1) + \
                            copy(addr2, 2) + \
                            ['add '] + \
                            copy(0, heap)
                return (insts1 + insts2 + instsPlus), heap, heap

# Set initial heap default address
def compileProgram(env, s, heap = 8):

    if type(s) == Leaf:
        if s == 'End':
            return env, [], heap

    if type(s) == Node:
        for label in s:
            children = s[label]

            if label == 'Print':
                [e, p] = children
                (insts1, addr, heap) = compileExpression(env, e, heap)
                (env, insts2, heap) = compileProgram(env, p, heap)
                return env, insts1 + copy(addr, 5) + insts2, heap

            elif label == 'Assign':
                var = children[0]['Variable'][0]
                heapArrayStart = heap + 1
                heapArrayEnd = heapArrayStart + 3

                (insts1, addr1, heap1) = compileExpression(env, children[1], heapArrayEnd)
                (insts2, addr2, heap2) = compileExpression(env, children[2], heap1)
                (insts3, addr3, heap3) = compileExpression(env, children[3], heap2)

                rest = children[4]
                env[var] = heapArrayStart
                instsAssign = copy(addr1, heapArrayStart) + \
                              copy(addr2, heapArrayStart + 1) + \
                              copy(addr3, heapArrayStart + 2)
                (env, insts4, heap4) = compileProgram(env, rest, heap3)

                return env, (insts1 + insts2 + insts3 + instsAssign + insts4), heap4

            elif label == 'Loop':
                [var, num, p1, p2] = children
                var = var['Variable'][0]
                (env, insts1, heap1) = compileProgram(env, p1, heap)
                (env, insts2, heap2) = compileProgram(env, p2, heap1)

                instsLoop = ['set 2 ' + str(num),
                             'label loopStart' + str(heap),
                             'set 1 1',
                             'add',
                             'branch loopCond' + str(heap),
                             'goto loopEnd' + str(heap),
                             'label loopCond' + str(heap),
                             'set 2 ' + str(num - 1)] + insts1 +\
                            ['goto loopStart' + str(heap),
                             'label loopEnd' + str(heap)] + insts2

                return env, instsLoop, heap2

def compile(s):
    p = tokenizeAndParse(s)

    # Add calls to type checking and optimization algorithms.
    if typeProgram({}, p) != None:
        p = foldConstants(p)
        p = eliminateDeadCode(p)
    (env, insts, heap) = compileProgram({}, p)
    return insts

def compileAndSimulate(s):
    return simulate(compile(s))

#eof
