package main

import (
	"bufio"
	"container/heap"
	"fmt"
	"log"
	"os"
	"strconv"
)

// An IntHeap is a min-heap of ints.
type IntHeap []int

func (h IntHeap) Len() int           { return len(h) }
func (h IntHeap) Less(i, j int) bool { return h[i] > h[j] }
func (h IntHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }

func (h *IntHeap) Push(x any) {
	// Push and Pop use pointer receivers because they modify the slice's length,
	// not just its contents.
	*h = append(*h, x.(int))
}

func (h *IntHeap) Pop() any {
	old := *h
	n := len(old)
	x := old[n-1]
	*h = old[0 : n-1]
	return x
}

func main() {
	h := &IntHeap{}
	heap.Init(h)

	scanner := bufio.NewScanner(os.Stdin)
	currentSum := 0
	for scanner.Scan() {
		line := scanner.Text()
		if line == "" {
			heap.Push(h, currentSum)
			currentSum = 0
		} else {
			v, err := strconv.ParseInt((line), 10, 64)
			if err != nil {
				log.Fatal(err)
			}
			currentSum += int(v)
		}
	}
	first := heap.Pop(h).(int)
	second := heap.Pop(h).(int)
	third := heap.Pop(h).(int)
	fmt.Printf("first: %d\n", first)
	fmt.Printf("second: %d\n", second)
	fmt.Printf("second: %d\n", second)
	fmt.Printf("total: %d\n", first+second+third)
}
