#!/usr/local/bin/python3

with open("input.txt") as f:
    input = [int(word) for word in f.readline().split(",")]

target_output = 19690720
for noun in range(0, 100):
    for verb in range(0, 100):
        program = input.copy()
        program[1] = noun
        program[2] = verb

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

        if program[0] == target_output:
            print("noun: %d, verb: %d, solution: %d" % (noun, verb, noun * 100 + verb))
