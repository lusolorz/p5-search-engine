#!/usr/bin/env -S python3 -u
"""Map 2."""
import sys

stopwords = []
with open("stopwords.txt", "r", encoding="utf-8") as temp:
    for line in temp:
        stopwords.append(line.strip())

for content in sys.stdin:
    content = content.split("\t")
    words = content[1].split()
    for word in words:
        if word not in stopwords:
            print(f"{content[0]}\t{word}")
