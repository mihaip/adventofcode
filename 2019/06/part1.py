#!/usr/local/bin/python3

class Object(object):
    def __init__(self, id):
        self.id = id
        self.children = []

root = Object("COM")
objects = {"COM": root}

def get_object(id):
    if id not in objects:
        objects[id] = Object(id)
    return objects[id]

with open("input.txt") as f:
    for line in f.readlines():
        parent, child = map(get_object, line.strip().split(")"))
        parent.children.append(child)

checksum = 0

def traverse(node, distance):
    global checksum
    checksum += distance
    for child in node.children:
        traverse(child, distance + 1)
traverse(root, 0)
print("checksum: %d" % checksum)
