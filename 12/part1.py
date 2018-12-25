#!/usr/local/bin/python3

import re

_INITIAL_STATE_RE = re.compile(r"initial state: ([#.]+)")

pattern_map = {}

with open("input.txt") as f:
	initial_state_line = f.readline().strip()
	state = _INITIAL_STATE_RE.match(initial_state_line).group(1)
	
	assert not f.readline().strip()
	for rule_line in f.readlines():
		[input_pattern, output] = rule_line.strip().split(" => ")
		pattern_map[input_pattern] = output

start_pot_offset = 0

for generation in range(20):
	next_state = ""
	state = ".." + state + ".."
	start_pot_offset -= 2
	for i in range(len(state)):
		pattern = ""
		for j in range(i-2, i+3):
			if j < 0 or j >= len(state):
				pattern += "."
			else:
				pattern += state[j]
		next_state += pattern_map.get(pattern, ".")
	state = next_state

result = 0
for i, value in enumerate(state):
	if value == "#":
		result += i + start_pot_offset
print(result)
