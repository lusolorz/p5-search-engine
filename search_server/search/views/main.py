from flask import Blueprint, request, render_template
import requests
import concurrent.futures
from search.config import SEARCH_INDEX_SEGMENT_API_URLS
from search.model import get_document_details
import search

# search_bp = Blueprint('search', __name__)

@search.app.route('/')
def search():
    query = request.args.get('q', '')
    weight = request.args.get('w', 0.5)
    
    if query:
        results = get_search_results(query, weight)
    else:
        results = []

    return render_template('index.html', results=results)

def get_search_results(query, weight):
    payload = {'q': query, 'w': weight}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(requests.get, url, params=payload) for url in SEARCH_INDEX_SEGMENT_API_URLS]
        responses = [future.result() for future in concurrent.futures.as_completed(futures)]

    combined_results = []
    for response in responses:
        if response.status_code == 200:
            combined_results.extend(response.json())

    combined_results = sorted(combined_results, key=lambda x: x['score'], reverse=True)[:10]
    detailed_results = [get_document_details(res['docid']) for res in combined_results]
    return detailed_results
