#!/usr/bin/env swift

import Foundation

fileprivate protocol Rule {
    func validate(_ message: String) -> Int?
    func dump(_ depth: Int)
}

fileprivate struct LiteralRule: Rule {
    let literal: String

    func validate(_ message: String) -> Int? {
        if message.hasPrefix(literal) {
            return literal.count
        }
        return nil
    }

    func dump(_ depth: Int) {
        print(String(repeating: "  ", count: depth), "literal", literal)
    }
}

fileprivate struct OrRule: Rule {
    let left: Rule
    let right: Rule

    func validate(_ message: String) -> Int? {
        if let leftResult = left.validate(message) {
            return leftResult
        }
        if let rightResult = right.validate(message) {
            return rightResult
        }
        return nil
    }

    func dump(_ depth: Int) {
        print(String(repeating: "  ", count: depth), "or")
        left.dump(depth + 1)
        right.dump(depth + 1)
    }
}

fileprivate struct CompoundRule: Rule {
    let rules: [Rule]

    func validate(_ message: String) -> Int? {
        var curMessage = message
        for rule in rules {
            if let ruleConsumed = rule.validate(curMessage) {
                curMessage = String(curMessage.dropFirst(ruleConsumed))
            } else {
                return nil
            }
        }
        return message.count - curMessage.count
    }

    func dump(_ depth: Int) {
        print(String(repeating: "  ", count: depth), "compound")
        for rule in rules {
            rule.dump(depth + 1)
        }
    }
}

fileprivate func main() {
    let inputStr = try! String(contentsOf: URL(fileURLWithPath: "./input.txt"))

    let lines = inputStr.components(separatedBy: .newlines)
    var readingRules = true
    var rawRules = Dictionary<Int, String>()
    var parsedRules = Dictionary<Int, Rule>()
    var messages: [String] = []

    func parseRule(_ str: String) -> Rule {
        if str.hasPrefix("\"") {
            return LiteralRule(literal: String(str.dropFirst().dropLast()))
        }
        if str.contains(" | ") {
            let pieces = str.components(separatedBy: " | ")
            return OrRule(left: parseRule(pieces[0]), right: parseRule(pieces[1]))
        }
        if str.contains(" ") {
            let pieces = str.components(separatedBy: " ")
            return CompoundRule(rules: pieces.map(parseRule))
        }
        let ruleIndex = Int(str)!
        if let parsedRule = parsedRules[ruleIndex] {
            return parsedRule
        }
        let parsedRule = parseRule(rawRules[ruleIndex]!)
        parsedRules[ruleIndex] = parsedRule
        return parsedRule
    }

    for line in lines {
        if line.isEmpty {
            readingRules = false
            continue
        }

        if (readingRules) {
            let rulePieces = line.components(separatedBy: ": ")
            let ruleIndex = Int(rulePieces[0])!
            rawRules[ruleIndex] = rulePieces[1]
        } else {
            messages.append(line)
        }
    }

    let rootRule = parseRule(rawRules[0]!)
    
    var validMessageCount = 0
    for message in messages {
        if let consumed = rootRule.validate(message) {
            if consumed == message.count {
                validMessageCount += 1
                continue
            }
        }
    }

    print("answer", validMessageCount)

}

main()
