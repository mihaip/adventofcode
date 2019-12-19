#!/usr/local/bin/python3

import collections
import os

IN = 1
OUT = 2

with open("input.txt") as f:
    program = [int(word) for word in f.readline().split(",")]

class VM(object):
    def __init__(self, program, input=None):
        self.program = collections.defaultdict(int)
        for i, instruction in enumerate(program.copy()):
            self.program[i] = instruction
        self.input = input
        self.outputs = []
        self.pc = 0
        self.relative_base = 0
        self.halted = False

        self.instruction_defs = {}
        def add_instruction(op_code, param_types, impl, autoincrement_pc=True):
            self.instruction_defs[op_code] = [param_types, impl, autoincrement_pc]

        add_instruction(1, [IN, IN, OUT], lambda a, b: a + b) # add
        add_instruction(2, [IN, IN, OUT], lambda a, b: a * b) # multiply
        add_instruction(3, [OUT], lambda: self.input) # read input
        add_instruction(4, [IN], lambda a: self.outputs.append(a)) # output value
        add_instruction(5, [IN, IN], self.jump_if_true, autoincrement_pc=False)  # jump-if-true
        add_instruction(6, [IN, IN], self.jump_if_false, autoincrement_pc=False) # jump-if-false
        add_instruction(7, [IN, IN, OUT], lambda a, b: 1 if a < b else 0)  # less than
        add_instruction(8, [IN, IN, OUT], lambda a, b: 1 if a == b else 0)  # equals
        add_instruction(9, [IN], self.set_relative_base)  # adjust the relative base
        add_instruction(99, [], self.halt) # halt

    def run(self):
        while not self.halted:
            self.step()

    def run_until_output(self):
        initial_output_len = len(self.outputs)
        while len(self.outputs) == initial_output_len:
            self.step()
            if self.halted:
                break
        return self.outputs[-1]

    def step(self):
        instruction = self.program[self.pc]
        op_code = instruction % 100
        mode1 = int(instruction/100) % 10
        mode2 = int(instruction/1000) % 10
        mode3 = int(instruction/10000) % 10
        def apply_in_mode(param, mode):
            if mode == 0:
                return self.program[param]
            elif mode == 1:
                return param
            elif mode == 2:
                return self.program[param + self.relative_base]
            else:
                raise Exception("Unexpected in mode %d", mode)

        def apply_out_mode(param, mode):
            if mode == 0:
                return param
            elif mode == 2:
                return param + self.relative_base
            else:
                raise Exception("Unexpected out mode %d", mode)

        if op_code not in self.instruction_defs:
            raise Exception("Unexpected op code %d", op_code)

        param_types, impl, autoincrement_pc = self.instruction_defs[op_code]
        # TODO: generify if we end up with many parameter types
        if param_types == [IN, IN, OUT]:
            in1 = apply_in_mode(self.program[self.pc + 1], mode1)
            in2 = apply_in_mode(self.program[self.pc + 2], mode2)
            out = apply_out_mode(self.program[self.pc + 3], mode3)
            self.program[out] = impl(in1, in2)
        elif param_types == [IN, IN]:
            in1 = apply_in_mode(self.program[self.pc + 1], mode1)
            in2 = apply_in_mode(self.program[self.pc + 2], mode2)
            impl(in1, in2)
        elif param_types == [IN]:
            in1 = apply_in_mode(self.program[self.pc + 1], mode1)
            impl(in1)
        elif param_types == [OUT]:
            out = apply_out_mode(self.program[self.pc + 1], mode1)
            self.program[out] = impl()
        elif param_types == []:
            impl()
        else:
            raise Exception("Unexpected parameter types %s", param_types)

        if autoincrement_pc:
            self.pc += len(param_types) + 1

    def jump_if_true(self, a, b):
        if a != 0:
            self.pc = b
        else:
            self.pc += 3

    def jump_if_false(self, a, b):
        if a == 0:
            self.pc = b
        else:
            self.pc += 3

    def set_relative_base(self, a):
        self.relative_base += a

    def halt(self):
        self.halted = True

    def fork(self):
        fork = VM([], self.input)
        fork.program = self.program.copy()
        fork.output = self.outputs.copy()
        fork.pc = self.pc
        fork.relative_base = self.relative_base
        fork.halted = self.halted
        return fork

DIRECTIONS = [
    (1, 0, -1), # north
    (2, 0, 1), # south
    (3, -1, 0), # west
    (4, 1, 0), # east
]

def move(input_vm, depth, visited, x, y):
    best_result = None
    for direction, dx, dy in DIRECTIONS:
        direction_x = x + dx
        direction_y = y + dy
        k = (direction_x, direction_y)
        if k in visited:
            continue
        direction_visited = visited.copy()
        direction_visited.add(k)
        vm = input_vm.fork()
        vm.input = direction
        status = vm.run_until_output()
        if status == 0: # wall
            continue
        elif status == 1: # moved
            direction_result = move(vm, depth + 1, direction_visited, direction_x, direction_y)
            if direction_result is not None and (best_result is None or direction_result[0] < best_result[0]):
                best_result = direction_result
        elif status == 2: # oxygen!
            best_result = (depth, direction_x, direction_y)
    return best_result


vm = VM(program)
oxygen_depth, oxygen_x, oxygen_y = move(vm, 1, visited=set(), x=0, y=0)
print("oxygen is %d moves away at %d, %d" % (oxygen_depth, oxygen_x, oxygen_y))
