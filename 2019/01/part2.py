#!/usr/local/bin/python3

total_fuel = 0
with open("input.txt") as f:
    for line in f.readlines():
        module_fuel = int(int(line) / 3) - 2
        total_fuel += module_fuel
        while True:
            module_fuel = int(module_fuel / 3) - 2
            if module_fuel > 0:
                total_fuel += module_fuel
            else:
                break

print(total_fuel)
