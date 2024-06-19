#!/usr/bin/env -S python3 -u
"""Map 5."""
import sys
import re
import math


# Passed in term /t idf score " " doc  " " tf " " freq
# {term}\t{idf} {docid} {tf} {weight}

for content in sys.stdin:
    content = content.split("\t")
    term = content[0]
    second = content[1].split()
    idf = second[0]
    doc_id = second[1]
    term_freq = second[2]
    weight = second[3]

    print(f"{doc_id}\t{idf} {term} {term_freq} {weight}")
