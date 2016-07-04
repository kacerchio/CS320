import re

############################################################
# Load the files. Change the path if necessary.

exec(open('parse.py').read())
exec(open('interpret.py').read())

interpretCheck = open('interpret.py').read()
if interpretCheck.find('import parse') != -1 or\
   interpretCheck.find('from parse import') != -1 or\
   interpretCheck.find("exec(open('parse.py').read())") == -1:
    print('''You did not load the parse.py module correctly. You must use "exec(open('parse.py').read())". Exiting.''')
    exit()

def check(name, function, inputs_result_pairs):
    def str_(s):
        return '"'+str(s)+'"' if type(s) == str else str(s)
    if type(name) == tuple:
        prefix = name[0]
        suffix = name[1]
    if type(name) == str:
        prefix = name + '('
        suffix = ')'

    passed = 0
    for (inputs, result) in inputs_result_pairs:
        try:
            output = function(inputs[0], inputs[1]) if len(inputs) == 2  else function(inputs[0])
        except:
            output = '<Error>'

        if output != '<Error>' and output == result:
            passed = passed + 1
        else:
            print("\n  Failed on:\n    "+prefix+', '.join([str_(i) for i in inputs])+suffix+"\n\n"+"  Should be:\n    "+str_(result)+"\n\n"+"  Returned:\n    "+str_(output)+"\n")
    print("Passed " + str(passed) + " of " + str(len(inputs_result_pairs)) + " tests.")
    print("")

############################################################
# The tests.

print("Problem #1, part (a), variable()...")
try: variable
except: print("The variable() function is not defined.")
else: check('variable', variable, [\
    ((["x"],), ('x', [])),\
    ((["test"],), ('test', [])),\
    ((["camelNotation123"],), ('camelNotation123', [])),\
    ((["123"],), None),\
    ((["123abc"],), None),\
    ])

print("Problem #1, part (a), number()...")
try: number
except: print("The number() function is not defined.")
else: check('number', number, [\
    ((["123"],), (123, [])),\
    ((["0"],), (0, [])),\
    ((["1010"],), (1010, [])),\
    ((["-1010"],), None),\
    ((["a45"],), None),\
    ((["abc"],), None),\
    ])

print("Problem #1, part (b), formula()...")
try: formula
except: print("The formula() function is not defined.")
else: check('formula', formula, [\
    (("true".split(" "),), ('True', [])),\
    (("false".split(" "),), ('False', [])),\
    (("true and false".split(" "),), ({'And': ['True', 'False']}, [])),\
    (("x123 and y456".split(" "),), ({'And': [{'Variable': ['x123']}, {'Variable': ['y456']}]}, [])),\
    (("x".split(" "),), ({'Variable': ['x']}, [])),\
    (("x and foo".split(" "),), ({'And': [{'Variable': ['x']}, {'Variable': ['foo']}]}, [])),\
    (("true and false and true and false".split(" "),), ({'And': ['True', {'And': ['False', {'And': ['True', 'False']}]}]}, [])),\
    (("x and y and z and true".split(" "),), ({'And': [{'Variable': ['x']}, {'And': [{'Variable': ['y']}, {'And': [{'Variable': ['z']}, 'True']}]}]}, [])),\
    (("nonzero ( 0 ) and false".split(" "),), ({'And': [{'Nonzero': [{'Number':[0]}]}, 'False']}, [])),\
    (("0 + 1".split(" "),), None),\
    (("( 0 + 1 )".split(" "),), None),\
    (("0 and 1".split(" "),), None),\
    (("not 123".split(" "), True,), None),\
    (("not true".split(" "), True,), None),\
    (("not ( true )".split(" "), True,), ({'Not':['True']},[])),\
    ])

print("Problem #1, part (c), term()...")
try: term
except: print("The term() function is not defined.")
else: check('term', term, [\
    (("123".split(" "),), ({'Number':[123]}, [])),\
    (("0".split(" "),), ({'Number':[0]}, [])),\
    (("x".split(" "),), ({'Variable': ['x']}, [])),\
    (("0 + 1".split(" "),), ({'Plus': [{'Number': [0]}, {'Number': [1]}]}, [])),\
    (("x + ( 1 + 2 )".split(" "),), ({'Plus': [{'Variable': ['x']}, {'Parens': [{'Plus': [{'Number': [1]}, {'Number': [2]}]}]}]}, [])),\
    (("( x + 1 ) + 2".split(" "),), ({'Plus': [{'Parens': [{'Plus': [{'Variable': ['x']}, {'Number': [1]}]}]}, {'Number': [2]}]}, [])),\
    (("1 + 2 * 3" .split(" "),), ({'Plus': [{'Number': [1]}, {'Mult': [{'Number': [2]}, {'Number': [3]}]}]}, [])),\
    (("( 1 + 2 ) * 3" .split(" "),), ({'Mult': [{'Parens': [{'Plus': [{'Number': [1]}, {'Number': [2]}]}]}, {'Number': [3]}]}, [])),\
    (("1 + 2 * 3 + 4".split(" "),), ({'Plus': [{'Number': [1]}, {'Plus': [{'Mult': [{'Number': [2]}, {'Number': [3]}]}, {'Number': [4]}]}]}, [])),\
    (("1 + 2 + if ( false , 2 , 3 ) + 0".split(" "),), ({'Plus': [{'Number': [1]}, {'Plus': [{'Number': [2]}, {'Plus': [{'If': ['False', {'Number':[2]}, {'Number':[3]}]}, {'Number': [0]}]}]}]}, [])),\
    (("if ( a and b , 2 , 3 ) + 1".split(" "),), ({'Plus': [{'If': [{'And': [{'Variable': ['a']}, {'Variable': ['b']}]}, {'Number': [2]}, {'Number': [3]}]}, {'Number': [1]}]}, [])),\
    ])

print("Problem #1, part (d), program()...")
try: program
except: print("The program() function is not defined.")
else: check('program', program, [\
    (("print true ;".split(" "),), ({'Print': ['True', 'End']}, [])),\
    (("assign x := 3 + 4 ; print x * x ;".split(" "),), ({'Assign': [{'Variable': ['x']}, {'Plus': [{'Number': [3]}, {'Number': [4]}]}, {'Print': [{'Mult': [{'Variable': ['x']}, {'Variable': ['x']}]}, 'End']}]}, [])),\
    (("assign x := true and false ; print false ;".split(" "),), ({'Assign': [{'Variable': ['x']}, {'And': ['True', 'False']}, {'Print': ['False', 'End']}]}, [])),\
    (("if true { print 1 ; } print 0 ;".split(" "),), ({'If': ['True', {'Print': [{'Number': [1]}, 'End']}, {'Print': [{'Number': [0]}, 'End']}]}, [])),\
    (("do { if false { print 0 ; } print 1 ; } until true ; print 2 ;".split(" "),), ({'DoUntil': [{'If': ['False', {'Print': [{'Number': [0]}, 'End']}, {'Print': [{'Number': [1]}, 'End']}]}, "True", {'Print': [{'Number': [2]}, 'End']}]}, [])),\
    (("assign x := 1 + 2 ; do { assign y := a and b ; } until false ;".split(" "),), ({'Assign': [{'Variable': ['x']}, {'Plus': [{'Number': [1]}, {'Number': [2]}]}, {'DoUntil': [{'Assign': [{'Variable': ['y']}, {'And': [{'Variable': ['a']}, {'Variable': ['b']}]}, 'End']}, 'False', 'End']}]}, [])),\
    (([],), ('End', [])),\
    (("print 1 + 2 + if ( z , 2 , 3 ) + 0 ; assign y := 1 + 2 + z + 0 ; print if ( true , 2 , 3 ) + y ;".split(" "),), ({'Print': [{'Plus': [{'Number': [1]}, {'Plus': [{'Number': [2]}, {'Plus': [{'If': [{'Variable': ['z']}, {'Number': [2]}, {'Number': [3]}]}, {'Number': [0]}]}]}]}, {'Assign': [{'Variable': ['y']}, {'Plus': [{'Number': [1]}, {'Plus': [{'Number': [2]}, {'Plus': [{'Variable': ['z']}, {'Number': [0]}]}]}]}, {'Print': [{'Plus': [{'If': ['True', {'Number': [2]}, {'Number': [3]}]}, {'Variable': ['y']}]}, 'End']}]}]}, [])),\
    (("assign x := true ; do { assign x := false ; } until x ; print x ;".split(" "),), ({'Assign': [{'Variable': ['x']}, 'True', {'DoUntil': [{'Assign': [{'Variable': ['x']}, 'False', 'End']}, {'Variable': ['x']}, {'Print': [{'Variable': ['x']}, 'End']}]}]}, [])),\
    (("prong true ;".split(" "), True), None),\
    (("print true ; false ;".split(" "), True), None),\
    (("123 ;".split(" "), True), None),\
    (("123 + 456".split(" "), True), None),\
    (("if { print true ; }".split(" "), True), None),\
    ])

print("Problem #2, part (a), evalTerm()...")
try: evalTerm
except: print("The evalTerm() function is not defined.")
else: check('evalTerm', evalTerm, [\
    (({}, {'Number': [123]}), {'Number': [123]}),\
    (({'x':{'Number': [10]}}, {'Variable': ['x']}), {'Number': [10]}),\
    (({}, {'Plus': [{'Number': [1]}, {'Plus': [{'Mult': [{'Number': [2]}, {'Number': [3]}]}, {'Number': [4]}]}]}), {'Number': [11]}),\
    (({}, {'Plus': [{'Number': [0]}, {'Number': [1]}]}), {'Number': [1]}),\
    (({'x':{'Number': [2]}, 'y':{'Number': [3]}}, {'Plus': [{'Variable': ['y']}, {'Variable': ['x']}]}), {'Number': [5]}),\
    (({'z':'True'}, {'If': [{'Variable': ['z']}, {'Number': [1]}, {'Number': [2]}]}), {'Number': [1]}),\
    (({'x':{'Number': [4]}}, {'Parens': [{'Plus': [{'Number': [1]}, {'Number': [2]}]}]}), {'Number': [3]}),\
    (({'x':{'Number': [4]}}, {'Plus': [{'Variable': ['x']}, {'Parens': [{'Plus': [{'Number': [1]}, {'Number': [2]}]}]}]}), {'Number': [7]}),\
    ])

print("Problem #2, part (b), evalFormula()...")
try: evalFormula
except: print("The evalFormula() function is not defined.")
else: check('evalFormula', evalFormula, [\
    (({}, 'True'), 'True'),\
    (({}, {'And': ['True', 'True']}), 'True'),\
    (({'x':'True'}, {'Variable':['x']}), 'True'),\
    (({'x':'True', 'y':'False'}, {'And': [{'Variable': ['y']}, {'Variable': ['x']}]}), 'False'),\
    (({}, {'And': ['True', 'False']}), 'False'),\
    (({'x':'False'}, {'Parens': [{'And': [{'Parens': [{'And': ['True', {'Variable': ['x']}]}]}, 'False']}]}), None),\
    ])

print("Problem #2, part (c), execProgram()...")
try: execProgram
except: print("The execProgram() function is not defined.")
else: check('execProgram', execProgram, [\
    (({}, 'End'), ({}, [])),\
    (({}, {'Print': ['False', 'End']}), ({}, ['False'])),\
    (({'y':'False'}, {'Print': [{'Variable':['y']}, 'End']}), ({'y': 'False'}, ['False'])),\
    (({'x':{'Number':[123]}}, {'Assign': [{'Variable': ['x']}, 'True', {'Print': [{'Variable': ['x']}, 'End']}]}), ({'x': 'True'}, ['True'])),\
    (({}, {'Assign': [{'Variable': ['x']}, 'True', {'If': [{'Nonzero': [{'Number': [123]}]}, {'DoUntil': [{'Print': [{'Number': [123]},'End']},{'Variable': ['x']},'End']}, {'Print': [{'Variable': ['x']}, 'End']}]}]}), ({'x': 'True'}, [{'Number':[123]}, 'True'])),\
   ])

print("Problem #2, part (d), interpret()...")
try: interpret
except: print("The interpret() function is not defined.")
else: check('interpret', interpret, [\
    (("print true;",), ['True']),\
    (("print 1 + 2 + 3;",), [{'Number':[6]}]),\
    (("assign x := 3+4 ; print x*x+1;",), [{'Number':[50]}]),\
    (("assign x := true; if x { print x; } print x;",), ['True', 'True']),\
    (("assign x := false; do { print x; assign x := true; } until x; print x;",), ['False', 'True']),\
    (("",), []),\
    (("assign x := 0; if nonzero(123) {  do { print 123; assign x := 1; } until nonzero(x);  } print x;",), [{'Number':[123]}, {'Number':[1]}]),\
    (("assign x := false; if not(x) { do { print 456; assign x := not(x); } until x and true ; } print x;",), [{'Number':[456]}, 'True']),\
    (("assign x := true; assign y := true; do { do { print x; assign y := x and y; } until x; assign x := x and true; } until y; print x; print y;",), ['True', 'True', 'True']),\
    ])

#eof
