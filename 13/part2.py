#!/usr/local/bin/python3

import copy
import re

_CART_RE = re.compile(r"([v\^<>])")
_LEFT_TURNS = [
	[[0, -1], [-1, 0]],
	[[-1, 0], [0, 1]],
	[[0, 1], [1, 0]],
	[[1, 0], [0, -1]]
]
_RIGHT_TURNS = [[b, a] for a, b in _LEFT_TURNS]

class Cart:
	def __init__(self, x, y, dx, dy):
		self.x = x
		self.y = y
		self.dx = dx
		self.dy = dy
		self.turn_counter = 0
	
	def tick(self):
		self.x += self.dx
		self.y += self.dy
		track = map[self.y][self.x]
		if track == '-':
			assert self.dy == 0
		elif track == '|':
			assert self.dx == 0
		elif track == '/':
			if self.dx == 0 and self.dy == 1:
				self.dx = -1
				self.dy = 0
			elif self.dx == 1 and self.dy == 0:
				self.dx = 0
				self.dy = -1
			elif self.dx == 0 and self.dy == -1:
				self.dx = 1
				self.dy = 0
			elif self.dx == -1 and self.dy == 0:
				self.dx = 0
				self.dy = 1
			else:
				assert False, "Unexpected speed %d,%d for / turn" % (self.dx, self.dy)
		elif track == '\\':
			if self.dx == 0 and self.dy == 1:
				self.dx = 1
				self.dy = 0
			elif self.dx == 1 and self.dy == 0:
				self.dx = 0
				self.dy = 1
			elif self.dx == 0 and self.dy == -1:
				self.dx = -1
				self.dy = 0
			elif self.dx == -1 and self.dy == 0:
				self.dx = 0
				self.dy = -1
			else:
				assert False, r"Unexpected speed %d,%d for \ turn" % (self.dx, self.dy)
		elif track == '+':
			turn_index = self.turn_counter % 3
			if turn_index == 0:
				for cur, new in _LEFT_TURNS:
					if cur[0] == self.dx and cur[1] == self.dy:
						self.dx = new[0]
						self.dy = new[1]
						break
			elif turn_index == 1:
				# straight, do nothing
				pass
			elif turn_index == 2:
				for cur, new in _RIGHT_TURNS:
					if cur[0] == self.dx and cur[1] == self.dy:
						self.dx = new[0]
						self.dy = new[1]
						break
			self.turn_counter += 1
		else:
			assert False, "Unexpected track piece '%s'" % track
		
		for c in active_carts:
			if c != self and c.x == self.x and c.y == self.y:
				return c
		return None
	
	def cart_char(self):
		if self.dx == 0 and self.dy == 1:
			return "v"
		elif self.dx == 1 and self.dy == 0:
			return ">"
		elif self.dx == 0 and self.dy == -1:
			return "^"
		elif self.dx == -1 and self.dy == 0:
			return "<"
		else:
			assert False, "Unexpected speed %d,%d" % (self.dx, self.dy)
				
def print_state():
	state = []
	for line in map:
		state.append(list(line))
	for cart in carts:
		state[cart.y][cart.x] = cart.cart_char()
	for row in state:
		print("".join(row))

map = []
carts = []

with open("input.txt") as f:
	for line in f.readlines():
		line = line[:-1]
		map_line = list(line)
		y = len(map)
		for cart_match in _CART_RE.finditer(line):
			x = cart_match.start(1)
			cart_char = cart_match.group(1)
			if cart_char == '^':
				dx = 0
				dy = -1
				track = '|'
			elif cart_char == 'v':
				dx = 0
				dy = 1
				track = '|'
			elif cart_char == '<':
				dx = -1
				dy = 0
				track = '-'
			elif cart_char == '>':
				dx = 1
				dy = 0
				track = '-'
			else:
				assert False, "Unexpected cart character: %s" % cart_char
			carts.append(Cart(x, y, dx, dy))
			map_line[x] = track
		map.append("".join(map_line))


active_carts = copy.copy(carts)

while len(active_carts) > 1:
	carts = list(sorted(active_carts, key=lambda c: [c.y, c.x]))
	
	for cart in carts:
		collided_cart = cart.tick()
		if collided_cart:
			active_carts.remove(cart)
			active_carts.remove(collided_cart)

cart = active_carts[0]
print("%d,%d" % (cart.x, cart.y))
