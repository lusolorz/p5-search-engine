#!/usr/bin/env -S python3 -u
"""Map 0."""
import sys


for line in sys.stdin:
    # Assuming each line reps a doc & contains '<!DOCTYPE html>' string.
    if '<!DOCTYPE html>' in line:
        print("count\t1")
