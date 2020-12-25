#!/usr/bin/env swift

import Foundation

fileprivate func transform(subject: Int, loopSize: Int) -> Int {
    var value = 1
    for _ in 1...loopSize {
        value *= subject
        value = value % 20201227
    }

    return value
}

fileprivate func guessLoopSize(_ expectedValue: Int) -> Int {
    var loopSize = 1;
    var value = 1
    while true {
        value = value * 7 % 20201227
        if value == expectedValue {
            return loopSize
        }
        loopSize += 1
    }
}

fileprivate func main() {
    let inputStr = try! String(contentsOf: URL(fileURLWithPath: "./input.txt"))

    let lines = inputStr.components(separatedBy: .newlines)
    let pk1 = Int(lines[0])!
    let pk2 = Int(lines[1])!

    let loopSize1 = guessLoopSize(pk1)
    let loopSize2 = guessLoopSize(pk2)

    print(loopSize1, loopSize2)

    let encryptionKey1 = transform(subject: pk1, loopSize: loopSize2)
    let encryptionKey2 = transform(subject: pk2, loopSize: loopSize1)
    if encryptionKey1 != encryptionKey2 {
        print("encryption keys should be equal")
    } else {
        print("answer", encryptionKey1)
    }
}

main()
