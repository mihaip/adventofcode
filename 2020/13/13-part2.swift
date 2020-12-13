#!/usr/bin/env swift

import Foundation

fileprivate func main() {
    let inputStr = try! String(contentsOf: URL(fileURLWithPath: "./input.txt"))

    let lines = inputStr.components(separatedBy: .newlines)
    let buses = lines[1].components(separatedBy: ",").map(Int.init)

    var numbers: [Int] = []
    var remainders : [Int] = []
    for (i, bus) in buses.enumerated() {
        if let bus = bus {
            numbers.append(bus)
            remainders.append(bus - i % bus)
        }
    }

    let base = numbers.remove(at: 0)
    remainders.remove(at: 0)
    var result = 0
    var inc = base

    for (number, remainder) in zip(numbers, remainders) {
        while true {
            if (result % number == remainder) {
                inc *= number
                break
            } else {
                result += inc
            }
        }
    }

    print("answer", result)
}

main()
