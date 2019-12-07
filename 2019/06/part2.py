#!/usr/local/bin/python3

class Object(object):
    def __init__(self, id):
        self.id = id
        self.children = []
        self.parent = None

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
        child.parent = parent

def get_path(node):
    path = []
    while node:
        path.insert(0, node)
        node = node.parent
    return path

you_path = get_path(objects["YOU"])
santa_path = get_path(objects["SAN"])

for common_ancestor_index in range(min(len(you_path), len(santa_path))):
    you_node = you_path[common_ancestor_index]
    santa_node = santa_path[common_ancestor_index]
    if you_node != santa_node:
        break

print("transfers: %d" % (len(you_path) + len(santa_path) - 2 * (common_ancestor_index + 1)))
