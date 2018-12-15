#!/usr/local/bin/python3

import collections
import re

RECORD_RE = re.compile(r"\[(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})\] (.+)")
BEGINS_SHIFT_RE = re.compile(r"Guard #(\d+) begins shift")

lines = []
with open("input.txt") as f:
    lines = [l.strip() for l in f.readlines()]
lines = sorted(lines)

leaderboard = []
for i in range(60):
    leaderboard.append(collections.defaultdict(int))

current_guard_id = None
current_sleep_start = None

for line in lines:
    year, month, day, hour, minute, message = RECORD_RE.match(line).groups()
    year, month, day, hour, minute = map(int, [year, month, day, hour, minute])
    begins_shift_match = BEGINS_SHIFT_RE.match(message)
    if begins_shift_match:
        current_guard_id = begins_shift_match.group(1)
    elif message == "falls asleep":
        assert current_sleep_start == None
        current_sleep_start = minute
    elif message == "wakes up":
        assert current_sleep_start is not None
        for i in range(current_sleep_start, minute):
            leaderboard[i][current_guard_id] += 1
        current_sleep_start = None
    else:
        assert False, "Unexpected message: %s" % message

max_sleep_count = None
max_sleep_minute = None
max_sleep_guard = None

for minute, guard_counts in enumerate(leaderboard):
    if not guard_counts:
        continue
    sleepiest_guard = max(guard_counts.keys(), key=lambda id: guard_counts[id])
    sleep_count = guard_counts[sleepiest_guard]
    if max_sleep_count is None or sleep_count > max_sleep_count:
        max_sleep_count = sleep_count
        max_sleep_minute = minute
        max_sleep_guard = sleepiest_guard

print("guard %s was sleepiest at minute %d" % (max_sleep_guard, max_sleep_minute))
