#!/usr/bin/env swift

import Foundation

fileprivate func main() {
    let inputStr = try! String(contentsOf: URL(fileURLWithPath: "./input.txt"))

    var numbers: [Int] = []
    for line in inputStr.components(separatedBy: .newlines) {
        if line.isEmpty {
            continue
        }

        let n = Int(line)!
        numbers.append(n)
    }
    numbers.sort()

    numbers.insert(0, at: 0)
    numbers.append(numbers[numbers.count - 1] + 3)

    var diffs1 = 0
    var diffs3 = 0
    for (i, n) in numbers[1..<numbers.count].enumerated() {
        let diff = n - numbers[i]
        if diff == 0 {
            // ignore
        } else if diff == 1 {
            diffs1 += 1
        } else if diff == 2 {
            // ignore
        } else if diff == 3 {
            diffs3 += 1
        } else {
            print("unexpected diff", numbers[i], "->", n)
        }
    }

    print("answer", diffs1, diffs3, diffs1 * diffs3)

}

main()
