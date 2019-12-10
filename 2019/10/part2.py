#!/usr/local/bin/python3

import collections
import math

asteroids = []

with open("input.txt") as f:
    for y, line in enumerate(f):
        line = line.strip()
        for x, c in enumerate(line):
            if c == '#':
                asteroids.append((x, y))

print("%d asteroids" % len(asteroids))

def find_nth_asteroid(station_x, station_y, n):
    direction_to_asteroids = collections.defaultdict(list)
    i = 0
    for asteroid_x, asteroid_y in asteroids:
        if asteroid_x == station_x and asteroid_y == station_y:
            continue
        delta_x = asteroid_x - station_x
        delta_y = asteroid_y - station_y
        # Polar coordinates
        r = math.sqrt(delta_x**2 + delta_y**2)
        # I don't like radians
        phi = math.atan2(delta_y, delta_x) / (2 * math.pi) * 360
        phi -= 90
        if phi < -180:
            phi += 360
        direction_to_asteroids[phi].append([r, asteroid_x, asteroid_y])

    directions = sorted(direction_to_asteroids.keys())
    for direction in directions:
        i += 1
        direction_asteroids = sorted(direction_to_asteroids[direction])
        r, asteroid_x, asteroid_y = direction_asteroids[0]
        print("i=%d asteroid=%d,%d (%d, %d) r=%g phi=%g" % (i, asteroid_x, asteroid_y, asteroid_x - station_x, asteroid_y - station_y, r, direction))
        if i == n:
            return asteroid_x, asteroid_y
        # In theory we should remove the asteroid from the list, but we only
        # have to do one sweep
    return None, None

x, y = find_nth_asteroid(20, 18, 200)
print("%d,%d = %d" % (x, y, x * 100 + y))
