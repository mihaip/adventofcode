#!/usr/bin/env swift

import Foundation

fileprivate func main() {
    let inputStr = try! String(contentsOf: URL(fileURLWithPath: "./input.txt"))

    var area = [[String]]()
    for line in inputStr.components(separatedBy: .newlines) {
        if line.isEmpty {
            continue
        }
        area.append(line.map(String.init))
    }

    var x = 0
    var y = 0
    let dX = 3
    let dY = 1

    var trees = 0
    while (y < area.count) {
        let square = area[y][x % area[y].count]
        if square == "#" {
            trees += 1
        }
        x += dX
        y += dY
    }

    print("answer", trees)
}

main()
