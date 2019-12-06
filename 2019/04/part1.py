#!/usr/local/bin/python3

min = 347312
max = 805915
count = 0

for combination in range(min, max + 1):
    digits = [int(d) for d in str(combination)]
    has_double = False
    increasing = True
    for i in range(5):
        if digits[i] == digits[i + 1]:
            has_double = True
        elif digits[i] > digits[i + 1]:
            increasing = False
            break
    if not has_double or not increasing:
        continue
    count += 1

print(count)


