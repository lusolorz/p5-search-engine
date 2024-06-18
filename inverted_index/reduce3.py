#!/usr/bin/env -S python3 -u
"""Reduce 3."""
import sys
import itertools
import math

# answer should be term: tf-idf score, doc_id, tf fin doc, .....
# term 

#add these all to the same line:
def reduce_one_group(key, group):
    # get term frequency accross all docs here 
    # we can also add to a string and return that
    # and thne deal with it in map with a 4 for loop every four return 4 
    temp = list(group)
    all_docs = len(temp)
    """Reduce one group."""
    for line in group:
        doc_id = line.partition("\t")[2]
        nt = line.partition("\t")[4]
        idf_score = math.log10(all_docs/nt)
        print(f"{key}\t{idf_score}\t{doc_id}\t{nt}")
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