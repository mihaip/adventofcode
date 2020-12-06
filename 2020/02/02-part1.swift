#!/usr/bin/env swift

import Foundation

fileprivate func main() {
    let regex = try! NSRegularExpression(pattern: #"(\d+)-(\d+) (.): (.+)"#, options: [])
    let inputStr = try! String(contentsOf: URL(fileURLWithPath: "./input.txt"))

    var validCount = 0
    for line in inputStr.components(separatedBy: .newlines) {
        if let match = regex.firstMatch(in: line, options: [], range: NSRange(location: 0, length: line.count)) {
            let minCount = Int(line[Range(match.range(at: 1), in: line)!])!
            let maxCount = Int(line[Range(match.range(at: 2), in: line)!])!
            let letter = line[Range(match.range(at: 3), in: line)!].first!
            let password = line[Range(match.range(at: 4), in: line)!]

            let letterCount = password.filter { $0 == letter }.count
            if letterCount >= minCount && letterCount <= maxCount {
                validCount += 1
            }
        }
    }

    print("answer", validCount)
}

main()
