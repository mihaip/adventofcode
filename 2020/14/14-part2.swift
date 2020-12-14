#!/usr/bin/env swift

import Foundation

fileprivate func main() {
    let inputStr = try! String(contentsOf: URL(fileURLWithPath: "./input.txt"))
    let maskRegex = try! NSRegularExpression(pattern: #"mask = ([X01]+)"#, options: [])
    let memRegex = try! NSRegularExpression(pattern: #"mem\[(\d+)\] = (\d+)"#, options: [])

    var addressOrMask: UInt64 = 0
    var floatingBits: [UInt64] = []
    func generateAddresses(_ baseAddress: UInt64) -> [UInt64] {
        var results = [baseAddress | addressOrMask]
        for floatingBit in floatingBits {
            var bitResults: [UInt64] = []
            for r in results {
                let bitMask = UInt64(1) << floatingBit
                bitResults.append(r | bitMask)
                bitResults.append(r & ~bitMask)
            }
            results = bitResults
        }
        return results
    }

    var memory = Dictionary<UInt64, UInt64>()
    for line in inputStr.components(separatedBy: .newlines) {
        if line.isEmpty {
            continue
        }
        if let match = maskRegex.firstMatch(in: line, options: [], range: NSRange(location: 0, length: line.count)) {
            let maskStr = line[Range(match.range(at: 1), in: line)!].map(String.init)
            addressOrMask = 0
            floatingBits = []
            for (i, bit) in maskStr.enumerated() {
                let offset: UInt64 = 35 - UInt64(i)
                if bit == "1" {
                    addressOrMask |= 1 << offset
                } else if bit == "X" {
                    floatingBits.append(offset)
                }
            }
        } else if let match = memRegex.firstMatch(in: line, options: [], range: NSRange(location: 0, length: line.count)) {
            let writeAddress = UInt64(line[Range(match.range(at: 1), in: line)!])!
            let writeValue = UInt64(line[Range(match.range(at: 2), in: line)!])!

            for resultAddress in generateAddresses(writeAddress) {
                memory[resultAddress] = writeValue
            }
        }
    }

    var sum: UInt64 = 0
    for value in memory.values {
        sum += value
    }
    print("answer", sum)
}

main()
