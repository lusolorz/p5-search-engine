#!/usr/bin/env -S python3 -u
"""Reduce 3."""
import sys
import itertools

# answer should be term: tf-idf score, doc_id, tf fin doc, .....


def reduce_one_group(key, group):
    # get term frequency accross all docs here 
    # all_docs = len(group)
    """Reduce one group."""
    # for line in group:
        # should be grouped by term now
        # get term frequency accross all docs here 
        # add the overall term freq 


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()