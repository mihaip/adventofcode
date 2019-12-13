#!/usr/local/bin/python3

import collections

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

inputs = []
location = [0, 0]
min_x = None
max_x = None
min_y = None
max_y = None
directions = [
    [0, -1], # up
    [1, 0], # right
    [0, 1], # down
    [-1, 0], # left
]
direction_labels = [
    "^",
    ">",
    "v",
    "<",
]
direction = 0
painted_panels = collections.defaultdict(int)
painted_locations = set()

def location_key():
    return f"{location[0]}-{location[1]}"

def get_color():
    return painted_panels[location_key()]

def set_color(color):
    global min_x, max_x, min_y, max_y
    x, y = location
    if min_x is None or x - 1 < min_x:
        min_x = x - 1
    if max_x is None or x + 1 > max_x:
        max_x = x + 1
    if min_y is None or y - 1 < min_y:
        min_y = y - 1
    if max_y is None or y + 1 > max_y:
        max_y = y + 1
    painted_panels[location_key()] = color
    painted_locations.add(location_key())

def print_panels():
    for y in range(min_y, max_y + 1):
        line = ""
        for x in range(min_x, max_x + 1):
            color = painted_panels[f"{x}-{y}"]
            if y == location[1] and x == location[0]:
                line += direction_labels[direction]
            elif color:
                line += "#"
            else:
                line += "."
        print(line)

vm = VM(program)
iterations = 0
while not vm.halted:
    # print("location: %s" % location)
    vm.input = get_color()
    # print("  input: %s" % vm.input)
    new_color = vm.run_until_output()
    # print("  new_color: %d" % new_color)
    turn_right = vm.run_until_output()
    # print("  turn_right: %d" % turn_right)
    set_color(new_color)
    direction += 1 if turn_right else -1
    if direction < 0:
        direction += 4
    elif direction == 4:
        direction -= 4
    location[0] += directions[direction][0]
    location[1] += directions[direction][1]
    iterations += 1
    # print_panels()

print("%d outputs" % len(vm.outputs))
print_panels()

# Sample input
# iterations = 0
# for new_color, turn_right in ((1, 0), (0, 0), (1,0), (1,0), (0,1), (1,0), (1,0)):
#     print("location: %s" % location)
#     print("  input: %s" % get_color())
#     print("  new_color: %d" % new_color)
#     print("  turn_right: %d" % turn_right)
#     set_color(new_color)
#     direction += 1 if turn_right else -1
#     if direction < 0:
#         direction += 4
#     elif direction == 4:
#         direction -= 4
#     location[0] += directions[direction][0]
#     location[1] += directions[direction][1]
#     print_panels()
#     iterations += 1
#     if iterations > 100:
#         break

print("painted panels: %d in %d iterations" % (len(painted_locations), iterations))
