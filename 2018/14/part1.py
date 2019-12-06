#!/usr/local/bin/python3

input = 380621

recipes = [3, 7]
elf1_cursor = 0
elf2_cursor = 1
result_start_index = None

def add_recipe(recipe):
	global result_start_index
	recipes.append(recipe)
	if len(recipes) == input:
		result_start_index = len(recipes)

while True:
	sum = recipes[elf1_cursor] + recipes[elf2_cursor]
	if sum >= 10:
		add_recipe(int(sum/10))
		add_recipe(sum % 10)
	else:
		add_recipe(sum)
	if result_start_index is not None and len(recipes) >= result_start_index + 10:
		break
	elf1_cursor += 1 + recipes[elf1_cursor]
	elf2_cursor += 1 + recipes[elf2_cursor]
	elf1_cursor = elf1_cursor % len(recipes)
	elf2_cursor = elf2_cursor % len(recipes)	

print("".join(map(str, recipes[result_start_index:result_start_index + 10])))
