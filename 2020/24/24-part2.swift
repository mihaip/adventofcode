#!/usr/bin/env swift

import Foundation

fileprivate class Tile: Hashable {
    let x: Double
    let y: Double

    init(_ x: Double, _ y: Double) {
        self.x = x
        self.y = y
    }

    func neighbors() -> [Tile] {
        return [
            (1.0, 0.0),
            (-1.0, 0.0),
            (0.5, 0.5),
            (-0.5, 0.5),
            (-0.5, -0.5),
            (0.5, -0.5),
        ].map{ Tile(x + $0.0, y + $0.1) }
    }

    static func == (lhs: Tile, rhs: Tile) -> Bool {
        return lhs.x == rhs.x && lhs.y == rhs.y
    }

    func hash(into hasher: inout Hasher) {
        hasher.combine(x)
        hasher.combine(y)
    }
}

fileprivate func main() {
    let inputStr = try! String(contentsOf: URL(fileURLWithPath: "./input.txt"))

    let lines = inputStr.components(separatedBy: .newlines)

    var flipped = Set<Tile>()
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

        let tile = Tile(x, y)
        if flipped.contains(tile) {
            flipped.remove(tile)
        } else {
            flipped.insert(tile)
        }
    }

    print("flipped", flipped.count)

    for day in 1...100 {
        var nextFlipped = Set<Tile>()

        let allTiles = Set<Tile>(flipped).union(Set(flipped.flatMap{ $0.neighbors() }))
        for tile in allTiles {
            let neighborCount = tile.neighbors().filter{ flipped.contains($0) }.count
            if flipped.contains(tile) {
                if neighborCount == 1 || neighborCount == 2 {
                    nextFlipped.insert(tile)
                }
            } else {
                if neighborCount == 2 {
                    nextFlipped.insert(tile)
                }
            }
        }

        flipped = nextFlipped

        print("day", day, flipped.count)
    }

    print("answer", flipped.count)
}

main()
