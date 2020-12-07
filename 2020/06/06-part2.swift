#!/usr/bin/env swift

import Foundation

fileprivate class Group {
    var peopleCount = 0
    private var answers = Dictionary<String, Int>()

    func addAnswer(_ answer: String) {
        if let count = answers[answer] {
            answers[answer] = count + 1
        } else {
            answers[answer] = 1
        }
    }

    func answerCount() -> Int {
        return answers.values.filter { $0 == peopleCount}.count
    }

}

fileprivate func main() {
    let inputStr = try! String(contentsOf: URL(fileURLWithPath: "./input.txt"))

    var currentGroup: Group? = nil
    var sum = 0
    for line in inputStr.components(separatedBy: .newlines) {
        if line.isEmpty {
            if let group = currentGroup {
                sum += group.answerCount()
            }
            currentGroup = nil
            continue
        }
        if currentGroup == nil {
            currentGroup = Group()
        }
        currentGroup!.peopleCount += 1
        for answer in line.map(String.init) {
            currentGroup!.addAnswer(answer)
        }
    }

    print("answer", sum)
}

main()
