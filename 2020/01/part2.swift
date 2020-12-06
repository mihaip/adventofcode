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

    func findEntrySet(_ target: Int, _ targetEntryCount: Int) -> [Int]? {
        if targetEntryCount == 1 {
            return entrySet.contains(target) ? [target] : nil
        }
        for entry in entrySet {
            let remainingTarget = target - entry
            if remainingTarget <= 0 {
                continue
            }
            if let otherEntryResult = findEntrySet(remainingTarget, targetEntryCount - 1) {
                return [entry] + otherEntryResult
            }
        }
        return nil
    }

    if let answer = findEntrySet(2020, 3) {
        print("answer", answer[0] * answer[1] * answer[2])
    } else {
        print("no answer possible?!")
    }
}

main()
