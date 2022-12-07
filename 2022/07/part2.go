package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

type entry struct {
	name     string
	children map[string]*entry
	size     int
	parent   *entry
}

func newDirEntry(name string) *entry {
	return &entry{
		name:     name,
		children: make(map[string]*entry, 0),
	}
}

func (e *entry) addChild(child *entry) {
	if e.children == nil {
		panic(fmt.Sprintf("Tried to add child %+v to file %+v", child, e))
	}
	e.children[child.name] = child
	child.parent = e
}

func newFileEntry(name string, size int) *entry {
	return &entry{
		name: name,
		size: size,
	}
}

func sumTraverse(e *entry) int {
	if e.children == nil {
		return e.size
	}
	childrenSum := 0
	for _, c := range e.children {
		childrenSum += sumTraverse(c)
	}

	return childrenSum
}

func findMatch(e *entry, needFree int, match *int) int {
	if e.children == nil {
		return e.size
	}
	childrenSum := 0
	for _, c := range e.children {
		childrenSum += findMatch(c, needFree, match)
	}
	if childrenSum >= needFree {
		if *match == 0 || childrenSum < *match {
			*match = childrenSum
		}
	}

	return childrenSum
}

func main() {
	root := newDirEntry("/")
	cwd := root

	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		line := scanner.Text()
	resume:
		if strings.HasPrefix(line, "$ cd") {
			var path string
			fmt.Sscanf(line, "$ cd %s", &path)
			if path == "/" {
				cwd = root
			} else if path == ".." {
				cwd = cwd.parent
			} else {
				if _, ok := cwd.children[path]; !ok {
					panic(fmt.Sprintf("Could not find %q in line: %+v", path, cwd))
				}
				cwd = cwd.children[path]
			}
		} else if strings.HasPrefix(line, "$ ls") {
			for scanner.Scan() {
				line = scanner.Text()
				if strings.HasPrefix(line, "$ ") {
					goto resume
				} else if strings.HasPrefix(line, "dir ") {
					var name string
					fmt.Sscanf(line, "dir %s", &name)
					cwd.addChild(newDirEntry(name))
				} else {
					var size int
					var name string
					fmt.Sscanf(line, "%d %s", &size, &name)
					cwd.addChild(newFileEntry(name, size))
				}
			}
		} else {
			panic(fmt.Sprintf("unexpected line: %q", line))
		}
	}

	totalUsed := sumTraverse(root)
	currentFree := 70000000 - totalUsed
	needFree := 30000000 - currentFree

	var deleteSize int
	findMatch(root, needFree, &deleteSize)

	fmt.Printf("deleteSize: %d\n", deleteSize)
}
