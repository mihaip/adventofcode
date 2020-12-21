#!/usr/bin/env swift

import Foundation

fileprivate func rotate(_ data: [[String]]) -> [[String]] {
    var rotatedData = Array(repeating: Array(repeating: "", count: data.count), count: data.count)
    for x in 0..<data.count {
        for y in 0..<data.count {
            rotatedData[x][data.count - y - 1] = data[y][x]
        }
    }
    return rotatedData
}

fileprivate func vFlip(_ data: [[String]]) -> [[String]] {
    var flippedData = Array(repeating: Array(repeating: "", count: data.count), count: data.count)
    for y in 0..<data.count {
        for x in 0..<data.count {
            flippedData[data.count - y - 1][x] = data[y][x]
        }
    }
    return flippedData

}

fileprivate func hFlip(_ data: [[String]]) -> [[String]] {
    var flippedData = Array(repeating: Array(repeating: "", count: data.count), count: data.count)
    for y in 0..<data.count {
        for x in 0..<data.count {
            flippedData[y][data.count - x - 1] = data[y][x]
        }
    }
    return flippedData
}


fileprivate func generateVariants(_ image: [String]) -> [[String]] {
    var variants: [[[String]]] = []
    let base = image.map{ $0.map(String.init) }
    for rotation in 0...3 {
        var rotated = base
        for _ in 0..<rotation {
            rotated = rotate(rotated)
        }
        variants.append(rotated)
        variants.append(hFlip(rotated))
        variants.append(vFlip(rotated))
        // Don't need to combine h and v flip because that's the same as a 180° rotation
    }

    return variants.map{ $0.map{ $0.joined() }}
}

fileprivate func main() {
    let inputStr = try! String(contentsOf: URL(fileURLWithPath: "./image.txt"))

    let image = inputStr.components(separatedBy: .newlines).filter{ !$0.isEmpty }

    let MONSTER_ROW_1_RE = try! NSRegularExpression(pattern: #"(..................)#(.)"#, options: [])
    let MONSTER_ROW_1_TEMPLATE = "$1O$2"
    let MONSTER_ROW_2_RE = try! NSRegularExpression(pattern: #"#(....)##(....)##(....)###"#, options: [])
    let MONSTER_ROW_2_TEMPLATE = "O$1OO$2OO$3OOO"
    let MONSTER_ROW_3_RE = try! NSRegularExpression(pattern: #"(.)#(..)#(..)#(..)#(..)#(..)#(...)"#, options: [])
    let MONSTER_ROW_3_TEMPLATE = "$1O$2O$3O$4O$5O$6O$7"

    for variant in generateVariants(image) {
        var monsterCount = 0
        var output = variant
        for y in 1..<output.count - 1 {
            // Iterate and keep calling firstMatch (instead of matches) to work around overlapping matches
            for x in 0..<output[y].count {
                if let row2Match = MONSTER_ROW_2_RE.firstMatch(in: output[y], options: [], range: NSRange(location: x, length: output[y].count - x)) {
                    if let row1Match = MONSTER_ROW_1_RE.firstMatch(in: output[y - 1], options: [], range: row2Match.range) {
                        if let row3Match = MONSTER_ROW_3_RE.firstMatch(in: output[y + 1], options: [], range: row2Match.range) {
                            output[y - 1] = MONSTER_ROW_1_RE.stringByReplacingMatches(in: output[y - 1], options: [], range: row1Match.range, withTemplate: MONSTER_ROW_1_TEMPLATE)
                            output[y] = MONSTER_ROW_2_RE.stringByReplacingMatches(in: output[y], options: [], range: row2Match.range, withTemplate: MONSTER_ROW_2_TEMPLATE)
                            output[y + 1] = MONSTER_ROW_3_RE.stringByReplacingMatches(in: output[y + 1], options: [], range: row3Match.range, withTemplate: MONSTER_ROW_3_TEMPLATE)
                            monsterCount += 1
                        }
                    }
                }
            }

        }
        if monsterCount > 0 {
            print("answer", output.joined(separator: "").components(separatedBy: "#").count - 1)
            break
        }

    }
}

main()
