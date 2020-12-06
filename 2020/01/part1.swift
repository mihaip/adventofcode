#!/usr/bin/env swift

import Foundation

fileprivate func main() {
    let inputStr = try! String(contentsOf: URL(fileURLWithPath: "./input.txt"))

    var entrySet = Set<Int>()
    for inputLine in inputStr.components(separatedBy: .newlines) {
        if inputLine.isEmpty {
            continue
        }
        let entry = Int(inputLine)!
        entrySet.insert(entry)
    }

    let TARGET = 2020
    for entry in entrySet {
        let otherEntry = TARGET - entry
        if otherEntry >= 0 && entrySet.contains(otherEntry) {
            print("answer", otherEntry * entry)
            break
        }
    }
}

main()
