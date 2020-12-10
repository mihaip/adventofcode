#!/usr/bin/env swift

import Foundation

fileprivate class Node {
    let v: Int
    var edges: [Node]
    var pathCount: Int?

    init(_ v: Int) {
        self.v = v
        self.edges = []
        self.pathCount = nil
    }
}

fileprivate func main() {
    let inputStr = try! String(contentsOf: URL(fileURLWithPath: "./input.txt"))

    var numbers: [Int] = []
    for line in inputStr.components(separatedBy: .newlines) {
        if line.isEmpty {
            continue
        }

        let n = Int(line)!
        numbers.append(n)
    }
    numbers.sort()
    numbers.insert(0, at: 0)
    numbers.append(numbers[numbers.count - 1] + 3)

    var nodes: [Node] = []
    for (i, n) in numbers.enumerated() {
        let node = Node(n)
        for j in 1...3 {
            let index = i - j
            if index >= 0 && n - numbers[index] <= 3 {
                nodes[index].edges.append(node)
            }
        }
        nodes.append(node)
    }

    let root = nodes[0]

    func countPaths(_ node: Node) -> Int {
        if node.edges.isEmpty {
            // only the destination has no nodes
            return 1
        }
        if let pathCount = node.pathCount {
            return pathCount
        }
        var pathCount = 0
        for e in node.edges {
            pathCount += countPaths(e)
        }
        node.pathCount = pathCount
        return pathCount
    }

    print("answer", countPaths(root))
}

main()
