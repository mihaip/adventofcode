#!/usr/local/bin/python3

import sys

def is_safe_increasing(report):
    for i in range(len(report) - 1):
        item1 = report[i]
        item2 = report[i + 1]
        diff = item2 - item1
        if diff <= 3 and diff >= 1:
            # Do nothing
            pass
        else:
            return False
    return True

def is_safe_decreasing(report):
    for i in range(len(report) - 1):
        item1 = report[i]
        item2 = report[i + 1]
        diff = item2 - item1
        if diff >= -3 and diff <= -1:
            # Do nothing
            pass
        else:
            return False
    return True

def is_safe(report):
    if is_safe_decreasing(report) or is_safe_increasing(report):
        return True
    for i in range(len(report)):
        report2 = report[:i] + report[i + 1:]
        if is_safe_decreasing(report2) or is_safe_increasing(report2):
            return True
    return False

safe_count = 0

for line in sys.stdin.readlines():
    report = line.split()
    report = [int(item) for item in report]

    is_report_safe = is_safe(report)
    if is_report_safe:
        safe_count += 1

print(safe_count)
