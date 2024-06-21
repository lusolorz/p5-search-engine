#!/usr/bin/env -S python3 -u
"""Reduce 3."""
import sys
import itertools
import math


# Answer should be term: tf-idf score, doc_id, tf fin doc, .....
# term


# Add these all to the same line:
def reduce_one_group(key, group):
    """Reduce one group."""
    # get term frequency accross all docs here
    # we can also add to a string and return that
    # and thne deal with it in map with a 4 for loop every four return 4
    temp_group = list(group)
    terms_all_docs = len(temp_group)
    with open('total_document_count.txt', encoding="utf-8") as temp:
        num_docs = temp.readline().strip()

    for line in temp_group:
        doc_id = line.partition("\t")[2].split()[0]
        freq = line.partition("\t")[2].split()[1]
        idf_score = math.log10(int(num_docs)/terms_all_docs)
        print(f"{key}\t{idf_score} {doc_id} {freq}")
        # should be grouped by term now
        # get term frequency accross all docs here
        # add the overall term freq


def keyfunc3(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc3):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()
