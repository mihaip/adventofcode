#!/usr/local/bin/python3

import re

RECORD_RE = re.compile(r"\[(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})\] (.+)")
BEGINS_SHIFT_RE = re.compile(r"Guard #(\d+) begins shift")

lines = []
with open("input.txt") as f:
    lines = [l.strip() for l in f.readlines()]
lines = sorted(lines)

guard_records = dict()
current_guard_record = None
current_sleep_start = None
sleepiest_guard = None

class GuardRecord:
    def __init__(self, id):
        self.id = id
        self.sleep_counts = [0] * 60
        self.total_sleep_minutes = 0

    def add_sleep(self, start, end):
        for i in range(start, end):
            self.sleep_counts[i] += 1
        self.total_sleep_minutes += end - start

    def get_sleepiest_minute(self):
        return max(range(len(self.sleep_counts)), key= lambda i: self.sleep_counts[i])

for line in lines:
    year, month, day, hour, minute, message = RECORD_RE.match(line).groups()
    year, month, day, hour, minute = map(int, [year, month, day, hour, minute])
    begins_shift_match = BEGINS_SHIFT_RE.match(message)
    if begins_shift_match:
        id = begins_shift_match.group(1)
        if id in guard_records:
            current_guard_record = guard_records[id]
        else:
            current_guard_record = GuardRecord(id)
            guard_records[id] = current_guard_record
    elif message == "falls asleep":
        assert current_sleep_start == None
        current_sleep_start = minute
    elif message == "wakes up":
        assert current_sleep_start is not None
        current_guard_record.add_sleep(current_sleep_start, minute)
        current_sleep_start = None
        if sleepiest_guard is None or sleepiest_guard.total_sleep_minutes < current_guard_record.total_sleep_minutes:
            sleepiest_guard = current_guard_record
    else:
        assert False, "Unexpected message: %s" % message

print("sleepiest guard: %s, sleepiest at minute %d" % (sleepiest_guard.id, sleepiest_guard.get_sleepiest_minute()))
