#!/usr/bin/env swift

import Foundation

fileprivate class Game {
    var p1: [Int]
    var p2: [Int]
    var seenGames = Set<String>()

    init(_ p1: [Int], _ p2: [Int]) {
        self.p1 = p1
        self.p2 = p2
    }

    func play() -> (Int, [Int]) {
        while !p1.isEmpty && !p2.isEmpty {
            let key = p1.map(String.init).joined(separator: "-") + "|" + p1.map(String.init).joined(separator: "-")
            if seenGames.contains(key) {
                return (1, p1)
            }
            seenGames.insert(key)
            let card1 = p1.removeFirst()
            let card2 = p2.removeFirst()

            let winner: Int
            if card1 <= p1.count && card2 <= p2.count {
                let subGame = Game(Array(p1[0..<card1]), Array(p2[0..<card2]))
                (winner, _) = subGame.play()
            } else {
                winner = card1 > card2 ? 1 : 2;
            }

            if winner == 1 {
                p1.append(card1)
                p1.append(card2)
            } else {
                p2.append(card2)
                p2.append(card1)
            }
        }

        return p1.isEmpty ? (2, p2) : (1, p1)
    }
}

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

    let game = Game(p1, p2)
    let (winner, winnerCards) = game.play()

    var score = 0
    for (i, card) in winnerCards.reversed().enumerated() {
        score += card * (i + 1)
    }

    print("winner", winner)
    print("answer", score)
}

main()
