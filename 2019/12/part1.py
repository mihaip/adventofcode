#!/usr/local/bin/python3

import itertools
import re

class Moon:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.vx = 0
        self.vy = 0
        self.vz = 0

    def apply_velocity(self):
        m.x += m.vx
        m.y += m.vy
        m.z += m.vz

    def potential_energy(self):
        return abs(m.x) + abs(m.y) + abs(m.z)

    def kinetic_energy(self):
        return abs(m.vx) + abs(m.vy) + abs(m.vz)

MOON_LINE_RE = re.compile(r"<x=(-?[0-9]+), y=(-?[0-9]+), z=(-?[0-9]+)>")
moons = []

with open("input.txt") as f:
    for moon_line in f.readlines():
        x, y, z = map(int, MOON_LINE_RE.match(moon_line).groups())
        moons.append(Moon(x, y, z))

for step in range(1, 1001):
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
    print("Step %d" % step)
    total_energy = 0
    for m in moons:
        m.apply_velocity()
        total_energy += m.potential_energy() * m.kinetic_energy()
        print("pos=%d,%d,%d vel=%d,%d,%d" % (m.x, m.y, m.z, m.vx, m.vy, m.vz))
    print("total_energy=%d" % total_energy)


