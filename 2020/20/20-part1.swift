#!/usr/bin/env swift

import Foundation

let TILE_SIZE = 10

class Tile: Equatable, Hashable, CustomStringConvertible {
    let id: Int
    let data: [[String]]

    init(_ id: Int, _ data: [[String]]) {
        self.id = id
        self.data = data
    }

    public var description: String {
        return "tile\(id)"
    }

    func dump() -> String {
        return data.map{ $0.joined() }.joined(separator: "\n")
    }

    func generateVariants() -> [Tile] {
        var variants: [Tile] = []
        for rotation in 0...3 {
            var rotated = self
            for _ in 0..<rotation {
                rotated = rotated.rotated()
            }
            variants.append(rotated)
            variants.append(rotated.hFlipped())
            variants.append(rotated.vFlipped())
            // Don't need to combine h and v flip because that's the same as a 180° rotation
        }
        return variants
    }

    func rotated() -> Tile {
        var rotatedData = Array(repeating: Array(repeating: "", count: TILE_SIZE), count: TILE_SIZE)
        for x in 0..<TILE_SIZE {
            for y in 0..<TILE_SIZE {
                rotatedData[x][TILE_SIZE - y - 1] = data[y][x]
            }
        }
        return Tile(id, rotatedData)
    }

    func vFlipped() -> Tile {
        var flippedData = Array(repeating: Array(repeating: "", count: TILE_SIZE), count: TILE_SIZE)
        for y in 0..<TILE_SIZE {
            for x in 0..<TILE_SIZE {
                flippedData[TILE_SIZE - y - 1][x] = data[y][x]
            }
        }
        return Tile(id, flippedData)

    }

    func hFlipped() -> Tile {
        var flippedData = Array(repeating: Array(repeating: "", count: TILE_SIZE), count: TILE_SIZE)
        for y in 0..<TILE_SIZE {
            for x in 0..<TILE_SIZE {
                flippedData[y][TILE_SIZE - x - 1] = data[y][x]
            }
        }
        return Tile(id, flippedData)
    }

    func topEdge() -> String {
        return data[0].joined()
    }

    func bottomEdge() -> String {
        return data[TILE_SIZE - 1].joined()
    }

    func leftEdge() -> String {
        return data.map{ $0[0] }.joined()
    }

    func rightEdge() -> String {
        return data.map{ $0[TILE_SIZE - 1] }.joined()
    }

    static func == (lhs: Tile, rhs: Tile) -> Bool {
        return lhs.id == rhs.id && lhs.data == rhs.data
    }

    func hash(into hasher: inout Hasher) {
        hasher.combine(id)
        hasher.combine(data[0][0])
        hasher.combine(data[0][1])
        hasher.combine(data[1][0])
        hasher.combine(data[1][1])
    }
}

fileprivate func main() {
    let inputStr = try! String(contentsOf: URL(fileURLWithPath: "./input.txt"))

    let lines = inputStr.components(separatedBy: .newlines)
    var tiles = Dictionary<Int, Tile>()
    var i = 0
    while i < lines.count {
        let line = lines[i]
        i += 1
        if line.isEmpty {
            continue
        }
        if line.hasPrefix("Tile ") {
            let tileId = Int(line.dropFirst(5).dropLast())!
            let tileData = lines[i..<i + TILE_SIZE].map{ $0.map(String.init) }
            tiles[tileId] = Tile(tileId, tileData)
            i += TILE_SIZE
        } else {
            print("Unexpected line", line)
        }
    }

    var variantsByTopEdges = Dictionary<String, Set<Tile>>()
    var variantsByLeftEdges = Dictionary<String, Set<Tile>>()
    func addVariantEdge(_ variant: Tile, _ edge: String, _ variantsByEdge: inout Dictionary<String, Set<Tile>>) {
        if variantsByEdge[edge] != nil {
            variantsByEdge[edge]!.insert(variant)
        } else {
            variantsByEdge[edge] = Set([variant])
        }
    }
    for tile in tiles.values {
        for variant in tile.generateVariants() {
            addVariantEdge(variant, variant.topEdge(), &variantsByTopEdges)
            addVariantEdge(variant, variant.leftEdge(), &variantsByLeftEdges)
        }
    }

    func pickTile(_ x: Int, _ y: Int, _ pickedTiles: [[Tile]], _ pickedTileIds: Set<Int>) -> Set<Tile> {
        if x == 0 && y == 0 {
            return Set(tiles.values.flatMap{ $0.generateVariants() })
        }
        var hPossibleTiles: Set<Tile>?
        if x > 0 {
            hPossibleTiles = Set()
            let leftNeighbor = pickedTiles[y][x - 1]
            if let variants = variantsByLeftEdges[leftNeighbor.rightEdge()] {
                for variant in variants {
                    if !pickedTileIds.contains(variant.id) {
                        hPossibleTiles!.insert(variant)
                    }
                }
            }
            if hPossibleTiles!.isEmpty {
                return Set()
            }
        }
        if y > 0 {
            var vPossibleTiles = Set<Tile>()
            let topNeighbor = pickedTiles[y - 1][x]
            if let variants = variantsByTopEdges[topNeighbor.bottomEdge()] {
                for variant in variants {
                    if !pickedTileIds.contains(variant.id) && (hPossibleTiles == nil || hPossibleTiles!.contains(variant)) {
                        vPossibleTiles.insert(variant)
                    }
                }
            }
            return vPossibleTiles
        } else {
            return hPossibleTiles!
        }
    }

    let IMAGE_SIZE = Int(sqrt(Double(tiles.count)))

    func tryWithTile(_ tile: Tile, _ x: Int, _ y: Int, _ pickedTiles: inout [[Tile]], _ pickedTileIds: inout Set<Int>) -> Bool {
        var nextX = x + 1
        var nextY = y
        if nextX == IMAGE_SIZE {
            nextX = 0
            nextY = y + 1
        }
        if nextY == IMAGE_SIZE {
            pickedTiles[y][x] = tile
            return true
        }
        var nextPickedTiles = pickedTiles
        nextPickedTiles[y][x] = tile
        var nextPickedTileIds = pickedTileIds
        nextPickedTileIds.insert(tile.id)
        for nextTile in pickTile(nextX, nextY, nextPickedTiles, nextPickedTileIds) {
            if tryWithTile(nextTile, nextX, nextY, &nextPickedTiles, &nextPickedTileIds) {
                pickedTiles = nextPickedTiles
                pickedTileIds = nextPickedTileIds
                return true
            }
        }
        return false
    }


    var firstPickedTiles: [[Tile]] = Array(repeating: Array(repeating: Tile(0, [[]]), count: IMAGE_SIZE), count: IMAGE_SIZE)
    var firstPickedTileIds = Set<Int>()
    for firstTile in pickTile(0, 0, firstPickedTiles, firstPickedTileIds) {
        if tryWithTile(firstTile, 0, 0, &firstPickedTiles, &firstPickedTileIds) {
            let tl = firstPickedTiles[0][0].id
            let tr = firstPickedTiles[0][IMAGE_SIZE - 1].id
            let bl = firstPickedTiles[IMAGE_SIZE - 1][0].id
            let br = firstPickedTiles[IMAGE_SIZE - 1][IMAGE_SIZE - 1].id
            print("answer", tl * tr * bl * br)
            break
        }
    }
}

main()
