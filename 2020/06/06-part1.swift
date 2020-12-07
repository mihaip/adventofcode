#!/usr/bin/env swift

import Foundation

fileprivate class Group {
    var answers = Set<String>()
}

fileprivate func main() {
    let inputStr = try! String(contentsOf: URL(fileURLWithPath: "./input.txt"))

    var currentGroup: Group? = nil
    var sum = 0
    for line in inputStr.components(separatedBy: .newlines) {
        if line.isEmpty {
            if let group = currentGroup {
                sum += group.answers.count
            }
            currentGroup = nil
            continue
        }
        if currentGroup == nil {
            currentGroup = Group()
        }
        for answer in line.map(String.init) {
            currentGroup!.answers.insert(answer)
        }
    }

    print("answer", sum)
}

main()
