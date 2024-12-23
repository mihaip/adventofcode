#!/usr/local/bin/python3

import sys

list1 = []
list2 = []

for line in sys.stdin.readlines():
    line = line.strip()
    [item1, item2] = line.split()
    item1 = int(item1)
    item2 = int(item2)
    list1.append(item1)
    list2.append(item2)

list1.sort()
list2.sort()

total = 0

for i in range(len(list1)):
    diff = abs(list1[i] - list2[i])
    total += diff

print(total)
