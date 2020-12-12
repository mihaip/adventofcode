#!/usr/bin/env swift

import Foundation

fileprivate func main() {
    let inputStr = try! String(contentsOf: URL(fileURLWithPath: "./input.txt"))

    var x = 0
    var y = 0
    var waypointX = 10
    var waypointY = 1
    for line in inputStr.components(separatedBy: .newlines) {
        if line.isEmpty {
            continue
        }
        let action = line.prefix(1)
        let value = Int(line.suffix(line.count - 1))!
        switch (action) {
        case "N":
            waypointY += value
        case "S":
            waypointY -= value
        case "E":
            waypointX += value
        case "W":
            waypointX -= value
        case "L":
            for _ in 1...(value / 90) {
                (waypointX, waypointY) = (-waypointY, waypointX)
            }
        case "R":
            for _ in 1...(value / 90) {
                (waypointX, waypointY) = (waypointY, -waypointX)
            }
        case "F":
            x += waypointX * value
            y += waypointY * value
        default:
            print("Unexpected action", action)
        }
    }
    print("answer", abs(x) + abs(y))
}

main()
