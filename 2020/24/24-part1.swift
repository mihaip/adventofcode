#!/usr/bin/env swift

import Foundation

fileprivate func main() {
    let inputStr = try! String(contentsOf: URL(fileURLWithPath: "./input.txt"))

    let lines = inputStr.components(separatedBy: .newlines)

    var flipped = Set<String>()
    for line in lines {
        if line.isEmpty {
            continue
        }
        var input = line
        var (x, y) = (0.0, 0.0)
        while !input.isEmpty {
            var (dX, dY) = (0.0, 0.0)
            if input.hasPrefix("e") {
                (dX, dY) = (1.0, 0.0)
                input = String(input.dropFirst(1))
            } else if input.hasPrefix("se") {
                (dX, dY) = (0.5, -0.5)
                input = String(input.dropFirst(2))
            } else if input.hasPrefix("sw") {
                (dX, dY) = (-0.5, -0.5)
                input = String(input.dropFirst(2))
            } else if input.hasPrefix("w") {
                (dX, dY) = (-1.0, 0)
                input = String(input.dropFirst(1))
            } else if input.hasPrefix("nw") {
                (dX, dY) = (-0.5, 0.5)
                input = String(input.dropFirst(2))
            } else if input.hasPrefix("ne") {
                (dX, dY) = (0.5, 0.5)
                input = String(input.dropFirst(2))
            } else {
                print("Unexpected input", input)
            }
            x += dX
            y += dY
        }

        let key = "\(x)-\(y)"
        if flipped.contains(key) {
            flipped.remove(key)
        } else {
            flipped.insert(key)
        }
    }

    print("answer", flipped.count)
}

main()
