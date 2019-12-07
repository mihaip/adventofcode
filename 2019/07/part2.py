#!/usr/local/bin/python3

import itertools

IN = 1
OUT = 2

with open("input.txt") as f:
    program = [int(word) for word in f.readline().split(",")]

class VM(object):
    def __init__(self, program, inputs=None):
        self.program = program.copy()
        self.inputs = inputs or []
        self.outputs = []
        self.pc = 0
        self.halted = False
        self.on_output = None

        self.instruction_defs = {}
        def add_instruction(op_code, param_types, impl, autoincrement_pc=True):
            self.instruction_defs[op_code] = [param_types, impl, autoincrement_pc]

        add_instruction(1, [IN, IN, OUT], lambda a, b: a + b) # add
        add_instruction(2, [IN, IN, OUT], lambda a, b: a * b) # multiply
        add_instruction(3, [OUT], lambda: self.inputs.pop(0)) # read input
        add_instruction(4, [IN], lambda a: self.outputs.append(a)) # output value
        add_instruction(5, [IN, IN], self.jump_if_true, autoincrement_pc=False)  # jump-if-true
        add_instruction(6, [IN, IN], self.jump_if_false, autoincrement_pc=False) # jump-if-false
        add_instruction(7, [IN, IN, OUT], lambda a, b: 1 if a < b else 0)  # less than
        add_instruction(8, [IN, IN, OUT], lambda a, b: 1 if a == b else 0)  # equals
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
        def apply_mode(param, mode):
            return param if mode else self.program[param]

        if op_code not in self.instruction_defs:
            raise Exception("Unexpected op code %d", op_code)

        param_types, impl, autoincrement_pc = self.instruction_defs[op_code]
        # TODO: generify if we end up with many parameter types
        if param_types == [IN, IN, OUT]:
            in1, in2, out = self.program[self.pc + 1:self.pc + 4]
            in1 = apply_mode(in1, mode1)
            in2 = apply_mode(in2, mode2)
            self.program[out] = impl(in1, in2)
        elif param_types == [IN, IN]:
            in1, in2 = self.program[self.pc + 1:self.pc + 3]
            in1 = apply_mode(in1, mode1)
            in2 = apply_mode(in2, mode2)
            impl(in1, in2)
        elif param_types == [IN]:
            in1 = self.program[self.pc + 1]
            in1 = apply_mode(in1, mode1)
            impl(in1)
        elif param_types == [OUT]:
            out = self.program[self.pc + 1]
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

    def halt(self):
        self.halted = True

def try_sequence(sequence):
    amps = []
    for i, setting in enumerate(sequence):
        inputs = [setting]
        if i == 0:
            inputs.append(0)
        amps.append(VM(program, inputs=inputs))

    while not amps[-1].halted:
        for i, amp in enumerate(amps):
            output = amp.run_until_output()
            next_amp = amps[(i + 1) % len(amps)]
            next_amp.inputs.append(output)

    return amps[-1].outputs[-1]

best_sequence = None
best_output = 0
for sequence in itertools.permutations(range(5, 10)):
    current_output = try_sequence(sequence)
    if current_output > best_output:
        best_output = current_output
        best_sequence = sequence

print("best output %d for sequence %s" % (best_output, best_sequence))
