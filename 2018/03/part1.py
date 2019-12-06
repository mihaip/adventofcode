#!/usr/local/bin/python3

import re

SQUARE_RE = re.compile(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)")
FABRIC_SIZE = 1000
fabric = []
for i in range(FABRIC_SIZE):
    fabric.append([0] * FABRIC_SIZE)

def print_fabric():
    for row in fabric:
        print(" ".join(map(str, row)))

with open("input.txt") as f:
    for line in f.readlines():
        id, left, top, width, height = map(int, SQUARE_RE.match(line).groups())
        for x in range(left, left + width):
            for y in range(top, top + height):
                fabric[y][x] += 1

result = 0
for row in fabric:
    for sq in row:
        if sq >= 2:
            result += 1
print(result)

