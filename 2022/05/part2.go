package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

type stack struct {
	crates []byte
}

func (s *stack) push(crate byte) {
	s.crates = append(s.crates, crate)
}

func (s *stack) peek() byte {
	return s.crates[len(s.crates)-1]
}

func (s *stack) reverse() {
	for i := 0; i < len(s.crates)/2; i++ {
		j := len(s.crates) - i - 1
		s.crates[i], s.crates[j] = s.crates[j], s.crates[i]
	}
}

func (s *stack) pop() byte {
	if len(s.crates) == 0 {
		return 0
	}
	last := s.crates[len(s.crates)-1]
	s.crates = s.crates[:len(s.crates)-1]
	return last
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	first := true
	var stacks []stack
	var stackCount int
	printStacks := func() {
		maxHeight := 0
		for _, s := range stacks {
			if len(s.crates) > maxHeight {
				maxHeight = len(s.crates)
			}
		}
		for i := maxHeight - 1; i >= 0; i-- {
			for _, s := range stacks {
				if i < len(s.crates) {
					fmt.Printf(" [%c] ", s.crates[i])
				} else {
					fmt.Printf("    ")
				}
			}
			fmt.Println()
		}
		fmt.Println("----------")
	}

	for scanner.Scan() {
		line := scanner.Text()
		if strings.HasPrefix(line, " 1 ") {
			continue
		}
		if line == "" {
			break
		}

		if first {
			stackCount = (len(line) + 1) / 4
			stacks = make([]stack, stackCount)
			first = false
		}

		for i := 0; i < stackCount; i++ {
			crate := line[i*4+1]
			if crate != ' ' {
				stacks[i].push(crate)
			}
		}
	}

	for i := 0; i < stackCount; i++ {
		stacks[i].reverse()
	}
	printStacks()

	for scanner.Scan() {
		line := scanner.Text()
		var count, from, to int
		fmt.Sscanf(line, "move %d from %d to %d", &count, &from, &to)

		moveStack := stack{}
		for i := 0; i < count; i++ {
			moveStack.push(stacks[from-1].pop())
		}
		for i := 0; i < count; i++ {
			stacks[to-1].push(moveStack.pop())
		}
		// printStacks()
	}

	for i := 0; i < stackCount; i++ {
		fmt.Printf("%c", stacks[i].peek())
	}
	fmt.Printf("\n")
}
