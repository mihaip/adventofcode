#!/usr/local/bin/python3

import collections
import re

INSTRUCTION_RE = re.compile("Step (\w+) must be finished before step (\w+) can begin.")
all_steps = set()

class Step:
    def __init__(self, name):
        self.name = name
        self.completed = False
        self.prerequisites = []

steps = {}

with open("input.txt") as f:
    for line in f.readlines():
        prerequisite, step = INSTRUCTION_RE.match(line).groups()
        if prerequisite not in steps:
            steps[prerequisite] = Step(prerequisite)
        if step not in steps:
            steps[step] = Step(step)
        steps[step].prerequisites.append(prerequisite)

ordered_steps = collections.OrderedDict()
for step_name in sorted(steps.keys()):
    ordered_steps[step_name] = steps[step_name]

def get_next_step():
    for step in ordered_steps.values():
        if step.completed:
            continue
        has_incomplete_prequisites = False
        for prerequisite in step.prerequisites:
            prerequisite_step = steps[prerequisite]
            if not prerequisite_step.completed:
                has_incomplete_prequisites = True
                break
        if has_incomplete_prequisites:
            continue
        return step
    return None

execution_order = []
while True:
    step = get_next_step()
    if not step:
        break
    step.completed = True
    execution_order.append(step)
print("".join([s.name for s in execution_order]))
