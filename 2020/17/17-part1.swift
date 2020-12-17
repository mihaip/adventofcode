#!/usr/bin/env swift

import Foundation

fileprivate class World {
    var active = Set<String>()
    var minX = 0
    var maxX = 0
    var minY = 0
    var maxY = 0
    var minZ = 0
    var maxZ = 0

    func addActive(_ x: Int, _ y: Int, _ z: Int) {
        if active.isEmpty {
            minX = x
            maxX = x
            minY = y
            maxY = y
            minZ = z
            maxZ = z
        } else {
            if x < minX {
                minX = x
            }
            if x > maxX {
                maxX = x
            }
            if y < minY {
                minY = y
            }
            if y > maxY {
                maxY = y
            }
            if z < minZ {
                minZ = z
            }
            if z > maxZ {
                maxZ = z
            }
        }
        active.insert(key(x, y, z))
    }

    func countActives(_ x: Int, _ y: Int, _ z: Int) -> Int {
        var result = 0
        for dX in -1...1 {
            for dY in -1...1 {
                for dZ in -1...1 {
                    if dX == 0 && dY == 0 && dZ == 0 {
                        continue
                    }
                    if active.contains(key(x + dX, y + dY, z + dZ)) {
                        result += 1
                    }
                }
            }
        }
        return result
    }

    func key(_ x: Int, _ y: Int, _ z: Int) -> String {
        return "\(x)-\(y)-\(z)"
    }

    func step() -> World {
        let world = World()
        for x in minX - 1...maxX + 1 {
            for y in minY - 1...maxY + 1 {
                for z in minZ - 1...maxZ + 1 {
                    let count = countActives(x, y, z)
                    if active.contains(key(x, y, z)) {
                        if count == 2 || count == 3 {
                            world.addActive(x, y, z)
                        }
                    } else {
                        if count == 3 {
                            world.addActive(x, y, z)
                        }
                    }
                }
            }
        }
        return world
    }
}

fileprivate func main() {
    let inputStr = try! String(contentsOf: URL(fileURLWithPath: "./input.txt"))

    let lines = inputStr.components(separatedBy: .newlines)
    var world = World()
    for (y, line) in lines.enumerated() {
        for (x, s) in line.map(String.init).enumerated() {
            if s == "#" {
                world.addActive(x, y, 0)
            }
        }
    }

    for _ in 0...5 {
        world = world.step()
    }
    print("answer", world.active.count)
}

main()
