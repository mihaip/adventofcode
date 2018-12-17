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
width = max_x - min_x
height = max_y - min_y
print("x: %d to %d -> width of %d" % (min_x, max_x, width))
print("y: %d to %d -> height of %d" % (min_y, max_y, height))

point_counts = collections.defaultdict(int)
grid = []
edge_points = set()
for x in range(width):
    grid.append([None] * height)
def print_grid():
    for y in range(height):
        row = []
        for x in range(width):
            point = grid[x][y]
            if point and point not in edge_points:
                if point.x == x + min_x and point.y == y + min_y:
                    row.append(point.name)
                else:
                    row.append(point.name.lower())
            else:
                row.append(" ")
        print("".join(row))

for p in points:
    grid[p.x - min_x][p.y - min_y] = p

print_grid()
print("--------")

for x in range(min_x, max_x):
    for y in range(min_y, max_y):
        closest_point = min(points, key=lambda p:p.distance_to(x, y))
        second_closest_point = min([p for p in points if p != closest_point], key=lambda p:p.distance_to(x, y))
        if closest_point.distance_to(x, y) != second_closest_point.distance_to(x, y):
            point_counts[closest_point] += 1
            grid[x - min_x][y - min_y] = closest_point

print_grid()
print("--------")

for x in range(width):
    if grid[x][0]:
        edge_points.add(grid[x][0])
    if grid[x][-1]:
        edge_points.add(grid[x][-1])

for y in range(height):
    if grid[0][y]:
        edge_points.add(grid[0][y])
    if grid[-1][y]:
        edge_points.add(grid[-1][y])

print_grid()
print("--------")

for point in edge_points:
    del point_counts[point]

print(max(point_counts.values()))
