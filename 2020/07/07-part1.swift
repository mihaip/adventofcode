#!/usr/bin/env swift

import Foundation

fileprivate class TravelBag: Hashable {
    let color: String
    var parents: Set<TravelBag>
    var contents: [TravelBag]

    init(color: String) {
        self.color = color
        self.parents = Set<TravelBag>()
        self.contents = []
    }

    func addContent(bag: TravelBag) {
        self.contents.append(bag)
        bag.parents.insert(self)
    }

    func ancestors() -> Set<TravelBag> {
        var result = Set(parents)
        for parent in self.parents {
            for ancestor in parent.ancestors() {
                result.insert(ancestor)
            }
        }

        return result
    }

    static func == (lhs: TravelBag, rhs: TravelBag) -> Bool {
        return lhs.color == rhs.color
    }

    func hash(into hasher: inout Hasher) {
        hasher.combine(color)
    }

    static var bags = Dictionary<String, TravelBag>()

    static func getBag(color: String) -> TravelBag {
        if let bag = bags[color] {
            return bag
        }
        let bag = TravelBag(color: color)
        bags[color] = bag
        return bag
    }
}

fileprivate func main() {
    let inputStr = try! String(contentsOf: URL(fileURLWithPath: "./input.txt"))
    let regex = try! NSRegularExpression(pattern: #"(\d+) (.+) bags?"#, options: [])

    for line in inputStr.components(separatedBy: .newlines) {
        if line.isEmpty {
            continue
        }
        let pieces = line.components(separatedBy: " bags contain ")
        let bag = TravelBag.getBag(color: pieces[0])

        let rules = pieces[1]
        if rules == "no other bags." {
            continue
        }

        for rule in rules.components(separatedBy: ", ") {
            let match = regex.firstMatch(in: rule, options: [], range: NSRange(location: 0, length: rule.count))!
            let contentCount = Int(rule[Range(match.range(at: 1), in: line)!])!
            let contentColor = String(rule[Range(match.range(at: 2), in: line)!])

            bag.addContent(bag: TravelBag.getBag(color: contentColor))
        }

    }

    print("answer", TravelBag.getBag(color: "shiny gold").ancestors().count)
}

main()
