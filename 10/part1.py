#!/usr/local/bin/python3

import re

_LINE_RE = re.compile(r"position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>")

class Point:
	def __init__(self, x, y, dx, dy):
		self.x = x
		self.y = y
		self.dx = dx
		self.dy = dy
	
	def step(self):
		self.x += self.dx
		self.y += self.dy
	
	def unstep(self):
		self.x -= self.dx
		self.y -= self.dy
		
points = []

with open("input.txt") as f:
    for line in f.readlines():
        [x, y, dx, dy] = map(int, _LINE_RE.match(line).groups())
        point = Point(x, y, dx, dy)
        points.append(point)

min_x = min(points, key=lambda p:p.x).x
max_x = max(points, key=lambda p:p.x).x
min_y = min(points, key=lambda p:p.y).y
max_y = max(points, key=lambda p:p.y).y
previous_bounding_area = (max_x - min_x) * (max_y - min_y)

step_count = 0
while True:
	for p in points:
		p.step()
	min_x = min(points, key=lambda p:p.x).x
	max_x = max(points, key=lambda p:p.x).x
	min_y = min(points, key=lambda p:p.y).y
	max_y = max(points, key=lambda p:p.y).y		
	bounding_area = (max_x - min_x) * (max_y - min_y)
	if bounding_area > previous_bounding_area:
		break
	previous_bounding_area = bounding_area
	step_count += 1

for p in points:
	p.unstep()
	
min_x = min(points, key=lambda p:p.x).x
max_x = max(points, key=lambda p:p.x).x
min_y = min(points, key=lambda p:p.y).y
max_y = max(points, key=lambda p:p.y).y	
width = max_x - min_x + 1
height = max_y - min_y + 1
output = []
for y in range(height):
	output.append([" "] * width)
for p in points:
	output[p.y - min_y][p.x - min_x] = "*"
for row in output:
	print("".join(row))
