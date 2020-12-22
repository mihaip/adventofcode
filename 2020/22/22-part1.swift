#!/usr/bin/env swift

import Foundation

fileprivate func main() {
    let inputStr = try! String(contentsOf: URL(fileURLWithPath: "./input.txt"))

    let lines = inputStr.components(separatedBy: .newlines)
    var p1: [Int] = []
    var p2: [Int] = []
    var readingP1 = true
    for line in lines {
        if line.isEmpty {
            readingP1 = false
            continue
        }
        if line.hasPrefix("Player") {
            continue
        }
        let card = Int(line)!
        if readingP1 {
            p1.append(card)
        } else {
            p2.append(card)
        }
    }

    while !p1.isEmpty && !p2.isEmpty {
        let card1 = p1.removeFirst()
        let card2 = p2.removeFirst()

        if card1 > card2 {
            p1.append(card1)
            p1.append(card2)
        } else {
            p2.append(card2)
            p2.append(card1)
        }
    }

    let winner = p1.isEmpty ? p2 : p1
    var score = 0
    for (i, card) in winner.reversed().enumerated() {
        score += card * (i + 1)
    }

    print("answer", score)
}

main()
