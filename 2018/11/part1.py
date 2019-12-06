#!/usr/local/bin/python3

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

best_square = None
best_power = None

for x in range(1, 298):
	for y in range(1, 298):		
		sum = 0
		for i in range(0, 3):
			for j in range(0, 3):
				sum += power_levels[x + i - 1][y + j - 1]
		if best_power is None or sum > best_power:
			best_power = sum
			best_square = [x, y]

print("best square: %d, %d with power %d" % (best_square[0], best_square[1], best_power))
