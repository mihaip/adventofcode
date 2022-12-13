package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
)

type point struct{ x, y int }

const impossible = math.MaxInt32

func walk(grid [][]rune, distances [][]int, p point, currentElevation rune, path int) {
	if p.x == -1 || p.y == -1 || p.x == len(grid[0]) || p.y == len(grid) {
		// Off-grid
		return
	}
	newElevation := grid[p.y][p.x]
	if newElevation-currentElevation > 1 {
		// Too steep
		return
	}

	if path >= distances[p.y][p.x] {
		// Worse path
		return
	}
	distances[p.y][p.x] = path

	for _, delta := range []point{{-1, 0}, {1, 0}, {0, 1}, {0, -1}} {
		newP := point{x: p.x + delta.x, y: p.y + delta.y}
		walk(grid, distances, newP, newElevation, path+1)
	}
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	var start, dest point
	y := 0

	grid := [][]rune{}
	distances := [][]int{}

	for scanner.Scan() {
		line := scanner.Text()
		row := make([]rune, 0, len(line))
		rowDistances := make([]int, 0, len(line))

		for x, c := range line {
			if c == 'S' {
				start.x = x
				start.y = y
				c = 'a'
			} else if c == 'E' {
				dest.x = x
				dest.y = y
				c = 'z'
			}
			row = append(row, c)
			rowDistances = append(rowDistances, impossible)
		}
		y++
		grid = append(grid, row)
		distances = append(distances, rowDistances)
	}

	walk(grid, distances, start, 'a', 0)

	fmt.Printf("best: %d\n", distances[dest.y][dest.x])
}
