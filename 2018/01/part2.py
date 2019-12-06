#!/usr/local/bin/python3

with open("input.txt") as f:
    changes = [int(l) for l in f.readlines()]

saw_duplicate = False
seen_frequencies = set()
frequency = 0
while True:
    for change in changes:
        frequency += change
        if frequency in seen_frequencies:
            print(frequency)
            saw_duplicate = True
            break
        seen_frequencies.add(frequency)
    if saw_duplicate:
        break
