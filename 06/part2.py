#!/usr/local/bin/python3

import collections

class Point(collections.namedtuple("_Point", ["x", "y", "name"])):
    def distance_to(self, x, y):
        return abs(x - self.x) + abs(y - self.y)

points = []

with open("input.txt") as f:
    for line in f.readlines():
        [x, y] = map(int, line.strip().split(", "))
        name = chr(ord('A') + len(points))
        points.append(Point(x, y, name))

min_x = min(points, key=lambda p: p.x).x - 1
min_y = min(points, key=lambda p: p.y).y - 1
max_x = max(points, key=lambda p: p.x).x + 1
max_y = max(points, key=lambda p: p.y).y + 1

MAX_DISTANCE = 10000
region_size = 0
for x in range(min_x, max_x):
    for y in range(min_y, max_y):
        distance_sum = 0
        i = 0
        while distance_sum < MAX_DISTANCE:
            distance_sum += points[i].distance_to(x, y)
            i += 1
            if i == len(points):
                break
        if distance_sum < MAX_DISTANCE:
            region_size += 1

print(region_size)
