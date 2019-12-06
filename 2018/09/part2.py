#!/usr/local/bin/python3

import collections
import re

_INPUT_RE = re.compile(r"(\d+) players; last marble is worth (\d+) points")

with open("input.txt") as f:
	player_count, marble_count = map(int, _INPUT_RE.match(f.read()).groups())

marble_count *= 100

player_scores = [0] * player_count
marbles = collections.deque([0])

for i in range(marble_count):
	marble = i + 1
	player_index = i % player_count
	if marble % 23:
		marbles.rotate(-2)
		marbles.appendleft(marble)
	else:
		player_scores[player_index] += marble
		marbles.rotate(7)
		player_scores[player_index] += marbles.popleft()
	
print("winner's score: %d" % max(player_scores))
