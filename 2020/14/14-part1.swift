#!/usr/bin/env swift

import Foundation

fileprivate func main() {
    let inputStr = try! String(contentsOf: URL(fileURLWithPath: "./input.txt"))
    let maskRegex = try! NSRegularExpression(pattern: #"mask = ([X01]+)"#, options: [])
    let memRegex = try! NSRegularExpression(pattern: #"mem\[(\d+)\] = (\d+)"#, options: [])

    var orMask: UInt64 = 0
    var andMask: UInt64 = 0b111111111111111111111111111111111111
    var memory = Dictionary<Int, UInt64>()
    for line in inputStr.components(separatedBy: .newlines) {
        if line.isEmpty {
            continue
        }
        if let match = maskRegex.firstMatch(in: line, options: [], range: NSRange(location: 0, length: line.count)) {
            let maskStr = line[Range(match.range(at: 1), in: line)!].map(String.init)
            orMask = 0
            andMask = 0b111111111111111111111111111111111111
            for (i, bit) in maskStr.enumerated() {
                let bitMask: UInt64 = 1 << (35 - UInt64(i))
                if bit == "1" {
                    orMask |= bitMask
                } else if bit == "0" {
                    andMask &= ~bitMask
                }
            }
        } else if let match = memRegex.firstMatch(in: line, options: [], range: NSRange(location: 0, length: line.count)) {
            let writeAddress = Int(line[Range(match.range(at: 1), in: line)!])!
            let writeValue = UInt64(line[Range(match.range(at: 2), in: line)!])!

            let resultValue = writeValue & andMask | orMask
            memory[writeAddress] = resultValue
        }
    }

    var sum: UInt64 = 0
    for value in memory.values {
        sum += value
    }
    print("answer", sum)
}

main()
