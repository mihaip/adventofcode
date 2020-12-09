#!/usr/bin/env swift

import Foundation

fileprivate func main() {
    let inputStr = try! String(contentsOf: URL(fileURLWithPath: "./input.txt"))
    let target = 23278925

    var numbers: [Int] = []
    for line in inputStr.components(separatedBy: .newlines) {
        if line.isEmpty {
            continue
        }

        let n = Int(line)!
        numbers.append(n)
    }

    for (i, s1) in numbers.enumerated() {
        var sum = s1
        var min = s1
        var max = s1
        for s2 in numbers[i + 1..<numbers.count] {
            sum += s2
            if s2 < min {
                min = s2
            }
            if s2 > max {
                max = s2
            }
            if sum == target {
                print("answer", min + max)
                break
            }
            if sum > target {
                break
            }
        }
    }
}

main()
