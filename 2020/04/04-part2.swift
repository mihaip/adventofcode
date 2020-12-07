#!/usr/bin/env swift

import Foundation

fileprivate class Passport {
    private var validFieldCount = 0

    func addField(name: String, value: String) {
        switch (name) {
        case "byr":
            if value.count == 4 {
                if let year = Int(value) {
                    if year >= 1920 && year <= 2002 {
                        validFieldCount += 1
                    }
                }
            }
            break
        case "iyr":
            if value.count == 4 {
                if let year = Int(value) {
                    if year >= 2010 && year <= 2020 {
                        validFieldCount += 1
                    }
                }
            }
            break
        case "eyr":
            if value.count == 4 {
                if let year = Int(value) {
                    if year >= 2020 && year <= 2030 {
                        validFieldCount += 1
                    }
                }
            }
            break
        case "hgt":
            if value.hasSuffix("cm") {
                if let height = Int(value[...value.index(value.endIndex, offsetBy: -3)]) {
                    if height >= 150 && height <= 193 {
                        validFieldCount += 1
                    }
                }
            } else if value.hasSuffix("in") {
                if let height = Int(value[...value.index(value.endIndex, offsetBy: -3)]) {
                    if height >= 59 && height <= 76 {
                        validFieldCount += 1
                    }
                }

            }
            break
        case "hcl":
            if value.count == 7 && value.range(of: #"#[0-9a-f]{6}"#, options: .regularExpression, range: nil, locale: nil) != nil {
                validFieldCount += 1
            }
            break
        case "ecl":
            if ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"].contains(value) {
                validFieldCount += 1
            }
        case "pid":
            if value.count == 9 && Int(value) != nil {
                validFieldCount += 1
            }
        default:
            break

        }
    }

    func isValid() -> Bool {
        return validFieldCount == 7
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
            currentPassport?.addField(name: fieldPieces[0], value: fieldPieces[1])
        }
    }

    print("answer", validPassports)
}

main()
