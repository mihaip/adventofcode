package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	x := 1
	cycle := 1
	sum := 0
	tick := func() {
		if cycle == 20 || (cycle-20)%40 == 0 {
			fmt.Printf("%d: %d\n", cycle, x)
			sum += cycle * x
		}
		cycle++
	}

	for scanner.Scan() {
		line := scanner.Text()

		if line == "noop" {
			tick()
		} else {
			var delta int
			fmt.Sscanf(line, "addx %d", &delta)
			tick()
			tick()
			x += delta
		}
	}
	fmt.Printf("x: %d\n", x)
	fmt.Printf("sum: %d\n", sum)
}
