package main

import (
	"bufio"
	"fmt"
	"os"
)

func min(start int, rest ...int) int {
	r := start
	for _, a := range rest {
		if a < r {
			r = a
		}
	}
	return r
}

func max(start int, rest ...int) int {
	r := start
	for _, a := range rest {
		if a > r {
			r = a
		}
	}
	return r
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	headX := 0
	headY := 0
	tailX := 0
	tailY := 0
	tailPath := make(map[string]bool, 0)
	tailPath["0-0"] = true
	updateTail := func() {
		dX := headX - tailX
		dY := headY - tailY
		if dX >= -1 && dX <= 1 && dY >= -1 && dY <= 1 {
			return
		}

		if dY < 0 {
			tailY--
		} else if dY > 0 {
			tailY++
		}
		if dX < 0 {
			tailX--
		} else if dX > 0 {
			tailX++
		}
	}

	minX := 0
	minY := 0
	maxX := 5
	maxY := 5
	printState := func() {
		for y := minY; y <= maxY; y++ {
			for x := minX; x <= maxX; x++ {
				if x == headX && y == headY {
					fmt.Printf("H")
				} else if x == tailX && y == tailY {
					fmt.Printf("T")
				} else {
					fmt.Printf(".")
				}
			}
			fmt.Printf("\n")
		}
		fmt.Printf("\n")
	}

	for scanner.Scan() {
		line := scanner.Text()
		var direction string
		var length int
		fmt.Sscanf(line, "%s %d", &direction, &length)

		var dX, dY int
		switch direction {
		case "R":
			dX = 1
		case "L":
			dX = -1
		case "U":
			dY = 1
		case "D":
			dY = -1
		}

		for i := 0; i < length; i++ {
			headX += dX
			headY += dY

			updateTail()
			tailPath[fmt.Sprintf("%d-%d", tailX, tailY)] = true

			minX = min(minX, headX, tailX)
			minY = min(minY, headY, tailY)
			maxX = max(maxX, headX, tailX)
			maxY = max(maxY, headY, tailY)

			// printState()
		}
	}

	printState()

	fmt.Printf("tailPath: %d\n", len(tailPath))

}
