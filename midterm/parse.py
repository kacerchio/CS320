'''

Kristel Tan (ktan@bu.edu)
CAS CS320 Fall 2015 - Professor Lapets
Midterm - parse.py
Skeleton code from Professor Lapets

'''

import re

def number(tokens, top = True):
    if re.compile(r"(-(0|[1-9][0-9]*)|(0|[1-9][0-9]*))").match(tokens[0]):
        return ({"Number": [int(tokens[0])]}, tokens[1:])

def variable(tokens, top = True):
    if re.compile(r"[a-z][A-Za-z0-9]*").match(tokens[0]):
        return ({"Variable": [tokens[0]]}, tokens[1:])

'''
expression	::=	true
            |	false
            |   number
            |	$ variable
            |	expression + expression
            |	@ variable [ expression ]

after left recursion...

expression  ::= left + expression
            |   left

left        ::= true
            |   false
            |   number
            |   $ variable
            |   @ variable [ expression ]
'''

def parse(seqs, tmp, top = True):

    for (label, seq) in seqs:
        tokens = tmp[0:]
        (ss, es) = ([], [])

        for x in seq:
            if type(x) == type(""):
                if tokens[0] == x:
                    tokens = tokens[1:]
                    ss = ss + [x]
                else:
                    break
            else:
                r = x(tokens, False)
                if not r is None:
                    (e, tokens) = r
                    es = es + [e]

        if len(ss) + len(es) == len(seq):
            if not top or len(tokens) == 0:
                return {label:es} if len(es) > 0 else label, tokens

def expression(tmp, top = True):

    tokens = tmp[0:]
    r = left(tokens, False)

    if not r is None:
        (e1, tokens) = r
        if len(tokens) > 0 and tokens[0] == '+':
            r = expression(tokens[1:], False)
            if not r is None:
                (e2, tokens) = r
                return {'Plus':[e1, e2]}, tokens
        else:
            return e1, tokens

def left(tmp, top = True):

    r = parse([('True', ['true']),
               ('False', ['false']),
               ('Element', ['@', variable, '[', expression, ']'])],
              tmp, top)

    if not r is None:
        return r

    tokens = tmp[0:]
    r = number(tokens, False)
    if not r is None:
        return r

    tokens = tmp[0:]
    if tokens[0] == '$':
        r = variable(tokens[1:], False)
        if not r is None:
            return r

'''

program	::=	@ variable := [ expression , expression , expression ] ; program
        |	print expression ; program
        |   loop $ variable from number { program } program
        |

'''

def program(tmp, top = True):

    if len(tmp) == 0:
        return('End', [])

    r = parse([('Assign', ['@', variable, ':=', '[', expression, ',', expression, ',', expression, ']', ';', program]),
               ('Print', ['print', expression, ';', program]),
               ('Loop', ['loop', '$', variable, 'from', number, '{', program, '}', program]),
               ('End', [])],
               tmp, top)

    if not r is None:
        return r

def tokenizeAndParse(s):
    tokens = re.split(r"(\s+|:=|print|\+|loop|from|{|}|;|\[|\]|,|@|\$)", s)
    tokens = [t for t in tokens if not t.isspace() and not t == ""]
    (p, tokens) = program(tokens)
    return p

#eof