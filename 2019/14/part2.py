#!/usr/local/bin/python3

import collections

reactions_by_output = {}
class Reaction:
    def __init__(self, inputs, output_name, output_quantity):
        self.inputs = inputs
        self.output_name = output_name
        self.output_quantity = output_quantity

def parse_str(s):
    quantity_str, name = s.split(" ")
    return int(quantity_str), name

with open("input.txt") as f:
    for line in f:
        line = line.strip()
        inputs_str, output_str = line.strip().split(" => ")
        output_quantity, output_name = parse_str(output_str)
        if output_name in reactions_by_output:
            raise Exception("Already had a reaction that generated %s" % output_name)
        reactions_by_output[output_name] = Reaction(
            inputs=list(map(parse_str, inputs_str.split(", "))),
            output_name=output_name,
            output_quantity=output_quantity)

def produce(name, quantity, store):
    existing_quantity = store[name]
    # print("produce(%s, %d, existing_quantity=%d)" % (name, quantity, existing_quantity))
    if quantity <= existing_quantity:
        # print("  %s: had too much" % name)
        store[name] -= quantity
        return 0
    quantity -= existing_quantity
    store[name] = 0
    if name == "ORE":
        # print("  ORE, returning %d" % quantity)
        return quantity
    reaction = reactions_by_output.get(name)
    if not reaction:
        raise Exception("Nothing produces %s" % name)
    produced_quantity = 0
    ore_count = 0
    multiplier = quantity // reaction.output_quantity
    if multiplier > 1:
        # print("  %s: bulk with multiplier %d" % (name, multiplier))
        for input_quantity, input_name in reaction.inputs:
            # print("  %s: checking input %s %d" % (name, input_name, input_quantity))
            ore_count += produce(input_name, input_quantity * multiplier, store)
        produced_quantity += reaction.output_quantity * multiplier
    while produced_quantity < quantity:
        # print("  %s: produced_quantity=%d ore_count=%d" % (name, produced_quantity, ore_count))
        for input_quantity, input_name in reaction.inputs:
            # print("  %s: checking input %s %d" % (name, input_name, input_quantity))
            ore_count += produce(input_name, input_quantity, store)
        produced_quantity += reaction.output_quantity
    if produced_quantity > quantity:
        # print("  %s: %d extra" % (name, produced_quantity - quantity))
        store[name] += produced_quantity - quantity
    # print("  %s: return %d" % (name, ore_count))
    return ore_count

MAX_ORE_COUNT = 1000000000000
current_fuel = 1
previous_fuel = None

while True:
    current_ore_count = produce("FUEL", current_fuel, store=collections.defaultdict(int))
    print("%d to produce %d fuel" % (current_ore_count, current_fuel))
    if current_ore_count < MAX_ORE_COUNT:
        previous_fuel = current_fuel
        current_fuel *= 2
    elif current_fuel == previous_fuel + 1:
        print("answer: %d" % previous_fuel)
        break
    else:
        current_fuel = (previous_fuel + current_fuel) // 2
