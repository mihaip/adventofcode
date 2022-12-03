package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	total := 0
	for scanner.Scan() {
		line := scanner.Text()
		mid := len(line) / 2
		c1, c2 := line[0:mid], line[mid:]

		c1Items := make(map[rune]bool)
		for _, i := range c1 {
			c1Items[i] = true
		}

		for _, i := range c2 {
			if _, ok := c1Items[i]; ok {
				if i >= 'a' && i <= 'z' {
					total += int(i-'a') + 1
				} else if i >= 'A' && i <= 'Z' {
					total += int(i-'A') + 27
				} else {
					panic("unexpected character")
				}
				break
			}
		}
	}
	fmt.Printf("total: %d\n", total)
}
