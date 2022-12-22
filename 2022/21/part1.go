package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

type Monkey struct {
	result int

	term1 string
	op    string
	term2 string
}

func eval(monkeys map[string]*Monkey, name string) int {
	monkey, ok := monkeys[name]
	if !ok {
		panic(fmt.Sprintf("unknown monkey: %s", name))
	}
	if monkey.result != 0 {
		return monkey.result
	}

	term1 := eval(monkeys, monkey.term1)
	term2 := eval(monkeys, monkey.term2)
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
	monkey.result = result
	return result
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	monkeys := make(map[string]*Monkey)
	for scanner.Scan() {
		line := scanner.Text()

		monkey := &Monkey{}
		name, tail, _ := strings.Cut(line, ": ")

		if _, err := fmt.Sscanf(tail, "%d", &monkey.result); err != nil {
			fmt.Sscanf(tail, "%s %s %s", &monkey.term1, &monkey.op, &monkey.term2)
		}
		monkeys[name] = monkey
	}

	result := eval(monkeys, "root")
	fmt.Printf("result: %d\n", result)
}
