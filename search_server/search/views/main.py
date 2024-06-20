"""Views."""
from flask import request, render_template
import requests
import concurrent.futures
from search.config import SEARCH_INDEX_SEGMENT_API_URLS
from search.model import get_document_details
import search
import heapq
import threading

@search.app.route('/')
def search():
    query = request.args.get('q', '')
    weight = request.args.get('w', 0.5)
    
    if query:
        results = get_search_results(query, weight)
    else:
        results = []

    return render_template('index.html', results=results)

def get_request(query, weight, url, all_results):
    full_url = f"{url}?q={query}&w={weight}"
    try:
        r = requests.get(full_url)
        r.raise_for_status()  # Check if the request was successful
        r = r.json()['hits']
        
        # Extract (docid, score) tuples for each result and store in a list
        results = [(result['docid'], result['score']) for result in r]
        all_results.append(results)
    except requests.exceptions.RequestException as e:
        # Log the exception and continue
        print(f"Error fetching from {full_url}: {e}")


def get_search_results(og_query, weight):
    payload = {'q': og_query, 'w': weight}

    query = ""

    # Split the original query into words
    words = og_query.split()

    # Iterate through each word
    for i, word in enumerate(words):
        # Add the word to the query string
        query += word
        # Add a '+' if it's not the last word
        if i < len(words) - 1:
            query += '+'

    all_results = []

    threads = {
        "thread1": threading.Thread(target=get_request, args = (query, weight, SEARCH_INDEX_SEGMENT_API_URLS[0], all_results)),
        "thread2": threading.Thread(target=get_request, args = (query, weight, SEARCH_INDEX_SEGMENT_API_URLS[1], all_results)),
        "thread3": threading.Thread(target=get_request, args = (query, weight, SEARCH_INDEX_SEGMENT_API_URLS[2], all_results))
    }
    for thread in threads:
        threads[thread].start()

    for thread in threads:
        threads[thread].join()

    # Use heapq.merge to merge all results, sorted by score
    # heapq.merge expects multiple sorted inputs, so we ensure each results list is sorted
    merged_results = heapq.merge(*[sorted(results, key=lambda x: x[1], reverse=True) for results in all_results], key=lambda x: x[1], reverse=True)

    # Convert the merged_results iterator to a list if needed
    merged_results = list(merged_results)

    # Loop through each URL to get the results

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


# import requests
# import concurrent.futures
# import heapq
# from flask import current_app as app
# from .model import get_db

# def fetch_results(url, payload):
#     try:
#         response = requests.get(url, params=payload)
#         if response.status_code == 200:
#             return response.json()
#     except requests.exceptions.RequestException as e:
#         app.logger.error(f"Error fetching from Index server: {e}")
#     return []

# def get_search_results(query, weight):
#     payload = {'q': query, 'w': weight}

#     # Making concurrent requests to all Index servers
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         futures = [executor.submit(fetch_results, url, payload) for url in app.config['SEARCH_INDEX_SEGMENT_API_URLS']]
#         responses = []
#         for future in concurrent.futures.as_completed(futures):
#             responses.extend(future.result())

#     # Combine results from all responses using heapq.merge()
#     combined_results = heapq.merge(*responses, key=lambda x: -x['score'])

#     # Fetch document details for the top 10 results
#     detailed_results = []
#     for result in combined_results:
#         if len(detailed_results) >= 10:
#             break
#         doc_details = get_document_details(result['docid'])
#         if doc_details:
#             detailed_results.append(doc_details)

#     return detailed_results