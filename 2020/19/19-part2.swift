#!/usr/bin/env swift

import Foundation

fileprivate protocol Rule {
    func validate(_ message: String) -> [Int]
    func dump(_ depth: Int)
}

fileprivate struct LiteralRule: Rule {
    let literal: String

    func validate(_ message: String) -> [Int] {
        if message.hasPrefix(literal) {
            return [literal.count]
        }
        return []
    }

    func dump(_ depth: Int) {
        print(String(repeating: "  ", count: depth), "literal", literal)
    }
}

fileprivate struct OrRule: Rule {
    let left: Rule
    let right: Rule

    func validate(_ message: String) -> [Int] {
        return Array(Set(left.validate(message) + right.validate(message)))
    }

    func dump(_ depth: Int) {
        print(String(repeating: "  ", count: depth), "or")
        left.dump(depth + 1)
        right.dump(depth + 1)
    }
}

fileprivate struct CompoundRule: Rule {
    let rules: [Rule]

    func validate(_ message: String) -> [Int] {
        func helper(_ message: String, _ rules: [Rule]) -> [Int] {
            if rules.isEmpty {
                return [0]
            }
            var result: [Int] = []
            let rule = rules.first!
            for ruleConsumed in rule.validate(message) {
                let curMessage = String(message.dropFirst(ruleConsumed))
                for r in helper(curMessage, Array(rules.dropFirst())) {
                    result.append(ruleConsumed + r)
                }
            }
            return result
        }

        return helper(message, rules)
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

    let lines = inputStr
        .replacingOccurrences(of: "8: 42", with: "8: 42 | 42 8")
        .replacingOccurrences(of: "11: 42 31", with: "11: 42 31 | 42 11 31")
        .components(separatedBy: .newlines)
    var readingRules = true
    var rawRules = Dictionary<Int, String>()
    var parsedRules = Dictionary<Int, Rule>()
    var messages: [String] = []

    func parseRule(_ str: String) -> Rule {
        if str.hasPrefix("\"") {
            return LiteralRule(literal: String(str.dropFirst().dropLast()))
        }
        if str == "42 | 42 8" {
            let rule = parseRule("42")
            var repeatingRule = parseRule("42")
            // A hack, could instead have a special OneOrMoreRule
            for i in 2...20 {
                repeatingRule = OrRule(left: repeatingRule, right: CompoundRule(rules: Array(repeating: rule, count: i)))
            }
            return repeatingRule
        }
        if str == "42 31 | 42 11 31" {
            let head = parseRule("42")
            let tail = parseRule("31")
            var headTailRule: Rule = CompoundRule(rules: [head, tail])
            // A hack, could instead have a special HeadOrTailRule
            for i in 2...20 {
                headTailRule = OrRule(
                    left: headTailRule,
                    right: CompoundRule(
                        rules: Array(repeating: head, count: i) + Array(repeating: tail, count: i)))
            }
            return headTailRule
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
        if rootRule.validate(message).contains(message.count) {
            validMessageCount += 1
        }
    }

    print("answer", validMessageCount)

}

main()
