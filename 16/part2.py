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
		self.possible_encodings = set(range(16))
		self.encoding = None
	
	def eval(self, input_a, input_b, reg_c, registers):
		if self.input_a_type == R:
			input_a = registers[input_a]
		if self.input_b_type == R:
			input_b = registers[input_b]
		registers[reg_c] = self.fn(input_a, input_b)
	
	def use_sample(self, sample):
		encoding, input_a, input_b, reg_c = sample.op		
		if encoding not in self.possible_encodings:
			return
		registers = list(sample.input)
		self.eval(input_a, input_b, reg_c, registers)
		if registers != sample.output:
			self.possible_encodings.remove(sample.op[0])

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
TEST_DATA = []

_INPUT_RE = re.compile(r"Before: \[(\d+), (\d+), (\d+), (\d+)\]")
_OP_RE = re.compile(r"(\d+) (\d+) (\d+) (\d+)")
_OUTPUT_RE = re.compile(r"After:  \[(\d+), (\d+), (\d+), (\d+)\]")

with open("input.txt") as f:
	lines = f.readlines()
	test_data_start = None
	for i in range(0, len(lines), 4):
		input_line, op_line, output_line = lines[i:i+3]
		if input_line == "\n":
			test_data_start = i
			break
		input = map(int, _INPUT_RE.match(input_line).groups())
		op = map(int, _OP_RE.match(op_line).groups())
		output = map(int, _OUTPUT_RE.match(output_line).groups())
		SAMPLES.append(Sample(list(input), list(op), list(output)))
	
	for test_line in lines[test_data_start:]:
		if test_line == "\n":
			continue
		TEST_DATA.append(list(map(int, _OP_RE.match(test_line).groups())))

for sample in SAMPLES:
	for opcode in OPCODES:	
		opcode.use_sample(sample)

opcodes_by_encoding = {}
while len(opcodes_by_encoding) != 16:
	for opcode in OPCODES:
		if opcode.encoding is not None:
			continue
		if len(opcode.possible_encodings) == 1:
			opcode.encoding = list(opcode.possible_encodings)[0]
			opcodes_by_encoding[opcode.encoding] = opcode
		else:
			opcode.possible_encodings = {e for e in opcode.possible_encodings if e not in opcodes_by_encoding}

registers = [0, 0, 0, 0]

for encoding, input_a, input_b, reg_c in TEST_DATA:
	opcode = opcodes_by_encoding[encoding]
	opcode.eval(input_a, input_b, reg_c, registers)

print(registers[0])
		
