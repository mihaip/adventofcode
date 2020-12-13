#!/usr/bin/env swift

import Foundation

/*
 * Function: euclid
 * Usage: (r,s) = euclid(m,n)
 * --------------------------
 * The extended Euclidean algorithm subsequently performs
 * Euclidean divisions till the remainder is zero and then
 * returns the Bézout coefficients r and s.
 */
fileprivate func euclid(_ m:Int, _ n:Int) -> (Int,Int) {
    if m % n == 0 {
        return (0,1)
    } else {
        let rs = euclid(n % m, m)
        let r = rs.1 - rs.0 * (n / m)
        let s = rs.0

        return (r,s)
    }
}

/*
 * Function: crt
 * Usage: x = crt(a,n)
 * -------------------
 * The Chinese Remainder Theorem supposes that given the
 * integers n_1...n_k that are pairwise co-prime, then for
 * any sequence of integers a_1...a_k there exists an integer
 * x that solves the system of linear congruences:
 *
 *   x === a_1 (mod n_1)
 *   ...
 *   x === a_k (mod n_k)
 */

fileprivate func crt(_ a_i:[Int], _ n_i:[Int]) -> Int {
    // Calculate factor N
    let N = n_i.map{$0}.reduce(1, *)

    // Euclidean algorithm determines s_i (and r_i)
    var s_i:[Int] = []
    for n in n_i {
        var t = euclid(n, N / n).1
        if t < 0 {
            t += n
        }
        s_i.append(t)
    }

    // Solve for x
    var x = 0
    for (a, (n, s)) in zip(a_i, zip(n_i, s_i)) {
        x += N / n * a * s
    }

    // Return minimal solution
    return x % N
}

fileprivate func main() {
    let inputStr = try! String(contentsOf: URL(fileURLWithPath: "./input.txt"))

    let lines = inputStr.components(separatedBy: .newlines)
    let buses = lines[1].components(separatedBy: ",").map(Int.init)

    var numbers: [Int] = []
    var offsets : [Int] = []
    for (i, bus) in buses.enumerated() {
        if let bus = bus {
            numbers.append(bus)
            offsets.append(i)
        }
    }

    var remainders: [Int] = []
    for (number, offset) in zip(numbers, offsets) {
        if offset == 0 {
            remainders.append(0)
        } else {
            remainders.append(number - offset % number)
        }
    }

    print("answer", crt(remainders, numbers))
}

main()
