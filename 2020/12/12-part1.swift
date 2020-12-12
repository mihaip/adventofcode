#!/usr/bin/env swift

import Foundation

fileprivate func main() {
    let inputStr = try! String(contentsOf: URL(fileURLWithPath: "./input.txt"))

    var x = 0
    var y = 0
    let directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    var direction = 1
    for line in inputStr.components(separatedBy: .newlines) {
        if line.isEmpty {
            continue
        }
        let action = line.prefix(1)
        let value = Int(line.suffix(line.count - 1))!
        switch (action) {
        case "N":
            y += value
        case "S":
            y -= value
        case "E":
            x += value
        case "W":
            x -= value
        case "L":
            direction -= value / 90
        case "R":
            direction += value / 90
        case "F":
            let (dX, dY) = directions[((direction % 4) + 4) % 4]
            x += dX * value
            y += dY * value
        default:
            print("Unexpected action", action)
        }
    }
    print("answer", abs(x) + abs(y))
}

main()
