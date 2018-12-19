#!/usr/local/bin/python3

class Node:
    def __init__(self, child_count, metadata_count):
        self.child_count = child_count
        self.metadata_count = metadata_count
        self.children = []
        self.metadata = []

    def read(self):
        for i in range(self.child_count):
            child = Node(read_input(), read_input())
            self.children.append(child)
            child.read()
        for i in range(self.metadata_count):
            self.metadata.append(read_input())

    def value(self):
        if not self.children:
            return sum(self.metadata)
        value = 0
        for i in self.metadata:
            if i > len(self.children):
                continue
            value += self.children[i - 1].value()
        return value

with open("input.txt") as f:
    input = list(map(int, f.read().split()))

def read_input():
    return input.pop(0)

root = Node(read_input(), read_input())
root.read()

print(root.value())
