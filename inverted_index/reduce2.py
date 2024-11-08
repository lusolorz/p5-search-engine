#!/usr/bin/env -S python3 -u
"""Reduce 2."""
import sys
import itertools


# Reduce to term and frequency of that term across all docs

# doc1 eecs
# doc1 sucks
# doc1 play
# doc1 eecs

# doc2 eecs
# doc2 sucks
# doc2 eecs

# after reduce
# eecs 2
# sucks 1
# play 1
# eecs 2
# sucks 1


def reduce_one_group(key, group):
    """Reduce one group."""
    temp_dict = {}
    num_words_in_doc = 0
    for line in group:
        term = line.partition("\t")[2].strip()
        if term not in temp_dict:
            temp_dict[term] = 1
        else:
            temp_dict[term] += 1
        num_words_in_doc += 1
    for term, value in temp_dict.items():
        print(f"{term}\t{key} {value}")

    # term /tab how many times that term has appeared in all docs


def keyfunc2(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc2):
        reduce_one_group(key, group)
    # Now we're gonna have terms associated with how many times
    # they appear in each doc and the doc_ids for each


if __name__ == "__main__":
    main()
