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
        add_instruction(3, [OUT], lambda: self.input.pop(0)) # read input
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
        
DELTAS = [[0, -1], [1, 0], [0, 1], [-1, 0]]
DIRECTIONS = {"^": 0, ">": 1, "v": 2, "<": 3}
TEST_ASCII = """#######...#####
#.....#...#...#
#.....#...#...#
......#...#...#
......#...###.#
......#.....#.#
^########...#.#
......#.#...#.#
......#########
........#...#..
....#########..
....#...#......
....#...#......
....#...#......
....#####......"""

def analyze(grid):
	lines = [l for l in grid.splitlines() if l]
	height = len(lines)
	result = 0
	for y, line in enumerate(lines):
		width = len(line)
		for x in range(width):
			g = line[x]
			if g in DIRECTIONS:
				return x, y, DIRECTIONS[g]
	assert False

def compute_path(x, y, orientation, grid):
	lines = [l for l in grid.splitlines() if l]
	height = len(lines)
	width = len(lines[0])
	def get(x, y):
		if x < 0 or x >= width or y < 0 or y >= height:
			return None
		return lines[y][x]
	def step(orientation):
		dx, dy = DELTAS[orientation]
		return x + dx, y + dy
		
	path = []
	current_distance = 0
	while True:
		next_x, next_y = step(orientation)
		# Continue along current direction
		if get(next_x, next_y) == "#":
			current_distance += 1
			x = next_x
			y = next_y
			continue
		if current_distance:
			path.append(str(current_distance + 1))
			current_distance = 0
		# Try to turn right		
		next_orientation = (orientation + 1) % 4
		next_x, next_y = step(next_orientation)
		if get(next_x, next_y) == "#":
			path.append("R")
			x = next_x
			y = next_y
			orientation = next_orientation
			continue		
		# Try to turn left	
		next_orientation = (orientation + 3) % 4
		next_x, next_y = step(next_orientation)
		if get(next_x, next_y) == "#":
			path.append("L")
			x = next_x
			y = next_y
			orientation = next_orientation
			continue
		break
	return path
	

vm = VM(program)
vm.run()
ascii = "".join(map(chr, vm.outputs))
# ascii = TEST_ASCII
print("ASCII:\n%s" % ascii)
start_x, start_y, orientation = analyze(ascii)
print("start at %d,%d in direction %d" % (start_x, start_y, orientation))
path = compute_path(start_x, start_y, orientation, ascii)

def list_find(list, sublist, start_index):
	for i in range(start_index, len(list)):
		if list[i:i+len(sublist)] == sublist:
			return i
	return -1
	
def list_replace(list, sublist, replacement):
	while True:
		replacement_index = list_find(list, sublist, 0)
		if replacement_index == -1:
			return list
		list[replacement_index:replacement_index + len(sublist)] = replacement

def find_repeats(path, start):
	#print("  find_repeats(%s, %d)" % (path, start))
	previous = None
	for i in range(2, len(path) - 2, 2):
		sub_path = path[start:start + i]
		#print("    %d: %s" % (i, sub_path))		
		if "A" in sub_path or "B" in sub_path:
			#print("      into another pattern, stopping")
			return previous
			continue
		count = 0
		start_index = start
		while True:
			start_index = list_find(path, sub_path, start_index)
			if start_index == -1:
				break
			count += 1
			start_index = start_index + len(sub_path)
		#print("      count: %d" % count)			
		if count == 1:
			#print("    count 1, returning")
			return previous
		previous = sub_path
	assert False

def find_best_repeats(path):
#	print("find_best_repeats(%s)" % path)
	best = None
	for i in range(0, len(path), 2):
		repeat = find_repeats(path, i)
		if not repeat or len(",".join(repeat)) > 18:
			continue
		if best is None or len(repeat) > len(best):
			best = repeat
	return best

print("path: %s" % ",".join(path))
"""
Aborted attempt at automatically compressing
a = find_best_repeats(path)
paths = list_replace(path, a, ["A"])
b = find_best_repeats(path)
path = list_replace(path, b, ["B"])
c = find_best_repeats(path)
path = list_replace(path, c, ["C"])
print("A: %s" % ",".join(a))
print("B: %s" % ",".join(b))
print("C: %s" % ",".join(c))
print("path: %s" % ",".join(path))
"""

R = "A,B,A,C,A,B,C,A,B,C"
A = "R,12,R,4,R,10,R,12"
B = "R,6,L,8,R,10"
C = "L,8,R,4,R,4,R,6"

cleaning_program = program.copy()
cleaning_program[0] = 2
vm = VM(cleaning_program, input=list(map(ord, "%s\n%s\n%s\n%s\nn\n" % (R, A, B, C))))
vm.run()
print("output: %s" % vm.outputs)
