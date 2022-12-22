package main

import (
	"bufio"
	"fmt"
	"os"
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
	OpenValves           map[*Valve]bool
	Pressure             int
	Time                 int
	CurrentValve         *Valve
	CurrentElephantValve *Valve
}

func (w *World) Tick() {
	for v := range w.OpenValves {
		w.Pressure += v.Flow
	}
	w.Time++
}

func (w *World) MoveTo(v *Valve) {
	w.CurrentValve = v
}

func (w *World) ElephantMoveTo(v *Valve) {
	w.CurrentElephantValve = v
}

func (w *World) CanOpen() bool {
	return !w.OpenValves[w.CurrentValve] && w.CurrentValve.Flow > 0
}

func (w *World) Open() {
	w.OpenValves[w.CurrentValve] = true
}

func (w *World) ElephantCanOpen() bool {
	return !w.OpenValves[w.CurrentElephantValve] && w.CurrentElephantValve.Flow > 0
}

func (w *World) ElephantOpen() {
	w.OpenValves[w.CurrentElephantValve] = true
}

func (w *World) Done() bool {
	return w.Time == 26
}

func (w *World) Fork() *World {
	openValves := make(map[*Valve]bool, len(w.OpenValves))
	for k, v := range w.OpenValves {
		openValves[k] = v
	}
	return &World{
		OpenValves:           openValves,
		Pressure:             w.Pressure,
		Time:                 w.Time,
		CurrentValve:         w.CurrentValve,
		CurrentElephantValve: w.CurrentElephantValve,
	}
}

func (w *World) Key() string {
	openValves := []string{}
	for v := range w.OpenValves {
		openValves = append(openValves, v.Name)
	}
	// sort.Slice(openValves, func(i, j int) bool {
	// 	return openValves[i] < openValves[j]
	// })
	return fmt.Sprintf("%s-%s-%s-%d", w.CurrentValve.Name, w.CurrentElephantValve.Name, strings.Join(openValves, ","), 26-w.Time)
}

var seenWorlds = map[string]*World{}

func Run(w *World) *World {
	k := w.Key()
	if seenWorlds[k] != nil {
		// fmt.Printf("seen %s\n", k)
		return seenWorlds[k]
	}

	for !w.Done() {
		var bestWorld *World

		// nil is signal value for open current valve
		actions := []*Valve{}
		elephantActions := []*Valve{}

		if w.CanOpen() {
			actions = append(actions, nil)
		}
		if w.ElephantCanOpen() {
			elephantActions = append(elephantActions, nil)
		}
		for _, tunnel := range w.CurrentValve.Tunnels {
			actions = append(actions, tunnel)
		}
		for _, tunnel := range w.CurrentElephantValve.Tunnels {
			elephantActions = append(elephantActions, tunnel)
		}

		for _, action := range actions {
			for _, elephantAction := range elephantActions {
				fork := w.Fork()
				fork.Tick()
				if action != nil {
					fork.MoveTo(action)
				} else {
					fork.Open()
				}
				if elephantAction != nil {
					fork.ElephantMoveTo(elephantAction)
				} else {
					fork.ElephantOpen()
				}
				fork = Run(fork)
				if bestWorld == nil || fork.Pressure > bestWorld.Pressure {
					bestWorld = fork
				}
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
		CurrentValve:         valvesByName["AA"],
		CurrentElephantValve: valvesByName["AA"],
		OpenValves:           map[*Valve]bool{},
	}

	world = Run(world)

	fmt.Printf("Time: %d\n", world.Time)
	fmt.Printf("Pressure: %d\n", world.Pressure)
	fmt.Printf("Current Valve: %s\n", world.CurrentValve.Name)
	fmt.Printf("Current Elephant Valve: %s\n", world.CurrentElephantValve.Name)
	fmt.Printf("Open valves:")
	for v := range world.OpenValves {
		fmt.Printf(" %s", v.Name)
	}
	fmt.Printf("\n")
}
