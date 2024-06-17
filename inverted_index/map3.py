#!/usr/bin/env -S python3 -u
"""Map 3."""
import sys
import re
import math

#passed in term /t doc /t freq in doc

for term, doc, freq in sys.stdin:
    # term = key
    # line = term frequncy across all docs
    # with open ('total_document_count.txt') as temp:
    #     num_docs =  temp.readline().strip()
    # idf_calc = math.log10(float(num_docs)/float(line))
    temp = doc + "  " + freq
    print(f"{term}\t{temp}")
