#!/usr/bin/env swift

import Foundation

fileprivate struct Rule {
    let field: String
    let min1: Int
    let max1: Int
    let min2: Int
    let max2: Int
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
        return rules.contains(where: { (f >= $0.min1 && f <= $0.max1) || (f >= $0.min2 && f <= $0.max2) })
    }

    var errorRate = 0
    for ticket in nearbyTickets {
        for field in ticket {
            if !validField(field) {
                errorRate += field
            }
        }
    }

    print("anwer", errorRate)
}

main()
