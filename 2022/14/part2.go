package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"strings"
)

const size = 1000

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	rock := make([][]bool, size)
	for i := range rock {
		rock[i] = make([]bool, size)
	}
	minX := math.MaxInt32
	maxX := 0
	minY := math.MaxInt32
	maxY := 0

	for scanner.Scan() {
		line := scanner.Text()

		prevX := -1
		prevY := -1
		for _, pair := range strings.Split(line, " -> ") {
			var x, y int

			fmt.Sscanf(pair, "%d,%d", &x, &y)
			minX = min(minX, x)
			maxX = max(maxX, x)
			minY = min(minY, y)
			maxY = max(maxY, y)

			if prevX == -1 {
				prevX, prevY = x, y
				continue
			}

			if prevX == x {
				dY := 1
				if prevY > y {
					dY = -1
				}
				for drawY := prevY; drawY != y; drawY += dY {
					rock[drawY][x] = true
				}
			} else {
				dX := 1
				if prevX > x {
					dX = -1
				}
				for drawX := prevX; drawX != x; drawX += dX {
					rock[y][drawX] = true
				}
			}
			rock[y][x] = true
			prevX, prevY = x, y
		}
	}

	for y := minY; y <= maxY; y++ {
		for x := minX; x <= maxX; x++ {
			if rock[y][x] {
				fmt.Print("#")
			} else {
				fmt.Print(".")
			}
		}
		fmt.Println()
	}

	for x := 0; x < size; x++ {
		rock[maxY+2][x] = true
	}

	count := 0
	for {
		x, y := 500, 0
		if rock[y][x] {
			break
		}
		for {
			if !rock[y+1][x] {
				y++
				continue
			}
			if !rock[y+1][x-1] {
				y++
				x--
				continue
			}
			if !rock[y+1][x+1] {
				y++
				x++
				continue
			}
			rock[y][x] = true
			count++
			break
		}
	}

	fmt.Printf("count: %d\n", count)
}
