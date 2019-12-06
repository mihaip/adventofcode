#!/usr/local/bin/python3

import collections
import re

INSTRUCTION_RE = re.compile("Step (\w+) must be finished before step (\w+) can begin.")
all_steps = set()

class Step:
    def __init__(self, name):
        self.name = name
        self.work_remaining = 60 + ord(name) - ord('A') + 1
        self.prerequisites = []
        self.worker = None

class Worker:
    def __init__(self):
        self.step = None

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
        if step.work_remaining == 0 or step.worker:
            continue
        has_incomplete_prequisites = False
        for prerequisite in step.prerequisites:
            prerequisite_step = steps[prerequisite]
            if prerequisite_step.work_remaining > 0:
                has_incomplete_prequisites = True
                break
        if has_incomplete_prequisites:
            continue
        return step
    return None

time = 0
WORKER_COUNT = 5
workers = [Worker() for i in range(WORKER_COUNT)]

while True:
    print("\n\niter, time so far: %d" % (time))
    available_workers = [w for w in workers if w.step is None]
    print("%d available workers" % len(available_workers))
    for worker in available_workers:
        worker.step = get_next_step()
        if worker.step:
            worker.step.worker = worker
    undone_steps = [w.step for w in workers if w.step]
    print("%d undone steps" % len(undone_steps))
    for step in undone_steps:
        print("  %s: %d work remaining" % (step.name, step.work_remaining))
    time_to_next_step_completion = min(undone_steps, key=lambda s:s.work_remaining).work_remaining
    print("%d time_to_next_step_completion" % time_to_next_step_completion)
    time += time_to_next_step_completion
    for worker in workers:
        if worker.step:
            worker.step.work_remaining -= time_to_next_step_completion
            if worker.step.work_remaining == 0:
                worker.step = None
    if all([w.step is None for w in workers]) and not get_next_step():
        break
print(time)
