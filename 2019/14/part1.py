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

store = collections.defaultdict(int)

def produce(name, quantity):
    existing_quantity = store[name]
    # print("produce(%s, %d, existing_quantity=%d)" % (name, quantity, existing_quantity))
    if quantity <= existing_quantity:
        print("  %s: had too much" % name)
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
    while produced_quantity < quantity:
        # print("  %s: produced_quantity=%d ore_count=%d" % (name, produced_quantity, ore_count))
        for input_quantity, input_name in reaction.inputs:
            # print("  %s: checking input %s %d" % (name, input_name, input_quantity))
            ore_count += produce(input_name, input_quantity)
        produced_quantity += reaction.output_quantity
    if produced_quantity > quantity:
        # print("  %s: %d extra" % (name, produced_quantity - quantity))
        store[name] += produced_quantity - quantity
    # print("  %s: return %d" % (name, ore_count))
    return ore_count

ore_count = produce("FUEL", 1)
print("%d ORE to produce 1 unit of FUEL" % ore_count)
