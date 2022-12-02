package main

import (
	"bufio"
	"fmt"
	"os"
)

const rock1 = "A"
const paper1 = "B"
const scissors1 = "C"

const rock2 = "X"
const paper2 = "Y"
const scissors2 = "Z"

var shapeScores = map[string]int{
	rock2:     1,
	paper2:    2,
	scissors2: 3,
}

const loss = 0
const draw = 3
const win = 6

var combinationScores = map[string]int{
	rock1 + rock2:     draw,
	rock1 + paper2:    win,
	rock1 + scissors2: loss,

	paper1 + rock2:     loss,
	paper1 + paper2:    draw,
	paper1 + scissors2: win,

	scissors1 + rock2:     win,
	scissors1 + paper2:    loss,
	scissors1 + scissors2: draw,
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	score := 0
	for scanner.Scan() {
		line := scanner.Text()
		var a, b string
		fmt.Sscanf(line, "%s %s", &a, &b)
		combination := a + b
		score += shapeScores[b] + combinationScores[combination]
	}
	fmt.Printf("score: %d\n", score)
}
