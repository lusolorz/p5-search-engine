"""REST APT."""
import os
import re
import math
import flask
# from index import app
import index


inverted_index = {}
pagerank = {}
stopwords = set()
docs_to_weights = {}


def load_index():
    """Load the inverted index, PageRank, and stopwords."""
    global inverted_index, pagerank, stopwords

    # Load the inverted index
    inverted_index_path = os.path.join(
        "./index_server/index/inverted_index", index.app.config["INDEX_PATH"]
    )
    with open(inverted_index_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.split()
            word = line[0]
            inverted_index[word] = {}
            # 00000000 2.7686381012476144 1345509 1 6307.358583064987
            # ... 8900538 1 140550.31899129925 9315114 2 212561.83132016915
            inverted_index[word]['idf'] = float(line[1])
            inverted_index[word]['docs'] = {}
            i = 2
            while i < len(line):
                doc = line[i]
                inverted_index[word]['docs'][line[i]] = {}
                i += 1
                inverted_index[word]['docs'][doc]['term_freq'] = int(line[i])
                i += 1
                inverted_index[word]['docs'][doc]['weight'] = float(line[i])
                i += 1

    # Load the PageRank values
    pagerank_path = os.path.join("./index_server/index/pagerank.out")
    with open(pagerank_path, 'r', encoding='utf-8') as f:
        for line in f:
            doc, rank = line.split(',')
            pagerank[doc] = float(rank)

    # Load the stopwords
    stopwords_path = os.path.join("./index_server/index/stopwords.txt")
    with open(stopwords_path, 'r', encoding='utf-8') as f:
        stopwords = set(word.strip() for word in f)


# GET /api/v1/
@index.app.route('/api/v1/', methods=['GET'])
def get_api_v1():
    """Return API v1."""
    # Create the context
    context = {
        "hits": "/api/v1/hits/",
        "url": "/api/v1/"
    }
    # Return the context
    return flask.jsonify(**context)


# GET /api/v1/hits/
@index.app.route('/api/v1/hits/', methods=['GET'])
def get_api_v1_hits():
    """Return API v1 hits."""
    w = 0.5
    if flask.request.args.get('w'):
        w = float(flask.request.args.get('w'))
    query = flask.request.args.get('q')
    query = re.sub(r"[^a-zA-Z0-9 ]+", "", query)
    query = query.casefold()
    query = query.split()
    temp_list_for_query = []
    for word in query:
        if word not in stopwords and word in inverted_index:
            temp_list_for_query.append(word)
        elif word not in inverted_index and word not in stopwords:
            content = {}
            content['hits'] = []
            return flask.jsonify(content)
    query = temp_list_for_query

    query_tfidf_vec = compute_query_vector(query)

    # for loop for all docs containg words in query:
    dict_of_docs_with_vectors = get_docs_with_all_words_in_query(query)

    query_tfidf_vec_magnitude = 0
    for point in query_tfidf_vec:
        query_tfidf_vec_magnitude += point ** 2
    query_tfidf_vec_magnitude = math.sqrt(query_tfidf_vec_magnitude)

    # compute numerator aka dot product of vectors
    content = {}
    content['hits'] = []

    # print(len(dict_of_docs_with_vectors))
    count = 0
    for doc, doc_vector in dict_of_docs_with_vectors.items():
        dot_product = 0
        if len(doc_vector) != len(query_tfidf_vec):
            break
        for i, value in enumerate(query_tfidf_vec):
            if doc_vector[i] == 0:
                dot_product = 0
                count += 1
                break
            dot_product += value * doc_vector[i]
        if dot_product != 0:
            normalization = (
                dot_product / (
                    query_tfidf_vec_magnitude * math.sqrt(docs_to_weights[doc])
                )
            )
            # score = w * pagerank.get(doc, 0.0) + (1 - w) * normalization
            content_doc_dict = {
                'docid': int(doc),
                'score': w * pagerank.get(doc, 0.0) + (1 - w) * normalization
            }
            content['hits'].append(content_doc_dict)

    content['hits'] = sorted(
        content['hits'], key=lambda x: x['score'], reverse=True
    )

    return flask.jsonify(content)

    # for doc in dict_of_docs_with_vectors:
    #     dot_product = 0
    #     # print(str(len(query_tfidf_vec)))
    #     # print(len(dict_of_docs_with_vectors[doc]))
    #     if len(dict_of_docs_with_vectors[doc]) != len(query_tfidf_vec):
    #         break
    #     for i in range(len(query_tfidf_vec)):
    #         if dict_of_docs_with_vectors[doc][i] == 0:
    #             dot_product = 0
    #             count += 1
    #             # print(doc)
    #             break
    #         dot_product += (
    #             query_tfidf_vec[i] * dict_of_docs_with_vectors[doc][i]
    #         )
    #     # print(docs_to_weights)
    #     if dot_product != 0:
    #         normalization = dot_product/(
    #             query_tfidf_vec_magnitude * math.sqrt(docs_to_weights[doc])
    #         )
    #         # score = w * pagerank[doc] + (1-w) * normalization
    #         content_doc_dict = {}
    #         content_doc_dict['docid'] = int(doc)
    #         content_doc_dict['score'] = (
    #             w * pagerank[doc] + (1-w) * normalization
    #         )
    #         content['hits'].append(content_doc_dict)
    # content['hits'] = sorted(
    #     content['hits'], key=lambda x: x['score'], reverse=True
    # )
    # # print(content['hits'])

    # return flask.jsonify(content)


def compute_query_vector(query):
    """Compute the query vector."""
    q_tf = {}
    for word in query:
        if word not in q_tf:
            q_tf[word] = 1
        else:
            q_tf[word] += 1

    q_tf_idf_vector = []
    for word, count in q_tf.items():
        q_tf_idf_vector.append(count * inverted_index[word]['idf'])

    return q_tf_idf_vector


def get_docs_with_all_words_in_query(query):
    """Retreive the docs that have all the words in a query."""
    dict_of_doc_vectors = {}
    for word in query:
        for doc in inverted_index[word]['docs']:
            # print(f"Processing doc: {doc} for word: {word}")
            # print(f"Available docs in index: {inverted_index[word]['docs']}")
            if doc not in docs_to_weights:
                # print(docs_to_weights)
                if doc in inverted_index[word]['docs']:
                    docs_to_weights[doc] = (
                        inverted_index[word]['docs'][doc]['weight']
                    )
            if doc not in dict_of_doc_vectors:
                dict_of_doc_vectors[doc] = []
                for word in query:
                    if doc in inverted_index[word]['docs']:
                        tf = inverted_index[word]['docs'][doc]['term_freq']
                        idf = inverted_index[word]['idf']
                        dict_of_doc_vectors[doc].append(
                            tf*idf
                        )
                    else:
                        dict_of_doc_vectors[doc].append(0)
    return dict_of_doc_vectors

    # list_of_docs.append(
    #     (
    #         doc,
    #         inverted_index[word][doc]['term_freq'],
    #         inverted_index[word][doc]['weight']
    #     )
    # )

    # for word in query:
    #     dict_of_doc_vectors[]
    # for word in query:
    #     for doc in inverted_index[word]['docs']:
    #         dict_of_doc_vectors[word] = { doc : [] }
    # for word in dict_of_doc_vectors:
    #     for doc in dict_of_doc_vectors[word]:
    #         if doc not in docs_to_weights:
    #             docs_to_weights[doc] = (
    #                 inverted_index[word]['docs'][doc]['weight']
    #             )
    #         for word in query:
    #             if doc in inverted_index[word]['docs']:
    #                 dict_of_doc_vectors[word][doc].append(
    #                     inverted_index[word]['docs'][doc]['term_freq']*inverted_index[word]['idf']
    #                 )
    #             else:
    #                 dict_of_doc_vectors[word][doc].append(0)
