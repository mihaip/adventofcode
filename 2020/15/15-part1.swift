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
            newNumber = lastNumberIndices[lastNumberIndices.count - 1] - lastNumberIndices[lastNumberIndices.count - 2]
        }
        spokenNumbers.append(newNumber)
        if var newNumberIndices = numberIndices[newNumber] {
            newNumberIndices.append(spokenNumbers.count)
            numberIndices[newNumber] = newNumberIndices
        } else {
            numberIndices[newNumber] = [spokenNumbers.count]
        }
        turn += 1
        if (turn == 2020) {
            break
        }
    }
    print("answer", spokenNumbers.last!)
}

main()
