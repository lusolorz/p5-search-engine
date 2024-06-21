#!/usr/bin/env -S python3 -u
"""Reduce 5."""
import sys
import itertools

# answer should be term: tf-idf score, doc_id, tf fin doc, .....
# term
temp_group = []
term_dict = {}
# term:tf idf score, list of docs with weights
# add these all to the same line:


def reduce_one_group(key, group):
    """Reduce one group."""
    # Process each line in the group and store the relevant parts in tuples
    for line in group:
        parts = line.partition("\t")[2].split()
        idf = parts[0]
        term = parts[1]
        if term not in term_dict:
            term_dict[term] = []
        term_freq = parts[2]
        weight = parts[3]
        term_dict[term].append((idf, key, term_freq, weight))

    # Sort the list of tuples by the first element (term)


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)

    sorted_keys = sorted(term_dict.keys())

    # Print the sorted results
    for term in sorted_keys:
        line = f"{term} {term_dict[term][0][0]}"
        for item in term_dict[term]:
            doc_id = item[1]
            term_freq = item[2]
            weight = item[3]
            # line += f"{item}"
            line += f" {doc_id} {term_freq} {weight}"
        print(line)


if __name__ == "__main__":
    main()


# Passed in doc_id /t idf score " " tf  " " term
