#!/usr/local/bin/python3

total_fuel = 0
with open("input.txt") as f:
    for line in f.readlines():
        total_fuel += int(int(line) / 3) - 2
print(total_fuel)
