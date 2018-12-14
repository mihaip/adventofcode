#!/usr/local/bin/python3

frequency = 0
with open("input.txt") as f:
    for line in f.readlines():
        frequency += int(line)
print(frequency)
