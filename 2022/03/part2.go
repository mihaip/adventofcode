package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	total := 0
	groupItems := make(map[rune]int)
	groupCounter := 0

	for scanner.Scan() {
		line := scanner.Text()

		lineItems := make(map[rune]bool)
		for _, i := range line {
			lineItems[i] = true
		}
		for i := range lineItems {
			groupItems[i] += 1
		}

		groupCounter += 1
		if groupCounter == 3 {
			for i, c := range groupItems {
				if c == 3 {
					if i >= 'a' && i <= 'z' {
						total += int(i-'a') + 1
					} else if i >= 'A' && i <= 'Z' {
						total += int(i-'A') + 27
					} else {
						panic("unexpected character")
					}
				}
			}
			groupCounter = 0
			groupItems = make(map[rune]int)
		}
	}
	fmt.Printf("total: %d\n", total)
}
