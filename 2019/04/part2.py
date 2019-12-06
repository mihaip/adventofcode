#!/usr/local/bin/python3

min = 347312
max = 805915
count = 0

for combination in range(min, max + 1):
    digits = [int(d) for d in str(combination)]
    increasing = True
    current_run_digit = None
    run_lengths = []
    for i in range(5):
        if digits[i] == digits[i + 1]:
            if digits[i] == current_run_digit:
                run_lengths[-1] += 1
            else:
                run_lengths.append(2)
                current_run_digit = digits[i]
        elif digits[i] > digits[i + 1]:
            increasing = False
            break
    has_double = 2 in run_lengths
    if not has_double or not increasing:
        continue
    count += 1

print(count)


