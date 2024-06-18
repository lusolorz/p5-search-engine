#!/usr/bin/env -S python3 -u
"""Reduce 4."""
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
    sum = 0
    term = ""

    term_to_freq_to_doc = {}
    for line in group:
    #     # doc_id = line.partition("\t")[0]
        idf_score = line.partition("\t")[2].split()[0]
        tf_score = line.partition("\t")[2].split()[1]
        term = line.partition("\t")[2].split()[2]
        term_freq = line.partition("\t")[2].split()[3]
        if term not in dict_terms:
            dict_terms[term] = {}
            dict_terms[term]['idf_score'] = idf_score
            dict_terms[term]['docs'] = {}
        sum += (float(idf_score) * float(term_freq)) ** 2
        if term not in term_to_freq_to_doc:
            term_to_freq_to_doc[term] = term_freq
    weight = math.sqrt(sum) * 100
    for term in term_to_freq_to_doc:
        dict_terms[term]['docs'][key] = {}
        dict_terms[term]['docs'][key]['weight'] = weight
        dict_terms[term]['docs'][key]['term_freq'] = term_to_freq_to_doc[term]

        # should be grouped by term now
        # get term frequency accross all docs here 
        # add the overall term freq 
    # we need to return:
    # term /t idf score for that term " " docid0 " " tf0 " " docid1 " " tf1 " " ....
    # doc_id term


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)
    for term in dict_terms:
        for doc in dict_terms[term]['docs']:
            print(f"{term}\t{dict_terms[term]['idf_score']} {doc} {dict_terms[term]['docs'][doc]['term_freq']} {dict_terms[term]['docs'][doc]['weight']}")

if __name__ == "__main__":
    main()


# Passed in doc_id /t idf score " " tf  " " term
