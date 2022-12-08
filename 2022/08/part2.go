package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	trees := make([][]int, 0)
	var width int
	for scanner.Scan() {
		line := scanner.Text()
		row := make([]int, 0, len(line))
		for _, tree := range line {
			row = append(row, int(tree-'0'))
		}
		trees = append(trees, row)
		width = len(row)
	}
	height := len(trees)

	best := -1

	computeScore2 := func(x, y, dX, dY int) int {
		if x == 0 || y == 0 || x == width-1 || y == height-1 {
			return 0
		}
		score := 0
		start := trees[y][x]
		if dX == 0 {
			for y1 := y + dY; y1 >= 0 && y1 < height; y1 += dY {
				tree := trees[y1][x]
				score++
				if tree >= start {
					break
				}
			}
		} else {
			for x1 := x + dX; x1 >= 0 && x1 < width; x1 += dX {
				tree := trees[y][x1]
				score++
				if tree >= start {
					break
				}
			}
		}

		return score
	}

	computeScore := func(x, y int) int {
		return computeScore2(x, y, 1, 0) *
			computeScore2(x, y, -1, 0) *
			computeScore2(x, y, 0, 1) *
			computeScore2(x, y, 0, -1)
	}

	for x := 0; x < width; x++ {
		for y := 0; y < height; y++ {
			score := computeScore(x, y)
			if score > best {
				best = score
			}
		}
	}

	fmt.Printf("best: %d\n", best)
}
