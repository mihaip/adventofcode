#!/usr/local/bin/python3

with open("input.txt") as f:
    input = f.read().strip()

def should_reduce(a, b):
    return a.lower() == b.lower() and a != b

def reduce(input):
    while True:
        output = ""
        i = 0
        while i < len(input):
            cur = input[i]
            if i == len(input) - 1:
                output += cur
                break
            next = input[i + 1]
            if should_reduce(cur, next):
                i += 2
            else:
                output += cur
                i += 1
        if output == input:
            break
        input = output
    return output

print(len(reduce(input)))
