"""Views."""
import heapq
import threading
import requests
from flask import request, render_template
from search.config import SEARCH_INDEX_SEGMENT_API_URLS
# from search.model import get_document_details
import search

@search.app.route('/')
def search_for_docs():
    """Search for documents."""
    query = request.args.get('q', '')
    weight = request.args.get('w', 0.5)

    if query:
        results = get_search_results(query, weight)
    else:
        results = []

    return render_template('index.html', results=results)

def get_request(query, weight, url, all_results):
    """GET request."""
    full_url = f"{url}?q={query}&w={weight}"
    try:
        r = requests.get(full_url, timeout=10)
        r.raise_for_status()  # Check if the request was successful
        r = r.json()['hits']

        # Extract (docid, score) tuples for each result and store in a list
        results = [(result['docid'], result['score']) for result in r]
        all_results.append(results)
    except requests.exceptions.RequestException as e:
        # Log the exception and continue
        print(f"Error fetching from {full_url}: {e}")


# def get_search_results(og_query, weight):
#     """Get search results."""
#     # payload = {'q': og_query, 'w': weight}
#     query = ""

#     # Split the original query into words
#     words = og_query.split()

#     # Iterate through each word
#     for i, word in enumerate(words):
#         # Add the word to the query string
#         query += word
#         # Add a '+' if it's not the last word
#         if i < len(words) - 1:
#             query += '+'

#     all_results = []

#     threads = {
#         "thread1": threading.Thread(
#             target=get_request, args = (
#                 query, weight, SEARCH_INDEX_SEGMENT_API_URLS[0], all_results
#             )
#         ),
#         "thread2": threading.Thread(
#             target=get_request, args = (
#                 query, weight, SEARCH_INDEX_SEGMENT_API_URLS[1], all_results
#             )
#         ),
#         "thread3": threading.Thread(
#             target=get_request, args = (
#                 query, weight, SEARCH_INDEX_SEGMENT_API_URLS[2], all_results
#             )
#         )
#     }

#     for thread in threads:
#         threads[thread].start()
#     for thread in threads:
#         threads[thread].join()

#     # Use heapq.merge to merge all results, sorted by score
#     # heapq.merge expects multiple sorted inputs, so we ensure each results list is sorted
#     merged_results = heapq.merge(
#         *[
#             sorted(results, key=lambda x: x[1], reverse=True) for results in all_results
#         ], key=lambda x: x[1], reverse=True)

#     # Convert the merged_results iterator to a list if needed
#     merged_results = list(merged_results)

#     # Loop through each URL to get the results

#     # Return the merged results
#     return merged_results[:9]


def get_search_results(og_query, weight):
    """Get search results."""
    query = "+".join(og_query.split())

    all_results = []

    threads = {}
    for index, url in enumerate(SEARCH_INDEX_SEGMENT_API_URLS):
        thread_name = f"thread{index + 1}"
        threads[thread_name] = threading.Thread(
            target=get_request, args=(query, weight, url, all_results)
        )
        threads[thread_name].start()

    for thread in threads.values():
        thread.join()

    # Use heapq.merge to merge all results, sorted by score
    sorted_results = [sorted(results, key=lambda x: x[1], reverse=True) for results in all_results]
    merged_results = heapq.merge(*sorted_results, key=lambda x: x[1], reverse=True)

    # Convert the merged_results iterator to a list if needed
    merged_results = list(merged_results)

    return merged_results[:9]


# r = requests.get('https://api.github.com/user')


# {
#     "hits": [
#         {
#             "docid": 8231931,
#             "score": 0.4021905074266496
#         },
#         {
#             "docid": 8058999,
#             "score": 0.14054933346325524
#         },
#         ...
#     ]
# # }
