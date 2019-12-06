#!/usr/local/bin/python3

with open("input.txt") as f:
    program = [int(word) for word in f.readline().split(",")]

program[1] = 12
program[2] = 2

pc = 0
while True:
    opcode = program[pc]
    if opcode == 1:
        src_a, src_b, dst = program[pc + 1:pc + 4]
        program[dst] = program[src_a] + program[src_b]
    elif opcode == 2:
        src_a, src_b, dst = program[pc + 1:pc + 4]
        program[dst] = program[src_a] * program[src_b]
    elif opcode == 99:
        break
    else:
        raise Exception("Unexpected op code %d", opcode)
    pc += 4

print(program[0])
