#!/usr/bin/env -S python3 -u
"""Reduce 1."""
import sys
import itertools
import re


def reduce_one_group(key, group):
    """Reduce one group."""
    content = ""
    for line in group:
        line = re.sub(r"[^a-zA-Z0-9 ]+", "", line)
        line = line.casefold()
        content += line
    print(f"{key}\t{content}")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()
