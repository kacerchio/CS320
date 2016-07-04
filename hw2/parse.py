'''

Kristel Tan (ktan@bu.edu)
CAS CS320 Fall 2015 - Professor Lapets
parse.py

'''

import re

# List of reserved words needed to make sure that variable() parses them according to the production
reservedWords = ['true', 'false', 'nonzero', 'not', 'and', 'print', 'assign', 'if', 'do', 'until']

# Question 1a

# Modified code for variable() parser from Assignment 1
# Parses token sequences that conform to any alphanumeric string
# beginning with a lowercase alphabetical letter
def variable(tokens):

    if re.match(r"^([a-z][a-zA-Z0-9]*)$", tokens[0]) and tokens[0] not in reservedWords:
        return (tokens[0], tokens[1:])
    else:
        return None

# Modified code for number() parser from Assignment 1
# Parses token sequences that conform to any valid non-negative integer
def number(tokens):

    if re.match(r"^0|([1-9][0-9]*)$", tokens[0]):
        return (int(tokens[0]), tokens[1:])
    else:
        return None

# Question 1b

# formula() parses token sequences that conform to the 'formula' productions
# using the left() function to help perform left-recursion elimination
def formula(tokens, top=True):

    (e1, tokens) = left(tokens)

    if e1 is not None:
        if tokens:
            if tokens[0] == 'and':
                (e2, tokens) = formula(tokens[1:])
                if e2 is not None:
                    return ({'And': [e1, e2]}, tokens)
                return (None, None)
        return (e1, tokens)
    return None

def left(tokens):

    if tokens[0] == 'not' and tokens[1] == '(':
        tokens = tokens[2:]
        r = formula(tokens)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == ')':
                tokens = tokens[1:]
                return({'Not':[e1]}, tokens)

    if tokens[0] == 'nonzero' and tokens[1] == '(':
        tokens = tokens[2:]
        r = term(tokens)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == ')':
                tokens = tokens[1:]
                return({'Nonzero':[e1]}, tokens)

    if tokens[0] == 'true':
        return ('True', tokens[1:])

    if tokens[0] == 'false':
        return ('False', tokens[1:])

    r = variable(tokens)
    if not r is None:
        (e1, tokens) = variable(tokens)
        if e1 is not None:
            return ({'Variable': [e1]}, tokens)
    return None, None

# Question 1c

# term() parses token sequences that conform to the 'term' productions
def term(tokens):

    (e1, tokens) = factor(tokens)

    if e1 is not None:
        if tokens:
            if tokens[0] == '+':
                (e2, tokens) = term(tokens[1:])
                if e2 is not None:
                    return ({'Plus': [e1, e2]}, tokens)
                return (None, None)
        return (e1, tokens)
    return None

# factor() parses token sequences that conform to the 'factor' productions
# using the fleft() to help perform left-recursion elimination
def factor(tokens, top=True):

    (e1, tokens) = fleft(tokens)

    if e1 is not None:
        if tokens:
            if tokens[0] == '*':
                (e2, tokens) = factor(tokens[1:])
                if e2 is not None:
                    return ({'Mult': [e1, e2]}, tokens)
                return (None, None)
        return (e1, tokens)
    return None, None

def fleft(tokens):

    if tokens[0] == '(':
        tokens = tokens[1:]
        r = term(tokens)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == ')':
                tokens = tokens[1:]
                return({'Parens':[e1]}, tokens)

    if tokens[0] == 'if' and tokens[1] == '(':
        tokens = tokens[2:]
        r = formula(tokens)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == ',':
                tokens = tokens[1:]
                r = term(tokens)
                if not r is None:
                    (e2, tokens) = r
                    if tokens[0] == ',':
                        tokens = tokens[1:]
                        r = term(tokens)
                        if not r is None:
                            (e3, tokens) = r
                            if tokens[0] == ')':
                                tokens = tokens[1:]
                                return({'If':[e1,e2,e3]}, tokens)

    var = variable(tokens)
    num = number(tokens)
    if var is not None:
        (e1, tokens) = variable(tokens)
        if e1 is not None:
            return ({'Variable': [e1]}, tokens)
    if num is not None:
        (e1, tokens) = number(tokens)
        if e1 is not None:
            return ({'Number':[e1]}, tokens)
    else:
        return None, None

# Question 1d

# program() parses token sequences that conform to the 'program'
# production using expression() as a helper parser

def program(tokens, top=True):

    if len(tokens) == 0 or tokens[0] == '}':
        return ('End', tokens)

    else:

        if tokens[0] == 'print':
            r = expression(tokens[1:])
            if not r is None:
                (e1, tokens) = r
                if tokens[0] == ';':
                    r = program(tokens[1:])
                    if not r is None:
                        (e2, tokens) = r
                        tokens = tokens[1:]
                        return ({'Print':[e1,e2]}, tokens)

        elif tokens[0] == 'assign':
            r = variable(tokens[1:])
            if not r is None:
                (e1, tokens) = r
                if tokens[0] == ':=':
                    (e2, tokens) = expression(tokens[1:])
                    if e2 is not None:
                        if tokens[0] == ';':
                            r = program(tokens[1:])
                            if not r is None:
                                (e3, tokens) = r
                                tokens = tokens[1:]
                                return ({'Assign':[{'Variable':[e1]}, e2,e3]}, tokens)

        elif tokens[0] == 'if':
            r = expression(tokens[1:])
            if not r is None:
                (e1, tokens) = r
                if tokens[0] == '{':
                    r = program(tokens[1:])
                    if not r is None:
                        (e2, tokens) = r
                        if tokens is not None:
                            r = program(tokens[0:])
                            if not r is None:
                                (e3, tokens) = r
                                return ({'If':[e1,e2,e3]}, tokens)

        elif tokens[0] == 'do' and tokens[1] == '{':
            r = program(tokens[2:])
            if not r is None:
                (e1, tokens) = r
                if tokens[0] == 'until':
                    r = expression(tokens[1:])
                    if not r is None:
                        (e2, tokens) = r
                        if tokens[0] == ';':
                            r = program(tokens[1:])
                            if not r is None:
                                (e3, tokens) = r
                                tokens = tokens[1:]
                                if len(tokens) == 0:
                                    return ({'DoUntil':[e1,e2,e3]}, tokens)

        return None

def expression(tokens):

    f = formula(tokens)
    t = term(tokens)

    if f is not None and t is not None:
        if len(f[1]) > len(t[1]):
            return t
    if f is not None:
        (e1, tokens) = formula(tokens)
        if e1 is not None:
            return f
    elif t is not None:
        (e1, tokens) = term(tokens)
        if e1 is not None:
            return t
    else:
        return None
