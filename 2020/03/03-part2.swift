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

    var answer = 1
    for (dX, dY) in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)] {
        var x = 0
        var y = 0
        var trees = 0
        while (y < area.count) {
            let square = area[y][x % area[y].count]
            if square == "#" {
                trees += 1
            }
            x += dX
            y += dY
        }
        answer *= trees
    }


    print("answer", answer)
}

main()
