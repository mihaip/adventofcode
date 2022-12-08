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

	visible := make(map[string]bool)

	for x := 0; x < width; x++ {
		tallest := -1
		for y := 0; y < height; y++ {
			tree := trees[y][x]
			if tree > tallest {
				visible[fmt.Sprintf("%d-%d", x, y)] = true
				tallest = tree
			}
		}
		tallest = -1
		for y := height - 1; y >= 0; y-- {
			tree := trees[y][x]
			if tree > tallest {
				visible[fmt.Sprintf("%d-%d", x, y)] = true
				tallest = tree
			}
		}
	}
	for y := 0; y < height; y++ {
		tallest := -1
		for x := 0; x < height; x++ {
			tree := trees[y][x]
			if tree > tallest {
				visible[fmt.Sprintf("%d-%d", x, y)] = true
				tallest = tree
			}
		}
		tallest = -1
		for x := width - 1; x >= 0; x-- {
			tree := trees[y][x]
			if tree > tallest {
				visible[fmt.Sprintf("%d-%d", x, y)] = true
				tallest = tree
			}
		}
	}

	fmt.Printf("visible: %d\n", len(visible))
}
