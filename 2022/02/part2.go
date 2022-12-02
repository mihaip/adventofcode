package main

import (
	"bufio"
	"fmt"
	"os"
)

const rock = "A"
const paper = "B"
const scissors = "C"

const loss = "X"
const draw = "Y"
const win = "Z"

var shapeScores = map[string]int{
	rock:     1,
	paper:    2,
	scissors: 3,
}

var outcomeScores = map[string]int{
	loss: 0,
	draw: 3,
	win:  6,
}

var combinationChoices = map[string]string{
	rock + loss: scissors,
	rock + draw: rock,
	rock + win:  paper,

	paper + loss: rock,
	paper + draw: paper,
	paper + win:  scissors,

	scissors + loss: paper,
	scissors + draw: scissors,
	scissors + win:  rock,
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	score := 0
	for scanner.Scan() {
		line := scanner.Text()
		var a, b string
		fmt.Sscanf(line, "%s %s", &a, &b)
		combination := a + b
		choice := combinationChoices[combination]
		score += shapeScores[choice] + outcomeScores[b]
	}
	fmt.Printf("score: %d\n", score)
}
