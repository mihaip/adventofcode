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

    def sum(self):
        return sum(self.metadata) + sum([c.sum() for c in self.children])

with open("input.txt") as f:
    input = list(map(int, f.read().split()))

def read_input():
    return input.pop(0)

root = Node(read_input(), read_input())
root.read()

print(root.sum())
