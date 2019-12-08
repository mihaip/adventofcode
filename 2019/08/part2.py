#!/usr/local/bin/python3

import collections

with open("input.txt") as f:
    input = f.readline().strip()

width = 25
height = 6
layer_count = int(len(input) / width / height)
picture = [[2] * width for y in range(height)]

for layer in range(layer_count):
    digit_counts = collections.defaultdict(int)
    for y in range(height):
        for x in range(width):
            i = layer * width * height + y * width + x
            layer_pixel = int(input[i])
            picture_pixel = picture[y][x]
            if layer_pixel != 2 and picture_pixel == 2:
                picture[y][x] = layer_pixel

for y in range(height):
    print("".join([" " if p == 0 else "*" for p in picture[y]]))
