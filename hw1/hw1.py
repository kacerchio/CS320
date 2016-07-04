'''

Kristel Tan (ktan@bu.edu)
CAS CS320 Fall 2015 - Professor Lapets
hw1.py 

'''

import re
import string

# Question 1a
# regexp() takes a list of tokens and returns a single string
def regexp(tokenlist):

    str = "|".join(tokenlist)
    str = str.replace('$', '\$')
    str = str.replace('+', '\+')
    str = str.replace('*', '\*')
    str = str.replace('(', '\(')
    str = str.replace(')', '\)')
    str = str.replace('?', '\?')

    return str

print("\nTesting re.match(regexp([\"abc\", \"def\", \"xyz\"]), \"abc\")...")
print(re.match(regexp(["abc", "def", "xyz"]), "abc"))

print("\nTesting re.match(regexp([\"abc\", \"def\", \"xyz\"]), \"ghi\")...")
print(re.match(regexp(["abc", "def", "xyz"]), "ghi"))


# Question 1b
# tokenize() takes a list of terminals and a concrete syntax
# character to tokenize and build a regular expression
def tokenize(terminals, s):

    tokens = re.split(r"(\s+|"+ regexp(terminals) +"|,|\(|\))", s.replace(' ',''))
    return [t for t in tokens if not t.isspace() and not t == ""]

print("\nTesting tokenize([\"red\", \"blue\", \"#\"], \"red#red blue# red#blue\")...")
print(tokenize(["red", "blue", "#"], "red#red blue# red#blue"))

# Question 1c
# tree() takes a token sequence and parses it into a tree
def tree(tokens):
    
    if len(tokens) > 3:
        if tokens[0] == 'two' and tokens[1] == 'children' and tokens[2] == 'start':
            (e1, tokens) = tree(tokens[3:])
            if tokens[0] == ';':
                (e2, tokens) = tree(tokens[1:])
                if tokens[0] == 'end':
                    return ({'Two':[e1, e2]}, tokens[1:])

    if len(tokens) > 3:
        if tokens[0] == 'one' and tokens[1] == 'child' and tokens[2] == 'start':
            (e1, tokens) = tree(tokens[3:])
            if tokens[0] == 'end':
                return ({'One':[e1]}, tokens[1:])

    if len(tokens) > 1:
        if tokens[0] == 'zero' and tokens[1] == 'children':
            return ('Zero', tokens[2:])

print("\nTesting tokenize([\"children\", \"child\", \"two\", \"one\", " \
        "\"zero\", \"start\", \"end\", \";\"], \"one child start two children start one child"
      "start zero children end; zero children end end\")...")

t = tokenize(["children", "child", "two", "one", "zero", "start", "end", ";"],
                  "one child start two children start one child start zero children end; zero children end end")

print (tree(t))


#------------------------------- Question 3 encompasses and modifies parts of Question 2 ------------------------------#


# Given number() function from assignment
# Modified regular expression to allow for positive and negative integers for Question 3
def number(tokens):

    if re.match(r"^(0|[1-9][0-9]*|-[1-9][0-9]*)$", tokens[0]):
        return ({"Number": [int(tokens[0])]}, tokens[1:])


# Question 2a
# variable() takes a token sequence and parses it into a tree,
# indicating if the root node is a variable
def variable(tokens):

    if re.match(r"^([a-zA-z]+)$", tokens[0]):
        return({"Variable": [tokens[0]]}, tokens[1:])

print("\nTesting variable(['x', ':=', '#', '2', ';', 'end', ';'])...")
print(variable(['x', ':=', '#', '2', ';', 'end', ';']))


# Question 2b
# term() takes a token sequence and parses it into a tree, indicating
# the appropriate root node according to the grammar definition
def term(tmp, top = True):

    tokens = tmp[0:]
    if tokens[0] == '#':
        return (number(tokens[1:]))

    tokens = tmp[0:]
    if tokens[0] == '$':
        return(variable(tokens[1:]))

    tokens = tmp[0:]
    if tokens[0] == 'plus' and tokens[1] == '(':
        tokens = tokens[2:]
        r = term(tokens, False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == ',':
                tokens = tokens[1:]
                r = term(tokens, False)
                if not r is None:
                    (e2, tokens) = r
                    if tokens[0] == ')':
                        tokens = tokens[1:]
                        if not top or len(tokens) == 0:
                            return ({'Plus':[e1,e2]}, tokens)

    tokens = tmp[0:]
    if tokens[0] == 'max' and tokens[1] == '(':
        tokens = tokens[2:]
        r = term(tokens, False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == ',':
                tokens = tokens[1:]
                r = term(tokens, False)
                if not r is None:
                    (e2, tokens) = r
                    if tokens[0] == ')':
                        tokens = tokens[1:]
                        if not top or len(tokens) == 0:
                            return ({'Max':[e1,e2]}, tokens)

    tokens = tmp[0:]
    if tokens[0] == 'if' and tokens[1] == '(':
        tokens = tokens[2:]
        r = formula(tokens, False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == ',':
                tokens = tokens[1:]
                r = term(tokens, False)
                if not r is None:
                    (e2, tokens) = r
                    if tokens[0] == ',':
                        tokens = tokens[1:]
                        r = term(tokens, False)
                        if not r is None:
                            (e3, tokens) = r
                            if tokens[0] == ')':
                                tokens = tokens[1:]
                                if not top or len(tokens) == 0:
                                    return ({'If':[e1,e2,e3]}, tokens)

    tokens = tmp[0:]
    if tokens[0] == '(':
        tokens = tokens[1:]
        r = term(tokens, False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == '+':
                tokens = tokens[1:]
                r = term(tokens, False)
                if not r is None:
                    (e2, tokens) = r
                    if tokens[0] == ')':
                        tokens = tokens[1:]
                        if not top or len(tokens) == 0:
                            return ({'Plus':[e1,e2]}, tokens)

    tokens = tmp[0:]
    if tokens[0] == '(':
        tokens = tokens[1:]
        r = term(tokens, False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == 'max':
                tokens = tokens[1:]
                r = term(tokens, False)
                if not r is None:
                    (e2, tokens) = r
                    if tokens[0] == ')':
                        tokens = tokens[1:]
                        if not top or len(tokens) == 0:
                            return({'Max':[e1, e2]}, tokens)

    tokens = tmp[0:]
    if tokens[0] == '(':
        tokens = tokens[1:]
        r = formula(tokens, False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == '?':
                tokens = tokens[1:]
                r = term(tokens, False)
                if not r is None:
                    (e2, tokens) = r
                    if tokens[0] == ':':
                        tokens = tokens[1:]
                        r = term(tokens, False)
                        if not r is None:
                            (e3, tokens) = r
                            if tokens[0] == ')':
                                tokens = tokens[1:]
                                if not top or len(tokens) == 0:
                                    return({'If':[e1,e2,e3]}, tokens)

    return None

print("\nTesting term(['max', '(', 'plus', '(', '#', '2', ',', '#', '3', ')', ',', '#', '4', ')'])...")
print(term(['max', '(', 'plus', '(', '#', '2', ',', '#', '3', ')', ',', '#', '4', ')']))


# Question 2c
# formula() takes a token sequence and parses it into a tree, indicating
# the appropriate root node according to the grammar definition
def formula(tmp, top = True):

    tokens = tmp[0:]
    if tokens[0] == 'true':
        tokens = tokens[1:]
        if not top or len(tokens) == 0:
            return ('True', tokens)

    tokens = tmp[0:]
    if tokens[0] == 'false':
        tokens = tokens[1:]
        if not top or len(tokens) == 0:
            return ('False', tokens)

    tokens = tmp[0:]
    if tokens[0] == 'not' and tokens[1] == '(':
        tokens = tokens[2:]
        r = formula(tokens, False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == ')':
                tokens = tokens[1:]
                if not top or len(tokens) == 0:
                    return({'Not':[e1]}, tokens)

    tokens = tmp[0:]
    if tokens[0] == 'xor' and tokens[1] == '(':
        tokens = tokens[2:]
        r = formula(tokens, False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == ',':
                tokens = tokens[1:]
                r = formula(tokens, False)
                if not r is None:
                    (e2, tokens) = r
                    if tokens[0] == ')':
                        tokens = tokens[1:]
                        if not top or len(tokens) == 0:
                            return ({'Xor':[e1,e2]}, tokens)

    tokens = tmp[0:]
    if tokens[0] == 'equal' and tokens[1] == '(':
        tokens = tokens[2:]
        r = term(tokens, False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == ',':
                tokens = tokens[1:]
                r = term(tokens, False)
                if not r is None:
                    (e2, tokens) = r
                    if tokens[0] == ')':
                        tokens = tokens[1:]
                        if not top or len(tokens) == 0:
                            return ({'Equal':[e1,e2]}, tokens)

    tokens = tmp[0:]
    if tokens[0] == 'less' and tokens[1] == '(':
        tokens = tokens[2:]
        r = term(tokens, False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == ',':
                tokens = tokens[1:]
                r = term(tokens, False)
                if not r is None:
                    (e2, tokens) = r
                    if tokens[0] == ')':
                        tokens = tokens[1:]
                        if not top or len(tokens) == 0:
                            return ({'Less':[e1,e2]}, tokens)

    tokens = tmp[0:]
    if tokens[0] == 'greater' and tokens[1] == '(':
        tokens = tokens[2:]
        r = term(tokens, False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == ',':
                tokens = tokens[1:]
                r = term(tokens, False)
                if not r is None:
                    (e2, tokens) = r
                    if tokens[0] == ')':
                        tokens = tokens[1:]
                        if not top or len(tokens) == 0:
                            return ({'Greater':[e1,e2]}, tokens)

    tokens = tmp[0:]
    if tokens[0] == '(':
        tokens = tokens[1:]
        r = formula(tokens, False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == 'xor':
                tokens = tokens[1:]
                r = formula(tokens, False)
                if not r is None:
                    (e2, tokens) = r
                    if tokens[0] == ')':
                        tokens = tokens[1:]
                        if not top or len(tokens) == 0:
                            return({'Xor':[e1,e2]}, tokens)

    tokens = tmp[0:]
    if tokens[0] == '(':
        tokens = tokens[1:]
        r = term(tokens, False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == '==':
                tokens = tokens[1:]
                r = term(tokens, False)
                if not r is None:
                    (e2, tokens) = r
                    if tokens[0] == ')':
                        tokens = tokens[1:]
                        if not top or len(tokens) == 0:
                            return({'Equal':[e1, e2]}, tokens)

    tokens = tmp[0:]
    if tokens[0] == '(':
        tokens = tokens[1:]
        r = term(tokens, False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == '<':
                tokens = tokens[1:]
                r = term(tokens, False)
                if not r is None:
                    (e2, tokens) = r
                    if tokens[0] == ')':
                        tokens = tokens[1:]
                        if not top or len(tokens) == 0:
                            return({'Less':[e1, e2]}, tokens)

    tokens = tmp[0:]
    if tokens[0] == '(':
        tokens = tokens[1:]
        r = term(tokens, False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == '>':
                tokens = tokens[1:]
                r = term(tokens, False)
                if not r is None:
                    (e2, tokens) = r
                    if tokens[0] == ')':
                        tokens = tokens[1:]
                        if not top or len(tokens) == 0:
                            return({'Greater':[e1, e2]}, tokens)



print("\nTesting formula(['greater', '(', '#', '12', ',', '#', '34', ')'])...")
print(formula(['greater', '(', '#', '12', ',', '#', '34', ')']))


# Question 2d
# program() takes a token sequence and parses it into a tree, indicating
# the appropriate root node according to the grammar definition
def program(tmp, top = True):

    tokens = tmp[0:]
    if tokens[0] == 'print':
        r = term(tokens[1:], False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == ';':
                r = program(tokens[1:], False)
                if not r is None:
                    (e2, tokens) = r
                    tokens = tokens[1:]
                    if not top or len(tokens) == 0:
                        return ({'Print':[e1, e2]}, tokens)

    tokens = tmp[0:]
    if tokens[0] == 'input' and tokens[1] == '$':
        r = variable(tokens[2:])
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == ';':
                r = program(tokens[1:], False)
                if not r is None:
                    (e2, tokens) = r
                    tokens = tokens[1:]
                    if not top or len(tokens) == 0:
                        return ({'Input':[e1, e2]}, tokens)

    tokens = tmp[0:]
    if tokens[0] == 'assign' and tokens[1] == '$':
        r = variable(tokens[2:])
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == ':=':
                r = term(tokens[1:], False)
                if not r is None:
                    (e2, tokens) = r
                    if tokens[0] == ';':
                        r = program(tokens[1:], False)
                        if not r is None:
                            (e3, tokens) = r
                            tokens = tokens[1:]
                            if not top or len(tokens) == 0:
                                return({'Assign':[e1, e2, e3]}, tokens)

    tokens = tmp[0:]
    if tokens[0] == 'end' and tokens[1] == ';':
        tokens = tokens[2:]
        if not top or len(tokens) == 0:
            return('End', tokens)


print("\nTesting program(['input', '$', 'x', ';', 'assign', '$', 'y', ':=', '#', '320', ';', 'end', ';'])")

print(program(['input', '$', 'x', ';', 'assign', '$', 'y', ':=', '#', '320', ';', 'end', ';']))
print(program(['print', '#', '123', ';', 'print', '#', '456', ';', 'end', ';']))


# Question 2e
# parse() takes a string and returns a parse tree corresponding to the input
# string if it conforms to the grammar of the programming language
def parse(concreteSyntax):

    terminals = ['print', 'input', 'assign', ':=', 'end', ';', 'true', 'false', 'not', 'xor',
                 'equal', 'less', 'greater', '#', '$', 'plus', 'max', 'if', '==',
                 '<', '>', '+', '?', ':']

    tokens = tokenize(terminals, concreteSyntax)

    if program(tokens) is None:
        return None
    else:
        return program(tokens)[0]

print("\nTesting program(['print', '#', '10', ';', 'end', ';'])...")

print(parse("print # 123 ; print # 456 ; end ;"))
print('\n')
print('------------------------------------------------------------------------------------------------------\n\n')
