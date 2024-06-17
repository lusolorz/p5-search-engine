#!/usr/bin/env -S python3 -u
"""Map 1."""
import sys
import hashlib
import bs4


# Map each term to a document 


ALGORITHM = 'sha512'


# Parse one HTML document at a time.  Note that this is still O(1) memory
# WRT the number of documents in the dataset.
HTML = ""
for doc in sys.stdin:
    # Assume well-formed HTML docs:
    # - Starts with <!DOCTYPE html>
    # - End with </html>
    # - Contains a trailing newline
    if "<!DOCTYPE html>" in doc:
        HTML = doc
    else:
        HTML += doc

    # If we're at the end of a document, parse
    if "</html>" not in doc:
        continue

    # Configure Beautiful Soup parser
    soup = bs4.BeautifulSoup(HTML, "html.parser")

    # Parse content from document
    # get_text() will strip extra whitespace and
    # concatenate content, separated by spaces
    element = soup.find("html")
    content = element.get_text(separator=" ", strip=True)
    # Remove extra newlines
    content = content.replace("\n", "")

    # Calculate doc_id by hashing the document content
    hash_obj = hashlib.new(ALGORITHM)
    hash_obj.update(content.encode("utf-8"))
    doc_id = hash_obj.hexdigest()
    # Mod by 10^7 to limit the length of the doc_id
    doc_id = int(doc_id, 16) % (10**7)
    
    # FIXME Map 1 output.  Emit one line for each document, including the doc
    # ID and document content (You will need them later!)
    print(f"{doc_id}\t{content}")
