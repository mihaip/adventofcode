#!/usr/local/bin/python3

import sys

with open("input.txt") as f:
    wire1 = f.readline().split(",")
    wire2 = f.readline().split(",")

wire_1_path = {}
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
        wire_1_path[position] = len(wire_1_path) + 1

x = 0
y = 0
best_distance = sys.maxsize
wire_2_steps = 0
for segment in wire2:
    for x, y, position in walk_segment(segment):
        wire_2_steps += 1
        if position in wire_1_path:
            wire_1_steps = wire_1_path[position]
            distance = wire_2_steps + wire_1_steps
            if distance < best_distance:
                best_distance = distance

print(best_distance)
