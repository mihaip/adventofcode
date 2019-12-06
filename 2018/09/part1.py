#!/usr/local/bin/python3

import re

_INPUT_RE = re.compile(r"(\d+) players; last marble is worth (\d+) points")

with open("input.txt") as f:
	player_count, marble_count = map(int, _INPUT_RE.match(f.read()).groups())

player_scores = [0] * player_count
marbles = [0]
cursor = 0

def marble_index(index):
	while index < 0:
		index += len(marbles)
	return index % len(marbles)

for i in range(marble_count):
	marble = i + 1
	player_index = i % player_count
	if marble % 23:
		insert_index = marble_index(cursor + 2)
		marbles.insert(insert_index, marble)
		cursor = insert_index
	else:
		player_scores[player_index] += marble
		removed_index = marble_index(cursor - 7)
		player_scores[player_index] += marbles[removed_index]
		marbles.pop(removed_index)
		cursor = removed_index
	
print("winner's score: %d" % max(player_scores))
