#!/usr/bin/env -S python3 -u
"""Map 2."""
import sys
import re


for doc_id, content in sys.stdin:
    content = content.split(" ")
    for word in content:
        print(f"{doc_id}\t{word}")
