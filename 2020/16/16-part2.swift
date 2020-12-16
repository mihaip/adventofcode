#!/usr/bin/env swift

import Foundation

fileprivate struct Rule: Equatable {
    let field: String
    let min1: Int
    let max1: Int
    let min2: Int
    let max2: Int

    func isValid(_ f: Int) -> Bool {
        return (f >= min1 && f <= max1) || (f >= min2 && f <= max2)
    }

    static func == (lhs: Rule, rhs: Rule) -> Bool {
        return lhs.field == rhs.field
    }
}

fileprivate func main() {
    let inputStr = try! String(contentsOf: URL(fileURLWithPath: "./input.txt"))
    let regex = try! NSRegularExpression(pattern: #"(.+): (\d+)-(\d+) or (\d+)-(\d+)"#, options: [])

    let lines = inputStr.components(separatedBy: .newlines)
    var rules: [Rule] = []
    var yourTicket: [Int] = []
    var nearbyTickets: [[Int]] = []
    var mode = 0
    for line in lines {
        if line.isEmpty {
            mode += 1
            continue
        }
        if mode == 0 {
            if let match = regex.firstMatch(in: line, options: [], range: NSRange(location: 0, length: line.count)) {
                let field = String(line[Range(match.range(at: 1), in: line)!])
                let min1 = Int(line[Range(match.range(at: 2), in: line)!])!
                let max1 = Int(line[Range(match.range(at: 3), in: line)!])!
                let min2 = Int(line[Range(match.range(at: 4), in: line)!])!
                let max2 = Int(line[Range(match.range(at: 5), in: line)!])!

                rules.append(Rule(field: field, min1: min1, max1: max1, min2: min2, max2: max2))
            } else {
                print("did not match regex", line)
            }
        } else if mode == 1 {
            if line.hasSuffix(":") {
                continue
            }
            yourTicket = line.components(separatedBy: ",").compactMap(Int.init)
        } else if mode == 2 {
            if line.hasSuffix(":") {
                continue
            }
            nearbyTickets.append(line.components(separatedBy: ",").compactMap(Int.init))
        } else {
            print("unexpected mode", mode, line)
        }
    }

    func validField(_ f: Int) -> Bool {
        return rules.contains(where: { $0.isValid(f) })
    }

    let validTickets = nearbyTickets.filter({ $0.allSatisfy(validField) })
    let fieldCount = yourTicket.count

    var unknownRules = rules
    var unknownFields: [Int] = []
    for i in 0..<fieldCount {
        unknownFields.append(i)
    }

    var answer = 1
    while !unknownFields.isEmpty {
        for (i, f) in unknownFields.enumerated() {
            func isPossibleRule(rule: Rule) -> Bool {
                return validTickets.allSatisfy({ rule.isValid($0[f]) })
            }
            let possibleRules = unknownRules.filter(isPossibleRule)
            if (possibleRules.count == 1) {
                let rule = possibleRules[0]
                unknownFields.remove(at: i)
                unknownRules.remove(at: unknownRules.firstIndex(of: rule)!)
                if rule.field.hasPrefix("departure") {
                    answer *= yourTicket[f]
                }
                break
            } else if (possibleRules.count == 0) {
                print("?! no rules are possible for field", f)
            }
        }
    }

    print("answer", answer)
}

main()
