#!/usr/local/bin/python3

import functools
import itertools
import math
import re

class Moon:
    def __init__(self, x, y, z):
        self.start_x = self.x = x
        self.start_y = self.y = y
        self.start_z = self.z = z
        self.vx = 0
        self.vy = 0
        self.vz = 0

    def apply_velocity(self):
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz

    def potential_energy(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    def kinetic_energy(self):
        return abs(self.vx) + abs(self.vy) + abs(self.vz)

MOON_LINE_RE = re.compile(r"<x=(-?[0-9]+), y=(-?[0-9]+), z=(-?[0-9]+)>")
moons = []

with open("input.txt") as f:
    for moon_line in f.readlines():
        x, y, z = map(int, MOON_LINE_RE.match(moon_line).groups())
        moons.append(Moon(x=x, y=y, z=z))

step = 1
has_x_period = False
x_period = 0
has_y_period = False
y_period = 0
has_z_period = False
z_period = 0

while True:
    # Apply Gravity
    for m1, m2 in itertools.combinations(moons, 2):
        if m1.x > m2.x:
            m1.vx -= 1
            m2.vx += 1
        elif m1.x < m2.x:
            m1.vx += 1
            m2.vx -= 1
        if m1.y > m2.y:
            m1.vy -= 1
            m2.vy += 1
        elif m1.y < m2.y:
            m1.vy += 1
            m2.vy -= 1
        if m1.z > m2.z:
            m1.vz -= 1
            m2.vz += 1
        elif m1.z < m2.z:
            m1.vz += 1
            m2.vz -= 1

    # Apply Velocity
    for m in moons:
        m.apply_velocity()

    if not has_x_period:
        x_period += 1
        has_x_period = all([m.x == m.start_x and m.vx == 0 for m in moons])
    if not has_y_period:
        y_period += 1
        has_y_period = all([m.y == m.start_y and m.vy == 0 for m in moons])
    if not has_z_period:
        z_period += 1
        has_z_period = all([m.z == m.start_z and m.vz == 0 for m in moons])

    step += 1
    if has_x_period and has_y_period and has_z_period:
        print("got the periods of all the moons after %d steps" % step)
        break
    if step % 100000 == 0:
        print("Step %d" % step)

def lcm(numbers):
    return functools.reduce(lambda x, y: (x*y) // math.gcd(x, y), numbers, 1)

print("LCM of periods: %d" % lcm([x_period, y_period, z_period]))
