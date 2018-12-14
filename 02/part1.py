#!/usr/local/bin/python3

import collections

two_count = 0
three_count = 0

with open("input.txt") as f:
    for id in f.readlines():
        counts = collections.defaultdict(int)
        for letter in id:
            counts[letter] += 1
        had_two = False
        had_three = False
        for count in counts.values():
            if count == 2:
                had_two = True
            elif count == 3:
                had_three = True
        if had_two:
            two_count += 1
        if had_three:
            three_count += 1

print(two_count * three_count)
