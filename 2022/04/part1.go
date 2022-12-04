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
		var start1, end1, start2, end2 int
		fmt.Sscanf(line, "%d-%d,%d-%d", &start1, &end1, &start2, &end2)

		if start1 >= start2 && end1 <= end2 {
			total++
		} else if start2 >= start1 && end2 <= end1 {
			total++
		}
	}
	fmt.Printf("total: %d\n", total)
}
