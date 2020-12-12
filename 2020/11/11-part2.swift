#!/usr/bin/env swift

import Foundation

fileprivate func main() {
    let inputStr = try! String(contentsOf: URL(fileURLWithPath: "./input.txt"))

    var floor = [[String]]()
    for line in inputStr.components(separatedBy: .newlines) {
        if line.isEmpty {
            continue
        }
        floor.append(line.map(String.init))
    }

    while true {
        var newFloor = floor
        var newOccupied = 0
        for (y, row) in floor.enumerated() {
            for (x, seat) in row.enumerated() {
                
                var occupied = 0
                for dX in -1...1 {
                    for dY in -1...1 {
                        if dX == 0 && dY == 0 {
                            continue
                        }

                        var d = 1
                        while (true) {
                            let nX = x + d * dX
                            let nY = y + d * dY
                            if (nX < 0 || nX == row.count || nY < 0 || nY == floor.count) {
                                break
                            }
                            if floor[nY][nX] == "#" {
                                occupied += 1
                                break
                            }
                            if floor[nY][nX] == "L" {
                                break
                            }
                            d += 1
                        }

                        if (occupied == 5) {
                            break
                        }
                    }
                    if (occupied == 5) {
                        break
                    }
                }

                if seat == "L" && occupied == 0 {
                    newFloor[y][x] = "#"
                } else if seat == "#" && occupied >= 5 {
                    newFloor[y][x] = "L"
                } else {
                    newFloor[y][x] = seat
                }
                if newFloor[y][x] == "#" {
                    newOccupied += 1
                }
            }
        }
        if newFloor == floor {
            print("answer", newOccupied)
            break
        }
        floor = newFloor
    }
}

main()
