#!/usr/bin/env -S python3 -u
"""Reduce 4."""
import sys
import itertools

# answer should be term: tf-idf score, doc_id, tf fin doc, .....
# term
dict_terms = {}
# term:tf idf score, list of docs with weights
# add these all to the same line:


def reduce_one_group(key, group):
    """Reduce one group."""
    # passed in doc_id /t idf score " " tf  " " term

    # get term frequency accross all docs here
    # we can also add to a string and return that
    # and thne deal with it in map with a 4 for loop every four return 4
    sum1 = 0
    term = ""

    term_to_freq_to_doc = {}
    for line in group:
        # doc_id = line.partition("\t")[0]
        idf_score = line.partition("\t")[2].split()[0]
        term = line.partition("\t")[2].split()[1]
        term_freq = line.partition("\t")[2].split()[2]
        if term not in dict_terms:
            dict_terms[term] = {}
            dict_terms[term]['idf_score'] = idf_score
            dict_terms[term]['docs'] = {}
        sum1 += ((float(idf_score) * float(term_freq)) ** 2)
        if term not in term_to_freq_to_doc:
            term_to_freq_to_doc[term] = term_freq
    # weight = math.sqrt(sum)
    weight = sum1
    for term, freq_to_doc in term_to_freq_to_doc.items():
        dict_terms[term]['docs'][key] = {}
        dict_terms[term]['docs'][key]['weight'] = weight
        dict_terms[term]['docs'][key]['term_freq'] = freq_to_doc

    # should be grouped by term now
    # get term frequency accross all docs here
    # add the overall term freq
    # we need to return:
    # term /t idf score for that term " " docid0 " " tf0 " " docid1 " " tf1 "
    # doc_id term


def keyfunc4(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc4):
        reduce_one_group(key, group)
    for term, term_data in dict_terms.items():
        idf_score = term_data['idf_score']

        for doc, doc_data in term_data['docs'].items():
            term_freq = doc_data['term_freq']
            weight = doc_data['weight']

            print(f"{term}\t{idf_score} {doc} {term_freq} {weight}")


if __name__ == "__main__":
    main()


# Passed in doc_id /t idf score " " tf  " " term
