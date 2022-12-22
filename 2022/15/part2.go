package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
)

type Sensor struct {
	x, y             int
	beaconX, beaconY int

	minX, maxX, minY, maxY int
	beaconD                int
}

const size = 4000000

type Interval struct {
	Min, Max int
}

type Row struct {
	Occupied []Interval
}

func (r *Row) AddInterval(i Interval) {
	r.Occupied = append(r.Occupied, i)
}

func (r *Row) ComputeFreeSpaces() int {
	sort.Slice(r.Occupied, func(i, j int) bool {
		return r.Occupied[i].Min < r.Occupied[j].Min
	})

	freeSpaces := 0
	if r.Occupied[0].Min > 0 {
		freeSpaces += r.Occupied[0].Min
	}
	max := r.Occupied[0].Max

	for i := 1; i < len(r.Occupied); i++ {
		if r.Occupied[i].Min <= max {
			if r.Occupied[i].Max > max {
				max = r.Occupied[i].Max
			}
			continue
		}

		freeSpaces += r.Occupied[i].Min - max - 1
		max = r.Occupied[i].Max
	}
	if max < size {
		freeSpaces += size - max
	}
	return freeSpaces
}

func (s *Sensor) Precompute() {
	s.beaconD = abs(s.beaconX-s.x) + abs(s.beaconY-s.y)
	s.minY = s.y - s.beaconD
	s.maxY = s.y + s.beaconD
	s.minX = s.x - s.beaconD
	s.maxX = s.x + s.beaconD
}

func (s *Sensor) CanSee(x, y int) bool {
	return abs(x-s.x)+abs(y-s.y) <= s.beaconD
}

func abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	sensorsByRow := map[int][]*Sensor{}
	rowsByRow := map[int]*Row{}

	for scanner.Scan() {
		line := scanner.Text()

		s := Sensor{}
		fmt.Sscanf(line, "Sensor at x=%d, y=%d: closest beacon is at x=%d, y=%d", &s.x, &s.y, &s.beaconX, &s.beaconY)
		s.Precompute()

		width := 0
		widthD := 1
		for y := s.minY; y <= s.maxY; y++ {
			sensorsByRow[y] = append(sensorsByRow[y], &s)
			row, ok := rowsByRow[y]
			if !ok {
				row = &Row{}
				rowsByRow[y] = row
			}
			row.AddInterval(Interval{s.x - width, s.x + width})
			if y == s.y {
				widthD = -widthD
			}
			width += widthD
		}
	}

	minY := 0
	maxY := size

	matchRow := -1
	for y, row := range rowsByRow {
		if y >= minY && y <= maxY {
			if row.ComputeFreeSpaces() == 1 {
				matchRow = y
				break
			}
		}
	}

	fmt.Printf("row: %d\n", matchRow)

	minX := 0
	maxX := size

	sensors := sensorsByRow[matchRow]

	col := minX - 1
	for x := minX; x <= maxX; x++ {
		sensorCanSee := false
		for _, s := range sensors {
			if s.CanSee(x, matchRow) {
				sensorCanSee = true
				break
			}
		}

		if !sensorCanSee {
			col = x
			break
		}
	}

	fmt.Printf("col: %d\n", col)
	fmt.Printf("result: %d\n", matchRow+col*4000000)
}
