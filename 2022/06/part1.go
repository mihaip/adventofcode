package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		line := scanner.Text()

		const cap = 3
		buf := make([]rune, cap)
		var i = 0

		for _, c := range line {
			i++
			if i < cap+1 {
				buf[i-1] = c
				continue
			}

			hasCollision := false
			set := make(map[rune]bool, cap+1)
			for _, c := range buf {
				if _, ok := set[c]; ok {
					hasCollision = true
					break
				}
				set[c] = true
			}
			if _, ok := set[c]; ok {
				hasCollision = true
			}

			if !hasCollision {
				fmt.Printf("answer: %d\n", i)
				break
			}

			for i := 0; i < cap-1; i++ {
				buf[i] = buf[i+1]
			}
			buf[cap-1] = c
		}
	}
	fmt.Printf("Done\n")
}
