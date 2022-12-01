package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
)

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	currentSum := 0
	maxSum := 0
	for scanner.Scan() {
		line := scanner.Text()
		if line == "" {
			if currentSum > maxSum {
				maxSum = currentSum
			}
			currentSum = 0
		} else {
			v, err := strconv.ParseInt((line), 10, 64)
			if err != nil {
				log.Fatal(err)
			}
			currentSum += int(v)
		}
	}
	fmt.Printf("maxSum: %d\n", maxSum)
}
