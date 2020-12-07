#!/usr/bin/env swift

import Foundation

fileprivate class Passport {
    var fields = Dictionary<String, String>()

    func isValid() -> Bool {
        return fields["byr"] != nil &&
            fields["iyr"] != nil &&
            fields["eyr"] != nil &&
                fields["hgt"] != nil &&
                fields["hcl"] != nil &&
                fields["ecl"] != nil &&
                fields["pid"] != nil
    }
}

fileprivate func main() {
    let inputStr = try! String(contentsOf: URL(fileURLWithPath: "./input.txt"))

    var currentPassport: Passport? = nil
    var validPassports = 0
    for line in inputStr.components(separatedBy: .newlines) {
        if line.isEmpty {
            if currentPassport?.isValid() ?? false {
                validPassports += 1
            }
            currentPassport = nil
            continue
        }
        if currentPassport == nil {
            currentPassport = Passport()
        }
        for fieldStr in line.components(separatedBy: .whitespaces) {
            let fieldPieces = fieldStr.components(separatedBy: ":")
            currentPassport?.fields[fieldPieces[0]] = fieldPieces[1]
        }
    }

    print("answer", validPassports)
}

main()
