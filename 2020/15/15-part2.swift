#!/usr/bin/env swift

import Foundation

fileprivate func main() {
    let inputStr = try! String(contentsOf: URL(fileURLWithPath: "./input.txt"))

    let lines = inputStr.components(separatedBy: .newlines)
    let numbers = lines[0].components(separatedBy: ",").compactMap(Int.init)

    var spokenNumbers: [Int] = []
    var numberIndices = Dictionary<Int, [Int]>()
    for n in numbers {
        spokenNumbers.append(n)
        numberIndices[n] = [spokenNumbers.count]
    }

    var turn = numbers.count
    while (true) {
        let lastNumber = spokenNumbers.last!
        let lastNumberIndices = numberIndices[lastNumber]!
        var newNumber: Int
        if lastNumberIndices.count == 1 {
            newNumber = 0
        } else {
            newNumber = lastNumberIndices[1] - lastNumberIndices[0]
        }
        spokenNumbers.append(newNumber)
        if let newNumberIndices = numberIndices[newNumber] {
            numberIndices[newNumber] = [newNumberIndices.last!, spokenNumbers.count]
        } else {
            numberIndices[newNumber] = [spokenNumbers.count]
        }
        turn += 1
        if (turn == 30000000) {
            break
        }
        if turn % 300000 == 0 {
            print("turn", turn)
        }
    }
    print("answer", spokenNumbers.last!)
}

main()
