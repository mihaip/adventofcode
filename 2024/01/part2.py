#!/usr/local/bin/python3

import sys

list1 = []
list2 = dict()

for line in sys.stdin.readlines():
    line = line.strip()
    [item1, item2] = line.split()
    item1 = int(item1)
    item2 = int(item2)
    list1.append(item1)
    if item2 not in list2:
        list2[item2] = 1
    else:
        list2[item2] += 1

total = 0

for item1 in list1:
    count = list2.get(item1, 0)
    total += item1 * count

print(total)
