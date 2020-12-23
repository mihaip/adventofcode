#!/usr/bin/env swift

import Foundation

fileprivate class Cup {
    let value: Int

    init(_ value: Int) {
        self.value = value
    }

    // Needs to be optional because we can't initialize them
    private var next_: Cup?

    // Use getters and setters to not make callers worry about optionals
    var next: Cup {
        get {
            return next_!
        }
        set(next) {
            next_ = next
        }
    }
}

fileprivate func main() {
    let inputStr = try! String(contentsOf: URL(fileURLWithPath: "./input.txt"))

    let lines = inputStr.components(separatedBy: .newlines)

    var firstCup: Cup?
    var previousCup: Cup?
    for value in lines[0].map(String.init).compactMap(Int.init) {
        let cup = Cup(value)
        if let previousCup = previousCup {
            previousCup.next = cup
        } else {
            firstCup = cup
        }
        previousCup = cup
    }

    previousCup!.next = firstCup!

    var current = firstCup!

    for _ in 0..<100 {
        let c1 = current.next
        let c2 = c1.next
        let c3 = c2.next

        current.next = c3.next

        var destinationValue = current.value - 1
        var destination: Cup?
        while true {
            var minValue = current.value
            var maxValue = current.value
            var maxCup = current
            var d = current
            repeat {
                if d.value == destinationValue {
                    destination = d
                }
                if d.value < minValue {
                    minValue = d.value
                }
                if d.value > maxValue {
                    maxValue = d.value
                    maxCup = d
                }
                d = d.next
            } while d !== current
            if destination != nil {
                break
            }
            destinationValue -= 1
            if destinationValue < minValue {
                destination = maxCup
                break
            }
        }

        c3.next = destination!.next
        destination!.next = c1

        current = current.next
    }

    var oneCup = current
    while oneCup.value != 1 {
        oneCup = oneCup.next
    }

    var answer: [Int] = []
    var c = oneCup.next
    repeat {
        answer.append(c.value)
        c = c.next
    } while c !== oneCup

    print("answer", answer.map(String.init).joined())
}

main()
