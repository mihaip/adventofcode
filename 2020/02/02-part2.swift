#!/usr/bin/env swift

import Foundation

fileprivate func main() {
    let regex = try! NSRegularExpression(pattern: #"(\d+)-(\d+) (.): (.+)"#, options: [])
    let inputStr = try! String(contentsOf: URL(fileURLWithPath: "./input.txt"))

    var validCount = 0
    for line in inputStr.components(separatedBy: .newlines) {
        if let match = regex.firstMatch(in: line, options: [], range: NSRange(location: 0, length: line.count)) {
            let offset1 = Int(line[Range(match.range(at: 1), in: line)!])! - 1
            let offset2 = Int(line[Range(match.range(at: 2), in: line)!])! - 1
            let letter = line[Range(match.range(at: 3), in: line)!].first!
            let password = line[Range(match.range(at: 4), in: line)!]

            let hasOffset1 = password[password.index(password.startIndex, offsetBy: offset1)] == letter
            let hasOffset2 = password[password.index(password.startIndex, offsetBy: offset2)] == letter

            if hasOffset1 != hasOffset2 {
                validCount += 1
            }
        }
    }

    print("answer", validCount)
}

main()
