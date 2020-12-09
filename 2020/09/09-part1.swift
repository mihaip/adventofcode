#!/usr/bin/env swift

import Foundation

fileprivate func main() {
    let inputStr = try! String(contentsOf: URL(fileURLWithPath: "./input.txt"))
    let window = 25

    var numbers: [Int] = []
    for line in inputStr.components(separatedBy: .newlines) {
        if line.isEmpty {
            continue
        }

        let n = Int(line)!
        if numbers.count <= window {
            numbers.append(n)
            continue
        }

        var valid = false
        for (i, s1) in numbers.enumerated()  {
            let s2Target = n - s1
            for (j, s2) in numbers.enumerated() {
                if j != i && s2 == s2Target {
                    valid = true
                    break
                }
            }
            if valid {
                break
            }
        }
        if !valid {
            print("answer", n)
            break
        }

        numbers.append(n)
        numbers.remove(at: 0)
    }
}

main()
