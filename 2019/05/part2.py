#!/usr/local/bin/python3

import sys

IN = 1
OUT = 2

current_input = 5
with open("input.txt") as f:
    program = [int(word) for word in f.readline().split(",")]

instruction_defs = {}

def add_instruction(op_code, param_types, impl, autoincrement_pc=True):
    instruction_defs[op_code] = [param_types, impl, autoincrement_pc]

def halt():
    print("halting")
    print("program: %s" % ",".join(map(str, program)))
    sys.exit()

def jump_if_true(a, b):
    global pc
    pc = b if a != 0 else pc + 3

def jump_if_false(a, b):
    global pc
    pc = b if a == 0 else pc + 3

add_instruction(1, [IN, IN, OUT], lambda a, b: a + b) # add
add_instruction(2, [IN, IN, OUT], lambda a, b: a * b) # multiply
add_instruction(3, [OUT], lambda: current_input) # write input
add_instruction(4, [IN], lambda a: print("output: %d" % a)) # output value
add_instruction(5, [IN, IN], jump_if_true, autoincrement_pc=False)  # jump-if-true
add_instruction(6, [IN, IN], jump_if_false, autoincrement_pc=False) # jump-if-false
add_instruction(7, [IN, IN, OUT], lambda a, b: 1 if a < b else 0)  # less than
add_instruction(8, [IN, IN, OUT], lambda a, b: 1 if a == b else 0)  # equals
add_instruction(99, [], halt) # halt

pc = 0
while True:
    instruction = program[pc]
    op_code = instruction % 100
    mode1 = int(instruction/100) % 10
    mode2 = int(instruction/1000) % 10
    def apply_mode(param, mode):
        return param if mode else program[param]

    if op_code not in instruction_defs:
        raise Exception("Unexpected op code %d", op_code)

    param_types, impl, autoincrement_pc = instruction_defs[op_code]
    # TODO: generify if we end up with many parameter types
    if param_types == [IN, IN, OUT]:
        in1, in2, out = program[pc + 1:pc + 4]
        in1 = apply_mode(in1, mode1)
        in2 = apply_mode(in2, mode2)
        program[out] = impl(in1, in2)
    elif param_types == [IN, IN]:
        in1, in2 = program[pc + 1:pc + 3]
        in1 = apply_mode(in1, mode1)
        in2 = apply_mode(in2, mode2)
        impl(in1, in2)
    elif param_types == [IN]:
        in1 = program[pc + 1]
        in1 = apply_mode(in1, mode1)
        impl(in1)
    elif param_types == [OUT]:
        out = program[pc + 1]
        program[out] = impl()
    elif param_types == []:
        impl()
    else:
        raise Exception("Unexpected parameter types %s", param_types)

    if autoincrement_pc:
        pc += len(param_types) + 1

halt()
