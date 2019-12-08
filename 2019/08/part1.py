#!/usr/local/bin/python3

import collections

with open("input.txt") as f:
    input = f.readline().strip()

width = 25
height = 6
layer_count = int(len(input) / width / height)
min_0_count = None
answer = None

for layer in range(layer_count):
    digit_counts = collections.defaultdict(int)
    for y in range(height):
        for x in range(width):
            i = layer * width * height + y * width + x
            pixel = int(input[i])
            digit_counts[pixel] += 1
    if min_0_count is None or digit_counts[0] < min_0_count:
        min_0_count = digit_counts[0]
        answer = digit_counts[1] * digit_counts[2]

print("answer: %d" % answer)

