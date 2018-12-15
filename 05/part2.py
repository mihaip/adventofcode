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

best_output_length = None
for i in range(26):
    filtered_input = input.replace(chr(ord('a') + i), "").replace(chr(ord('A') + i), "")
    output_length = len(reduce(filtered_input))
    if best_output_length is None or output_length < best_output_length:
        best_output_length = output_length

print(best_output_length)
