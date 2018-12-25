#!/usr/local/bin/python3

import copy

input = 1133

def power_level(x, y):
	rack_id = x + 10
	power_level = rack_id * y
	power_level += input
	power_level *= rack_id
	power_level = int(power_level / 100) % 10
	power_level -= 5
	return power_level

power_levels = []
for x in range(1, 301):
	row = []
	for y in range(1, 301):
		row.append(power_level(x, y))
	power_levels.append(row)
power_levels_transposed = []
for y in range(1, 301):
	column = []
	for x in range(1, 301):
		column.append(power_level(x, y))
	power_levels_transposed.append(column)
	
current_power_levels = copy.deepcopy(power_levels)
best_square = None
best_power = None

for square_size in range(2, 301):
	new_power_levels = copy.deepcopy(current_power_levels)
	for x in range(0, 300 - square_size):
		for y in range(0, 300 - square_size):		
			s = current_power_levels[x][y]
			s += sum(power_levels[x + square_size - 1][y:y + square_size])
			s += sum(power_levels_transposed[y + square_size - 1][x:x + square_size - 1])
			new_power_levels[x][y] = s
			if best_power is None or s > best_power:
				best_power = s
				best_square = [x, y, square_size]
	current_power_levels = new_power_levels

[best_x, best_y, best_size] = best_square
print("best square: %d,%d,%d with power %d" % (best_x + 1, best_y + 1, best_size, best_power))
