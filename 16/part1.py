#!/usr/local/bin/python3

import re

R = 1 # register input
I = 2 # immediate input
_ = 3 # ignored input

class Opcode:
	def __init__(self, name, input_a_type, input_b_type, fn):
		self.name = name
		self.input_a_type = input_a_type
		self.input_b_type = input_b_type
		self.fn = fn
	
	def eval(self, input_a, input_b, reg_c, registers):
		if self.input_a_type == R:
			input_a = registers[input_a]
		if self.input_b_type == R:
			input_b = registers[input_b]
		registers[reg_c] = self.fn(input_a, input_b)

OPCODES = [
	# Addition
	Opcode("addr", R, R, lambda a, b: a + b),
	Opcode("addi", R, I, lambda a, b: a + b),	

	# Multiplication
	Opcode("mulr", R, R, lambda a, b: a * b),
	Opcode("muli", R, I, lambda a, b: a * b),	

	# Bitwise AND
	Opcode("banr", R, R, lambda a, b: a & b),
	Opcode("bani", R, I, lambda a, b: a & b),	

	# Bitwise OR
	Opcode("borr", R, R, lambda a, b: a | b),
	Opcode("bori", R, I, lambda a, b: a | b),	

	# Assignment
	Opcode("setr", R, _, lambda a, b: a),
	Opcode("seti", I, _, lambda a, b: a),	

	# Greater than testing
	Opcode("gtir", I, R, lambda a, b: 1 if a > b else 0),
	Opcode("gtri", R, I, lambda a, b: 1 if a > b else 0),
	Opcode("gtrr", R, R, lambda a, b: 1 if a > b else 0),

	# Greater than testing
	Opcode("eqir", I, R, lambda a, b: 1 if a == b else 0),
	Opcode("eqri", R, I, lambda a, b: 1 if a == b else 0),
	Opcode("eqrr", R, R, lambda a, b: 1 if a == b else 0),
]

class Sample:
	def __init__(self, input, op, output):
		self.input = input
		self.op = op
		self.output = output

SAMPLES = []

_INPUT_RE = re.compile(r"Before: \[(\d+), (\d+), (\d+), (\d+)\]")
_OP_RE = re.compile(r"(\d+) (\d+) (\d+) (\d+)")
_OUTPUT_RE = re.compile(r"After:  \[(\d+), (\d+), (\d+), (\d+)\]")

with open("input.txt") as f:
	lines = f.readlines()
	for sample_lines in [lines[i:i+4] for i in range(0, len(lines), 4)]:
		input_line, op_line, output_line, ignored_line = sample_lines
		if input_line == "\n":
			# Skip test data
			break
		input = map(int, _INPUT_RE.match(input_line).groups())
		op = map(int, _OP_RE.match(op_line).groups())
		output = map(int, _OUTPUT_RE.match(output_line).groups())
		SAMPLES.append(Sample(list(input), list(op), list(output)))

result = 0
for sample in SAMPLES:
	matching_opcodes_count = 0
	for opcode in OPCODES:
		registers = list(sample.input)
		opcode.eval(*sample.op[1:], registers)
		if registers == sample.output:
			matching_opcodes_count += 1
			if matching_opcodes_count >= 3:
				break
	if matching_opcodes_count >= 3:
		result += 1

print(result)
		

