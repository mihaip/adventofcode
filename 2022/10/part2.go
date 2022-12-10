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
	screen := make([]string, 240)
	tick := func() {
		screenX := (cycle - 1) % 40
		if screenX == x || screenX == x+1 || screenX == x-1 {
			screen[cycle-1] = "#"
		} else {
			screen[cycle-1] = " "
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
	for screenX := 0; screenX < 240; screenX++ {
		if screenX%40 == 0 && screenX > 0 {
			fmt.Printf("\n")
		}
		fmt.Printf("%s", screen[screenX])
	}
	fmt.Printf("\n")
}
