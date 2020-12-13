#!/usr/bin/env swift

import Foundation

fileprivate func main() {
    let inputStr = try! String(contentsOf: URL(fileURLWithPath: "./input.txt"))

    let lines = inputStr.components(separatedBy: .newlines)
    let time = Int(lines[0])!
    let buses = lines[1].components(separatedBy: ",").filter{ $0 != "x" }.compactMap(Int.init)

    var bestBus: Int? = nil
    var bestBusTime = 0
    for bus in buses {
        let busTime = Int(ceil(Float(time) / Float(bus))) * bus
        if bestBus == nil || busTime < bestBusTime {
            bestBus = bus
            bestBusTime = busTime
        }
    }

    if let bestBus = bestBus {
        print("answer", bestBus * (bestBusTime - time))
    }
}

main()
