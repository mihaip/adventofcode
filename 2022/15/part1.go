package main

import (
	"bufio"
	"fmt"
	"os"
)

type Sensor struct {
	x, y             int
	beaconX, beaconY int

	minX, maxX, minY, maxY int
	beaconD                int
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

	for scanner.Scan() {
		line := scanner.Text()

		s := Sensor{}
		fmt.Sscanf(line, "Sensor at x=%d, y=%d: closest beacon is at x=%d, y=%d", &s.x, &s.y, &s.beaconX, &s.beaconY)
		s.Precompute()

		for y := s.minY; y <= s.maxY; y++ {
			sensorsByRow[y] = append(sensorsByRow[y], &s)
		}
	}

	row := 2000000

	sensors := sensorsByRow[row]
	minX := sensors[0].minX
	maxX := sensors[0].maxX
	for _, s := range sensors {
		if s.minX < minX {
			minX = s.minX
		}
		if s.maxX > maxX {
			maxX = s.maxX
		}
	}

	rowElements := map[int]bool{}
	for x := minX; x <= maxX; x++ {
		hasBeacon := false
		sensorCanSee := false
		for _, s := range sensors {
			if s.beaconX == x && s.beaconY == row {
				hasBeacon = true
				break
			}
			if s.CanSee(x, row) {
				sensorCanSee = true
			}
		}

		if sensorCanSee && !hasBeacon {
			rowElements[x] = true
		}
	}

	fmt.Printf("result: %d\n", len(rowElements))
}
