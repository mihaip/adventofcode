package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"
)

type Monkey struct {
	Items        []int64
	OpTerm1      string
	Op           string
	OpTerm2      string
	TestConstant int64
	TrueDest     int
	FalseDest    int

	InspectionCount int
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	monkeys := make(map[int]*Monkey)

	for scanner.Scan() {
		line := scanner.Text()

		var index int
		c, err := fmt.Sscanf(line, "Monkey %d", &index)
		if err != nil || c != 1 {
			panic(fmt.Sprintf("Unexpected line: %q", line))
		}

		monkey := &Monkey{}
		monkeys[index] = monkey

		scanner.Scan()
		itemsStr := strings.TrimPrefix(scanner.Text(), "  Starting items: ")
		for _, itemStr := range strings.Split(itemsStr, ", ") {
			item, _ := strconv.ParseInt(itemStr, 10, 64)
			monkey.Items = append(monkey.Items, item)
		}

		scanner.Scan()
		fmt.Sscanf(scanner.Text(), "  Operation: new = %s %s %s", &monkey.OpTerm1, &monkey.Op, &monkey.OpTerm2)

		scanner.Scan()
		fmt.Sscanf(scanner.Text(), "  Test: divisible by %d", &monkey.TestConstant)

		scanner.Scan()
		fmt.Sscanf(scanner.Text(), "    If true: throw to monkey %d", &monkey.TrueDest)

		scanner.Scan()
		fmt.Sscanf(scanner.Text(), "    If false: throw to monkey %d", &monkey.FalseDest)

		scanner.Scan()
	}

	for i := 0; i < 20; i++ {
		for index := 0; index < len(monkeys); index++ {
			monkey := monkeys[index]
			for _, item := range monkey.Items {
				monkey.InspectionCount++
				term1 := item
				if monkey.OpTerm1 != "old" {
					term1, _ = strconv.ParseInt(monkey.OpTerm1, 10, 64)
				}
				term2 := item
				if monkey.OpTerm2 != "old" {
					term2, _ = strconv.ParseInt(monkey.OpTerm2, 10, 64)
				}

				var result int64
				switch monkey.Op {
				case "+":
					result = term1 + term2
				case "*":
					result = term1 * term2
				default:
					panic(fmt.Sprintf("Unknown op %q", monkey.Op))
				}

				result /= 3

				var dest int
				if result%monkey.TestConstant == 0 {
					dest = monkey.TrueDest
				} else {
					dest = monkey.FalseDest
				}
				monkeys[dest].Items = append(monkeys[dest].Items, result)
			}
			monkey.Items = []int64{}
		}
	}

	for index := 0; index < len(monkeys); index++ {
		m := monkeys[index]
		fmt.Printf("Monkey %d: %d\n", index, m.InspectionCount)
	}

	sortedMonkeys := make([]*Monkey, 0, len(monkeys))
	for _, monkey := range monkeys {
		sortedMonkeys = append(sortedMonkeys, monkey)
	}

	sort.Slice(sortedMonkeys, func(i, j int) bool {
		return sortedMonkeys[i].InspectionCount > sortedMonkeys[j].InspectionCount
	})

	fmt.Printf("monkey business: %d\n", sortedMonkeys[0].InspectionCount*sortedMonkeys[1].InspectionCount)
}
