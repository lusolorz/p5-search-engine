#!/usr/bin/env -S python3 -u
"""Map 4."""
import sys
import re
import math


# Passed in term /t idf score " " doc  " " tf " " freq


for content in sys.stdin:
    content = content.split("\t")
    term = content[0]
    idf = content[1].split()[0]
    doc_id = content[1].split()[1]
    tf = content[1].split()[2]
    term_freq = content[1].split()[3]

    print(f"{doc_id}\t{idf} {tf} {term} {term_freq}")
