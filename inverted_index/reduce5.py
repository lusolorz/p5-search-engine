#!/usr/bin/env -S python3 -u
"""Reduce 5."""
import sys
import itertools
import math

# answer should be term: tf-idf score, doc_id, tf fin doc, .....
# term 
dict_terms = {}
#term:tf idf score, list of docs with weights 
#add these all to the same line:
def reduce_one_group(key, group):
    """Reduce one group."""
    # passed in doc_id /t idf score " " tf  " " term

    # get term frequency accross all docs here 
    # we can also add to a string and return that
    # and thne deal with it in map with a 4 for loop every four return 4 
    for line in group:
    #     # doc_id = line.partition("\t")[0]
        idf = line.partition("\t")[2].split()[0]
        doc_id = line.partition("\t")[2].split()[1]
        term_freq = line.partition("\t")[2].split()[2]
        weight = line.partition("\t")[2].split()[3]
        print(f"{key}\t{idf} {doc_id} {term_freq} {weight}")
    
    

def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()


# Passed in doc_id /t idf score " " tf  " " term
