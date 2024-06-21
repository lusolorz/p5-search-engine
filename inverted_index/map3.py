#!/usr/bin/env -S python3 -u
"""Map 3."""
import sys

# Passed in term /t doc /t freq in doc
for content in sys.stdin:
    content = content.split("\t")
    term = content[0]
    doc = content[1].split()[0]
    term_freq = content[1].split()[1]
    # term = key
    # line = term frequncy across all docs
    # with open ('total_document_count.txt') as temp:
    #     num_docs =  temp.readline().strip()
    # idf_calc = math.log10(float(num_docs)/float(line))
    print(f"{term}\t{doc} {term_freq}")
