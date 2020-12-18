#!/usr/bin/env swift

import Foundation

fileprivate protocol Node {
    func value() -> Int
    func dump(_ depth: Int)
}

fileprivate struct NumNode: Node {
    let num: Int

    func value() -> Int {
        return num
    }

    func dump(_ depth: Int) {
        print(String(repeating: "  ", count: depth), num)
    }
}

fileprivate struct OpNode: Node {
    let op: String
    let left: Node
    let right: Node

    func value() -> Int {
        if op == "+" {
            return left.value() + right.value()
        }
        if op == "*" {
            return left.value() * right.value()
        }
        print("unexpected op", op)
        return 0
    }

    func dump(_ depth: Int) {
        print(String(repeating: "  ", count: depth), op)
        left.dump(depth + 1)
        right.dump(depth + 1)
    }


}

fileprivate func main() {
    let inputStr = try! String(contentsOf: URL(fileURLWithPath: "./input.txt"))

    func isNum(_ c: String) -> Bool {
        return c >= "0" && c <= "9"
    }

    func parse(_ expr: [String]) -> Node {
        var node: Node
        var i = 0
        if isNum(expr[i]) {
            var curNumChars: [String] = [expr[i]]
            i += 1
            while i < expr.count {
                if isNum(expr[i]) {
                    i += 1
                    curNumChars.append(expr[i])
                } else {
                    break
                }
            }
            node = NumNode(num: Int(curNumChars.reversed().joined())!)
        } else if expr[i] == ")" {
            i += 1
            func findParenEnd() -> Int {
                var openParenCount = 0
                for j in i..<expr.count {
                    let c = expr[j]
                    if c == ")" {
                        openParenCount += 1
                    } else if c == "(" {
                        if openParenCount == 0 {
                            return j
                        }
                        openParenCount -= 1
                    }
                }
                print("Could not find closing parentheses in", expr, "starting at", i)
                return -1
            }
            let parenEnd = findParenEnd()
            node = parse(Array(expr[i..<parenEnd]))
            i = parenEnd + 1
        } else {
            fatalError("Unexpected leading character in " + expr.joined())
        }

        if i == expr.count {
            return node
        }
        let op = expr[i]
        i += 1
        if op == "+" || op == "*" {
            return OpNode(op: op, left: node, right: parse(Array(expr[i...])))
        } else {
            fatalError("Unexpected op " + op)
        }
    }

    var answer = 0
    let lines = inputStr.components(separatedBy: .newlines)
    for line in lines {
        if line.isEmpty {
            continue
        }
        let root = parse(line.replacingOccurrences(of: " ", with: "").map(String.init).reversed())
        answer += root.value()
    }
    print("answer", answer)
}

main()
