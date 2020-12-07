#!/usr/bin/env swift

import Foundation

func walk(_ sequence: ArraySlice<String>, _ low: String, _ high: String, _ min: Int, _ max: Int) -> Int {
    var curMin = min
    var curMax = max
    var mid = -1
    for v in sequence {
        if v == low {
            mid = Int(floor(Double(curMin + curMax)/2.0))
            curMax = mid
        } else if v == high {
            mid = Int(ceil(Double(curMin + curMax)/2.0))
            curMin = mid
        }
    }
    return mid
}

fileprivate func main() {
    let inputStr = try! String(contentsOf: URL(fileURLWithPath: "./input.txt"))

    var maxSeatId = 0
    for line in inputStr.components(separatedBy: .newlines) {
        if line.isEmpty {
            continue
        }

        let sequence = line.map(String.init)
        let rowSequence = sequence[0...6]
        let row = walk(rowSequence, "F", "B", 0, 127)
        let colSequence = sequence[7...9]
        let col = walk(colSequence, "L", "R", 0, 7)
        let seatId = row * 8 + col
        if seatId > maxSeatId {
            maxSeatId = seatId
        }
    }

    print("answer", maxSeatId)
}

main()
