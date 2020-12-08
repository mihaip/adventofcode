#!/usr/bin/env swift

import Foundation

fileprivate struct Instruction {
    let op: String
    let arg: Int
}

fileprivate class VM {
    var accumulator = 0
    var pc = 0
    let instructions: [Instruction]

    init(instructions: [Instruction]) {
        self.instructions = instructions
    }

    func terminates() -> Bool {
        var seenPcs = Set<Int>()
        while (true) {
            seenPcs.insert(pc)
            step()
            if (pc == instructions.count) {
                return true
            }
            if (pc > instructions.count) {
                return false
            }
            if (seenPcs.contains(pc)) {
                return false
            }
        }
    }

    func step() {
        let instruction = instructions[pc]
        switch (instruction.op) {
        case "acc":
            accumulator += instruction.arg
            pc += 1
            break
        case "jmp":
            pc += instruction.arg
            break
        case "nop":
            pc += 1
            break
        default:
            print("Unhandled instruction op", instruction.op)
            break
        }
    }
}

fileprivate func main() {
    let inputStr = try! String(contentsOf: URL(fileURLWithPath: "./input.txt"))
    let regex = try! NSRegularExpression(pattern: #"(.+) (-|\+)(\d+)"#, options: [])

    var instructions: [Instruction] = []
    var instructionsToFlip: [Int] = []
    for line in inputStr.components(separatedBy: .newlines) {
        if line.isEmpty {
            continue
        }
        let match = regex.firstMatch(in: line, options: [], range: NSRange(location: 0, length: line.count))!
        let op = String(line[Range(match.range(at: 1), in: line)!])
        let sign = String(line[Range(match.range(at: 2), in: line)!])
        var arg = Int(line[Range(match.range(at: 3), in: line)!])!
        if sign == "-" {
            arg *= -1
        }
        if op == "jmp" || op == "nop" {
            instructionsToFlip.append(instructions.count)
        }
        instructions.append(Instruction(op: op, arg: arg))
    }

    for flipIndex in instructionsToFlip {
        var flippedInstructions = instructions
        let flipInstruction = instructions[flipIndex]
        if flipInstruction.op == "jmp" {
            flippedInstructions[flipIndex] = Instruction(op: "nop", arg: flipInstruction.arg)
        } else {
            flippedInstructions[flipIndex] = Instruction(op: "jmp", arg: flipInstruction.arg)

        }
        let vm = VM(instructions: flippedInstructions)
        if (vm.terminates()) {
            print("answer", vm.accumulator)
        }
    }
}

main()
