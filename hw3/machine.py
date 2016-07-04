'''

Kristel Tan (ktan@bu.edu)
CAS CS320 Fall 2015 - Professor Lapets
Assignment 3 - machine.py
Skeleton code from Professor Lapets

'''

def simulate(s):
    instructions = s if type(s) == list else s.split("\n")
    instructions = [l.strip().split(" ") for l in instructions]
    mem = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: -1, 6: 0}
    control = 0
    outputs = []
    while control < len(instructions):
        # Update the memory address for control.
        mem[6] = control 
        
        # Retrieve the current instruction.
        inst = instructions[control]
        
        # Handle the instruction.
        if inst[0] == 'label':
            pass
        if inst[0] == 'goto':
            control = instructions.index(['label', inst[1]])
            continue
        if inst[0] == 'branch' and mem[int(inst[2])]:
            control = instructions.index(['label', inst[1]])
            continue
        if inst[0] == 'jump':
            control = mem[int(inst[1])]
            continue
        if inst[0] == 'set':
            mem[int(inst[1])] = int(inst[2])
        if inst[0] == 'copy':
            mem[mem[4]] = mem[mem[3]]
        if inst[0] == 'add':
            mem[0] = mem[1] + mem[2]

        # Push the output address's content to the output.
        if mem[5] > -1:
            outputs.append(mem[5])
            mem[5] = -1

        # Move control to the next instruction.
        control = control + 1

    print("memory: "+str(mem))
    return outputs

# Examples of useful helper functions from lecture.    
def copy(frm, to):
   return [
      'set 3 ' + str(frm),
      'set 4 ' + str(to),
      'copy'
   ]

# Helper function that cleans up any memory addresses used by
# setting them back to 0

def cleanup():
    return ['set 0 0 ',
            'set 1 0 ',
            'set 2 0 ',
            'set 3 0 ',
            'set 4 0 '
            ]

# Question 2a
# increment() returns a list of instructions that correspond to a machine
# language program that increments by 1 the integer stored in
# memory location addr and cleans up any memory addresses used in the process

def increment(addr):
    return copy(addr, 1) + \
           ['set 2 1 ', 'add '] + \
           copy(0, str(addr)) + cleanup()

# Question 2b
# decrement() returns a list of instructions that correspond to a machine
# language program that decrements by 1 the integer stored in
# memory location addr and cleans up any memory addresses used in the process

def decrement(addr):
    return copy(addr, 1) + \
           ['set 2 -1 ',
            'add '] + \
           copy(0, str(addr)) + cleanup()

# Question 2c
# call() returns a list of instructions that corresponding to the name of
# a procedure

def call(name):
    return decrement(7) + \
           copy(7,4) + \
           ['set 3 6 ',
            'copy '] + \
           copy(7,3) + \
           ['set 4 2 ',
            'copy ',
            'set 1 14 ',
            'add '] + \
           copy(7,4) +\
           ['set 3 0 ',
            'copy ',
            'goto ' + name] +\
           increment(7)

# Question 2d
# procedure() returns a sequence of instructions

def procedure(name, body):
    return ['goto ' + name + 'end',
            'label ' + name] + \
           body + \
           ['set 3 7',
            'set 4 3',
            'copy',
            'set 4 0',
            'copy',
            'jump 0',
            'label ' + name + 'end']

# eof
