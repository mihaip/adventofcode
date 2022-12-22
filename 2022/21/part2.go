package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strings"
)

type Monkey struct {
	name string

	result int

	term1Name string
	term1     *Monkey
	op        string
	term2Name string
	term2     *Monkey
}

func hasHuman(monkey *Monkey) bool {
	if monkey.name == "humn" {
		return true
	}
	if monkey.result != 0 {
		return false
	}
	return hasHuman(monkey.term1) || hasHuman(monkey.term2)
}

func eval(monkey *Monkey) int {
	if monkey.result != 0 || monkey.name == "humn" {
		return monkey.result
	}

	term1 := eval(monkey.term1)
	term2 := eval(monkey.term2)
	var result int
	switch monkey.op {
	case "+":
		result = term1 + term2
	case "*":
		result = term1 * term2
	case "-":
		result = term1 - term2
	case "/":
		result = term1 / term2
	default:
		panic("unknown op")
	}
	return result
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	monkeys := make(map[string]*Monkey)
	for scanner.Scan() {
		line := scanner.Text()

		name, tail, _ := strings.Cut(line, ": ")
		monkey := &Monkey{name: name}

		if _, err := fmt.Sscanf(tail, "%d", &monkey.result); err != nil {
			fmt.Sscanf(tail, "%s %s %s", &monkey.term1Name, &monkey.op, &monkey.term2Name)
		}
		monkeys[name] = monkey
	}

	for _, monkey := range monkeys {
		if monkey.term1Name != "" {
			monkey.term1 = monkeys[monkey.term1Name]
		}
		if monkey.term2Name != "" {
			monkey.term2 = monkeys[monkey.term2Name]
		}
	}

	root := monkeys["root"]
	human := monkeys["humn"]

	term1HasHuman := hasHuman(root.term1)
	term2HasHuman := hasHuman(root.term2)
	if term1HasHuman == term2HasHuman {
		panic("no solution")
	}

	var expected int
	var humanTerm *Monkey
	if term1HasHuman {
		expected = eval(root.term2)
		humanTerm = root.term1
	} else {
		expected = eval(root.term1)
		humanTerm = root.term2
	}

	fmt.Printf("expected: %d\n", expected)
	min := 0
	max := 0
	human.result = 1

	for {
		testResult := eval(humanTerm)
		if testResult < expected {
			max = human.result
			break
		}
		min = human.result
		human.result *= 2
	}

	fmt.Printf("min: %d max: %d\n", min, max)

	result := sort.Search(max-min, func(i int) bool {
		human.result = min + i
		testResult := eval(humanTerm)
		return testResult <= expected
	})

	human.result = result + min
	testResult := eval(humanTerm)
	fmt.Printf("human: %d: testResult: %d (delta: %d)\n", human.result, testResult, testResult-expected)
}
