package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strings"
)

type Valve struct {
	Name          string
	Flow          int
	TunnelNames   []string
	Tunnels       []*Valve
	ReachableFlow int
}

type World struct {
	OpenValves   map[*Valve]bool
	Pressure     int
	Time         int
	CurrentValve *Valve
}

func (w *World) MoveTo(v *Valve) {
	// fmt.Printf("MoveTo(%s)\n", v.Name)
	w.Time++
	w.CurrentValve = v
}

func (w *World) CanOpen() bool {
	return !w.OpenValves[w.CurrentValve] && w.CurrentValve.Flow > 0
}

func (w *World) Open() {
	// fmt.Printf("Open(%s)\n", w.CurrentValve.Name)
	w.Time++
	w.OpenValves[w.CurrentValve] = true
	w.Pressure += (30 - w.Time) * w.CurrentValve.Flow
}

func (w *World) Done() bool {
	return w.Time == 30
}

func (w *World) Fork() *World {
	openValves := make(map[*Valve]bool, len(w.OpenValves))
	for k, v := range w.OpenValves {
		openValves[k] = v
	}
	return &World{
		OpenValves:   openValves,
		Pressure:     w.Pressure,
		Time:         w.Time,
		CurrentValve: w.CurrentValve,
	}
}

func (w *World) Key() string {
	openValves := []string{}
	for v := range w.OpenValves {
		openValves = append(openValves, v.Name)
	}
	sort.Slice(openValves, func(i, j int) bool {
		return openValves[i] < openValves[j]
	})
	return fmt.Sprintf("%s-%s-%d", w.CurrentValve.Name, strings.Join(openValves, ","), w.Time)
}

var seenWorlds = map[string]*World{}

func Run(w *World) *World {
	k := w.Key()
	if w, ok := seenWorlds[k]; ok {
		return w
	}

	for !w.Done() {
		var bestWorld *World
		if w.CanOpen() {
			bestWorld = w.Fork()
			bestWorld.Open()
			bestWorld = Run(bestWorld)
		}

		for _, tunnel := range w.CurrentValve.Tunnels {
			fork := w.Fork()
			fork.MoveTo(tunnel)
			fork = Run(fork)
			if bestWorld == nil || fork.Pressure > bestWorld.Pressure {
				bestWorld = fork
			}
		}

		if bestWorld == nil {
			panic(fmt.Sprintf("no choice at time %d", w.Time))
		}
		w = bestWorld
	}
	seenWorlds[k] = w
	return w
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	valvesByName := map[string]*Valve{}

	for scanner.Scan() {
		valve := &Valve{}

		line := scanner.Text()

		head, tail, _ := strings.Cut(line, "; ")

		fmt.Sscanf(head, "Valve %s has flow rate=%d", &valve.Name, &valve.Flow)
		valvesByName[valve.Name] = valve

		if strings.HasPrefix(tail, "tunnels lead to valves ") {
			tail = tail[23:]
		} else if strings.HasPrefix(tail, "tunnel leads to valve ") {
			tail = tail[22:]
		}
		valve.TunnelNames = strings.Split(tail, ", ")
	}

	for _, valve := range valvesByName {
		for _, tunnelName := range valve.TunnelNames {
			valve.Tunnels = append(valve.Tunnels, valvesByName[tunnelName])
		}
	}

	world := &World{
		CurrentValve: valvesByName["AA"],
		OpenValves:   map[*Valve]bool{},
	}

	world = Run(world)

	fmt.Printf("Time: %d\n", world.Time)
	fmt.Printf("Pressure: %d\n", world.Pressure)
	fmt.Printf("Open valves:")
	for v := range world.OpenValves {
		fmt.Printf(" %s", v.Name)
	}
	fmt.Printf("\n")
}
