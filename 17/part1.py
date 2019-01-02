#!/usr/local/bin/python3

import re

_LINE_RE = re.compile(r"(x|y)=(\d+), (x|y)=(\d+)\.\.(\d+)")
SAND = "."
CLAY = "#"
WATER = "~"

x_segments = []
y_segments = []

with open("input.txt") as f:
	for line in f.readlines():
		coord1, coord1_value, coord2, coord2_range_start, coord2_range_end = _LINE_RE.match(line).groups()
		coord1_value, coord2_range_start, coord2_range_end = map(int, [coord1_value, coord2_range_start, coord2_range_end])
		if coord1 == "x":
			x_segments.append([coord1_value, coord2_range_start, coord2_range_end])
		else:
			y_segments.append([coord1_value, coord2_range_start, coord2_range_end])	

min_x = None
max_x = None
def check_x(x):
	global min_x, max_x
	if min_x is None or x < min_x:
		min_x = x
	if max_x is None or x > max_x:
		max_x = x
		
min_y = None
max_y = None
def check_y(y):
	global min_y, max_y
	if min_y is None or y < min_y:
		min_y = y
	if max_y is None or y > max_y:
		max_y = y
		
check_x(500)
check_y(0)

for x, y_start, y_end in x_segments:
	check_x(x)
	check_y(y_start)
	check_y(y_end)
	
for y, x_start, x_end in y_segments:
	check_y(y)
	check_x(x_start)
	check_x(x_end)

min_x -= 1
max_x += 1

width = max_x - min_x + 1
height = max_y - min_y + 1

board = []
for y in range(height):
	board.append([SAND] * width)
def print_board():
	header = "  "
	for x in range(width):
		header += "%d" % (x % 10)
	print(header)
	for y, row in enumerate(board):
		print("%d %s" % (y % 10, "".join(row)))

for x, y_start, y_end in x_segments:
	for y in range(y_start, y_end + 1):
		board[y - min_y][x - min_x] = CLAY
		
for y, x_start, x_end in y_segments:
	for x in range(x_start, x_end + 1):
		board[y - min_y][x - min_x] = CLAY

print_board()

water_sources = [(500 - min_x, 0)]

#while water_sources:
for i in range(32):
	print("%d water sources" % len(water_sources))
	new_water_sources = []
	for source_x, source_y in water_sources:
		reached_bottom = False
		drop_x, drop_y = [source_x, source_y]
		while board[drop_y][drop_x] == SAND:
			drop_y += 1
			if drop_y == height:
				reached_bottom = True
				break
		if reached_bottom:
			continue
		drop_y -= 1
		left_wall = drop_x
		right_wall = drop_x
		has_left_wall = None
		while True:
			if left_wall == 0 or board[drop_y + 1][left_wall] == SAND:
				has_left_wall = False
				break
			if board[drop_y][left_wall] == SAND:
				left_wall -= 1
				continue
			has_left_wall = True
			break
		has_right_wall = None
		while True:
			if right_wall == width - 1 or board[drop_y + 1][right_wall] == SAND:
				has_right_wall = False
				break
			if board[drop_y][right_wall] == SAND:
				right_wall += 1
				continue
			has_right_wall = True
			break
		if has_left_wall and has_right_wall:
			board[drop_y][left_wall + 1] = WATER
			new_water_sources.append([source_x, source_y])
			print("both walls")
		elif has_left_wall:
			# source moves to overflow on the right
			new_source_x = drop_x
			while board[drop_y + 1][new_source_x] != SAND:
				new_source_x += 1
			new_water_sources.append([new_source_x, drop_y])
			print("right overflow")
		elif has_right_wall:
			# source moves to overflow on the left
			print("left overflow")
		else:
			# sources on both the left and the right
			print("both overflow")
	water_sources = new_water_sources
	
print_board()
