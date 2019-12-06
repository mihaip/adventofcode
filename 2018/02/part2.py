#!/usr/local/bin/python3

import collections

variants = collections.defaultdict(set)

with open("input.txt") as f:
    for id in f.readlines():
        id = id.strip()
        for i in range(len(id)):
            variant = id[:i] + "*" + id[i + 1:]
            variants[variant].add(id)

for variant, ids in variants.items():
    if len(ids) == 2:
        print(variant.replace("*", ""))
