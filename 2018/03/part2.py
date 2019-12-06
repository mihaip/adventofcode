#!/usr/local/bin/python3

import re

SQUARE_RE = re.compile(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)")
FABRIC_SIZE = 1000
fabric = []
for i in range(FABRIC_SIZE):
    row = []
    for j in range(FABRIC_SIZE):
        row.append([])
    fabric.append(row)

def print_fabric():
    for row in fabric:
        print(" ".join(map(str, row)))

non_overlapping_claims = set()

with open("input.txt") as f:
    for line in f.readlines():
        id, left, top, width, height = map(int, SQUARE_RE.match(line).groups())
        had_overlap = False
        for x in range(left, left + width):
            for y in range(top, top + height):
                for overlap_id in fabric[y][x]:
                    if overlap_id in non_overlapping_claims:
                        non_overlapping_claims.remove(overlap_id)
                    had_overlap = True
                fabric[y][x].append(id)
        if not had_overlap:
            non_overlapping_claims.add(id)

print(non_overlapping_claims)
