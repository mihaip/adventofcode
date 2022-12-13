package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"os"
)

func parse(line string) []any {
	result := []any{}
	json.Unmarshal([]byte(line), &result)
	return result
}

type Result int

const (
	Unknown Result = iota
	Right
	Wrong
)

func compare(packet1, packet2 any, result *Result) {
	if *result != Unknown {
		return
	}
	i1, isNum1 := packet1.(float64)
	i2, isNum2 := packet2.(float64)
	if isNum1 && isNum2 {
		if i1 < i2 {
			*result = Right
		} else if i1 > i2 {
			*result = Wrong
		}
		return
	}
	var l1, l2 []any
	if isNum1 {
		l1 = []any{i1}
		l2 = packet2.([]any)
	} else if isNum2 {
		l1 = packet1.([]any)
		l2 = []any{i2}
	} else {
		l1 = packet1.([]any)
		l2 = packet2.([]any)
	}
	l := len(l1)
	if len(l2) > l {
		l = len(l2)
	}
	for i := 0; i < l; i++ {
		if i == len(l1) {
			*result = Right
			return
		}
		if i == len(l2) {
			*result = Wrong
			return
		}
		compare(l1[i], l2[i], result)
		if *result != Unknown {
			return
		}
	}
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	index := 1
	sum := 0
	for scanner.Scan() {
		packets1 := parse(scanner.Text())
		scanner.Scan()
		packets2 := parse(scanner.Text())

		result := Unknown
		compare(packets1, packets2, &result)
		if result == Right {
			sum += index
		}

		scanner.Scan()
		index++
	}

	fmt.Printf("sum: %d\n", sum)
}
