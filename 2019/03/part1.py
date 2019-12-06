#!/usr/local/bin/python3

import sys

with open("input.txt") as f:
    wire1 = f.readline().split(",")
    wire2 = f.readline().split(",")

wire_1_path = set()
x = 0
y = 0
position = None
def walk_segment(segment):
    global x
    global y
    direction = segment[0]
    distance = int(segment[1:])
    for i in range(distance):
        if direction == "R":
            x += 1
        elif direction == "L":
            x -= 1
        elif direction == "D":
            y += 1
        elif direction == "U":
            y -= 1
        yield x, y, "%d-%d" % (x, y)


for segment in wire1:
    for _, _, position in walk_segment(segment):
        wire_1_path.add(position)

x = 0
y = 0
best_distance = sys.maxsize
for segment in wire2:
    for x, y, position in walk_segment(segment):
        if position in wire_1_path:
            distance = abs(x) + abs(y)
            if distance < best_distance:
                best_distance = distance

print(best_distance)
