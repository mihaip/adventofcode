#!/usr/local/bin/python3

input = [3, 8, 0, 6, 2, 1]

recipes = [3, 7]
elf1_cursor = 0
elf2_cursor = 1
found_match = False

def add_recipe(recipe):
	global found_match
	recipes.append(recipe)
	if recipe == input[-1] and recipes[-2] == input[-2] and all([i == j for i, j in zip(recipes[-len(input):], input)]):
		found_match = True

while not found_match:
	sum = recipes[elf1_cursor] + recipes[elf2_cursor]
	if sum >= 10:
		add_recipe(int(sum/10))
		if found_match:
			break
		add_recipe(sum % 10)
	else:
		add_recipe(sum)
	elf1_cursor += 1 + recipes[elf1_cursor]
	elf2_cursor += 1 + recipes[elf2_cursor]
	elf1_cursor = elf1_cursor % len(recipes)
	elf2_cursor = elf2_cursor % len(recipes)	

print(len(recipes) - len(input))
