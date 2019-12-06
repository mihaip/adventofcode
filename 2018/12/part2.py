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
previous_result = None
previous_delta = None
GENERATION_COUNT = 50000000000
for generation in range(GENERATION_COUNT):
	next_state = []
	state = ".." + state + ".."
	start_pot_offset -= 2
	state_length = len(state)
	for i in range(state_length):
		if i >= 2 and i < state_length - 2:
			pattern = state[i-2:i+3]
			assert len(pattern) == 5
		else:
			pattern = []
			for j in range(i-2, i+3):
				if j < 0 or j >= len(state):
					pattern.append(".")
				else:
					pattern.append(state[j])
			pattern = "".join(pattern)
		next_state.append(pattern_map.get(pattern, "."))
	state = "".join(next_state)
	if (generation + 1) % 20 == 0:
		result = 0
		for i, value in enumerate(state):
			if value == "#":
				result += i + start_pot_offset
		if previous_result is not None:
			delta = result - previous_result
			if delta == previous_delta:
				print(int(result + delta * ((GENERATION_COUNT - (generation + 1))/20)))
				break
			else:
				previous_delta = delta
		previous_result = result
