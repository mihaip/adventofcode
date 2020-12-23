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
    var cupsByValue = Dictionary<Int, Cup>()
    var minValue = Int.max
    var maxValue = Int.min

    func addCup(_ value: Int) {
        let cup = Cup(value)

        cupsByValue[value] = cup
        if value < minValue {
            minValue = value
        }
        if value > maxValue {
            maxValue = value
        }

        if let previousCup = previousCup {
            previousCup.next = cup
        } else {
            firstCup = cup
        }
        previousCup = cup
    }

    let initialValues = lines[0].map(String.init).compactMap(Int.init)
    initialValues.forEach(addCup)
    let baseCount = maxValue
    for i in 1...1000000 - initialValues.count {
        addCup(baseCount + i)
    }

    previousCup!.next = firstCup!

    var current = firstCup!

    for i in 0..<10000000 {
        if i % 100000 == 0 {
            print("progress:", i / 100000)
        }
        let c1 = current.next
        let c2 = c1.next
        let c3 = c2.next

        current.next = c3.next

        var destinationValue = current.value - 1
        var destination: Cup?
        while true {
            if let d = cupsByValue[destinationValue] {
                if d !== c1 && d !== c2 && d !== c3 {
                    destination = d
                    break
                }
            }

            destinationValue -= 1
            if destinationValue < minValue {
                destinationValue = maxValue
            }
        }

        c3.next = destination!.next
        destination!.next = c1

        current = current.next
    }

    let oneCup = cupsByValue[1]!
    print("answer", oneCup.next.value * oneCup.next.next.value)
}

main()
