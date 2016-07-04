import re

############################################################
# Load the files being tested.

exec(open('parse.py').read())
exec(open('interpret.py').read())

interpretCheck = open('interpret.py').read()
if interpretCheck.find('import parse') != -1 or\
   interpretCheck.find('from parse import') != -1 or\
   interpretCheck.find("exec(open('parse.py').read())") == -1:
    print('''You did not load the parse.py module correctly in interpret.py. You must use "exec(open('parse.py').read())". Exiting.''')
    exit()

def check(function, inputs_result_pairs):
    def str_(s): return '"'+str(s)+'"' if type(s) == str else str(s)
    (prefix, suffix) = (function + '(', ')')

    passed = 0
    for (inputs, result) in inputs_result_pairs:
        try: output = eval(function)(*inputs)
        except: output = None
        if output == result: passed = passed + 1
        else: print("\n  Failed on:\n    "+prefix+', '.join([str_(i) for i in inputs])+suffix+"\n\n"+"  Should be:\n    "+str(result)+"\n\n"+"  Returned:\n    "+str(output)+"\n")
    print("Passed " + str(passed) + " of " + str(len(inputs_result_pairs)) + " tests.")
    print("")

############################################################
# The tests.

print("Problem #1, part (a), subst()...")
try: subst
except: print("The subst() function is not defined.\n")
else: check('subst', [\
    (({"x":{"Number":[5]}}, {"Variable":['x']}), {"Number":[5]}),\
    (({"y":{"Number":[2]}}, {"Plus":[{"Variable":['y']}, {"Variable":['y']}]}), {"Plus":[{"Number":[2]}, {"Number":[2]}]}),\
    (({"a":"True", "b":{"Number":[2]}}, {"Mult":[{"Variable":['y']}, {"Variable":['a']}]}), {"Mult":[{"Variable":['y']}, "True"]}),\
    (({"a":{"Number":[1]}, "b":{"Number":[2]}}, {"Mult":[{"Plus":[{"Variable":['y']}, {"Variable":['y']}]}, {"Variable":['b']}]}), {"Mult":[{"Plus":[{"Variable":['y']}, {"Variable":['y']}]}, {"Number":[2]}]}),\
    (({"z":{"Abc":["Def", "Ghi"]}}, {"Jkl":[{"Variable":['y']}, {"Variable":['z']}]}), {"Jkl":[{"Variable":['y']}, {"Abc":["Def", "Ghi"]}]}),\
    ])

def testUnify(x, y):
    if type(x) == dict and type(y) == dict: # Testing abstract syntax trees.
        return unify(x, y)
    elif type(x) == str and type(y) == str: # Testing concrete syntax strings.
        return unify(parser(grammar, 'expression')(x), parser(grammar, 'expression')(y))

print("Problem #1, part (b), unify()...")
try: unify
except: print("The unify() function is not defined.\n")
else: check('testUnify', [\
    (("x", "5"), {"x":{"Number":[5]}}),\
    (("x", "5 * 5"), {"x":{'Mult': [{'Number': [5]}, {'Number': [5]}]}}),\
    (("a * b", "5 * 5"), {"a":{'Number': [5]}, "b":{'Number': [5]}}),\
    (("False * True", "True * False"), None),\
    (("c", "Test"), {"c":{'ConBase': ['Test']}}),\
    (("Node x y", "Node Leaf Leaf"), {"x":{'ConBase': ['Leaf']}, "y":{'ConBase': ['Leaf']}}),\
    (("Node (Node x y) Leaf", "Node (Node Leaf Leaf) Leaf"), {"x":{'ConBase': ['Leaf']}, "y":{'ConBase': ['Leaf']}}),\
    (("Node (Node a b) (Node x y)", "Node (Node (Node Leaf Leaf) Leaf) (Node Leaf Leaf)"), {"a":{'ConInd': ['Node', {'ConBase': ['Leaf']}, {'ConBase': ['Leaf']}]}, "b":{'ConBase': ['Leaf']}, "x":{'ConBase': ['Leaf']}, "y":{'ConBase': ['Leaf']}}),\
    (({"Abc":[{"Variable":['x']}, "Ghi"]}, {"Abc":["Def", "Ghi"]}), {"x":"Def"}),\
    (("Leaf", "Leaf"), {}),\
    (({"Example":[{"Variable":['x']}, {"Example":[{"Variable":['a']}, {"Test3":["Test4"]}, "Test0"]}]}, {"Example":["Test1", {"Example":["Test2", {"Variable":['b']}, "Test0"]}]}), {'b': {'Test3': ['Test4']}, 'x': 'Test1', 'a': 'Test2'}),\
    (({"Example":[{"Variable":['x']}, "Test0"]}, {"Example":["Test1", {"Variable":['x']}]}), None),\
    (("Node (Node Leaf Leaf) Leaf", "Node (Node Leaf Leaf) Leaf"), {}),\
    (("And True False", "And True False"), {}),\
    (("Or x y", "Or True False"), {"x":{'ConBase': ['True']}, "y":{'ConBase': ['False']}}),\
    ])

def testEvaluate(d, e):
    return evaluate(build({}, parser(grammar, 'declaration')(d)), {}, parser(grammar, 'expression')(e))

print("Problem #2, part (b), evaluate()...")
try: evaluate
except: print("The evaluate() function is not defined.\n")
else: check('testEvaluate', [\
    (("f(Leaf) = Leaf;", "f(Leaf)"), {'ConBase': ['Leaf']}),\
    (("f(x) = Test;", "f(Test)"), {'ConBase': ['Test']}),\
    (("f(Node t1 t2) = True; f(Leaf) = False;", "f(Leaf)"), {'ConBase': ['False']}),\
    (("f(Node t1 t2) = g(True); f(Leaf) = False; g(True) = False; g(False) = True;", "f(Leaf)"), {'ConBase': ['False']}),\
    (("f(Node t1 t2) = g(g(True)); f(Leaf) = g(False); g(True) = False; g(False) = True;", "f(Leaf)"), {'ConBase': ['True']}),\
    (("new(Node t1 t2) = NewNode new(t1) new(t2); new(Leaf) = NewLeaf;", "new(Leaf)"), {'ConBase': ['NewLeaf']}),\
    (("new(Node t1 t2) = NewNode new(t1) new(t2); new(Leaf) = NewLeaf;", "new(Node Leaf Leaf)"), {'ConInd':['NewNode', {'ConBase': ['NewLeaf']}, {'ConBase': ['NewLeaf']}]}),\
    ])

#eof