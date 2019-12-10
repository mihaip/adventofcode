#!/usr/local/bin/python3

import math

asteroids = []

with open("input.txt") as f:
    for y, line in enumerate(f):
        line = line.strip()
        for x, c in enumerate(line):
            if c == '#':
                asteroids.append((x, y))

print("%d asteroids" % len(asteroids))

def count_visible_asteroids(station_x, station_y):
    unique_directions = set()
    for asteroid_x, asteroid_y in asteroids:
        if asteroid_x == station_x and asteroid_y == station_y:
            continue
        delta_x = asteroid_x - station_x
        delta_y = asteroid_y - station_y
        if delta_x == 0:
            direction = "up" if delta_y < 0 else "down"
        elif delta_y == 0:
            direction = "left" if delta_x < 0 else "right"
        else:
            gcd = math.gcd(abs(delta_x), abs(delta_y))
            direction = f"{delta_y / gcd}#{delta_x / gcd}"
        unique_directions.add(direction)
    return len(unique_directions)

best = None
best_location = None

for asteroid_x, asteroid_y in asteroids:
    current = count_visible_asteroids(asteroid_x, asteroid_y)
    if best is None or current > best:
        best = current
        best_location = (asteroid_x, asteroid_y)

best_x, best_y = best_location
print("best is at %d,%d with %d visible" % (best_x, best_y, best))
