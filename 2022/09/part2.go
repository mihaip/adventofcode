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

type piece struct {
	X, Y int
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	rope := make([]piece, 10)
	tailPath := make(map[string]bool, 0)
	tailPath["0-0"] = true
	updateTail := func(head piece, tail *piece) {
		dX := head.X - tail.X
		dY := head.Y - tail.Y
		if dX >= -1 && dX <= 1 && dY >= -1 && dY <= 1 {
			return
		}

		if dY < 0 {
			tail.Y--
		} else if dY > 0 {
			tail.Y++
		}
		if dX < 0 {
			tail.X--
		} else if dX > 0 {
			tail.X++
		}
	}

	minX := 0
	minY := 0
	maxX := 5
	maxY := 5
	printState := func() {
		for y := minY; y <= maxY; y++ {
			for x := minX; x <= maxX; x++ {
				c := "."
				for i := 0; i < 10; i++ {
					if x == rope[i].X && y == rope[i].Y {
						if i == 0 {
							c = "H"
						} else {
							c = fmt.Sprintf("%d", i)
						}
					}
				}
				fmt.Printf(c)
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
			rope[0].X += dX
			rope[0].Y += dY

			for i := 1; i < 10; i++ {
				updateTail(rope[i-1], &rope[i])
			}
			tailPath[fmt.Sprintf("%d-%d", rope[9].X, rope[9].Y)] = true

			minX = min(minX, rope[0].X, rope[9].X)
			minY = min(minY, rope[0].Y, rope[0].Y)
			maxX = max(maxX, rope[0].X, rope[0].X)
			maxY = max(maxY, rope[0].Y, rope[0].Y)

			// printState()
		}
	}

	printState()

	fmt.Printf("tailPath: %d\n", len(tailPath))

}
