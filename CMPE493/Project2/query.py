import json
import pickle

import trie

"""
    Imports the previously saved inverted index and trie structures, then processes
    the query given. It returns the list of document ids that satisfy the query.
    Arguments:
        query: String
    Returns:
        List<String> - The list of document ids that satisfy the query.
"""
def query_manager(query):
    inverted_index = dict()
    myTrie = trie.Trie()
    query = normalize_query(query)
    with open('inverted_index.json', 'r') as f:
        invertedIndex = json.load(f)
    with open('trie.pickle', 'rb') as f:
        myTrie = pickle.load(f)
    query_type = get_query_type(query)
    if query_type == 0: # Single-word query
        if query in invertedIndex:
            return sorted(list(map(int, invertedIndex[query])))
    else: # Prefix query
        candidate_words = myTrie.query(query[:-1])
        candidate_words.append(query[:-1])
        document_ids = list()
        for word in candidate_words:
            if word in invertedIndex:
                document_ids += invertedIndex[word]
        if len(document_ids) > 0:
            set_document_ids = set(document_ids)
            document_ids = list(set_document_ids)
            return sorted(list(map(int, document_ids)))
    return list()

"""
    Normalizes the given query word. It applies case-folding only on the query.
"""
def normalize_query(query):
    query = query.lower()
    return query

"""
    Determines whether the query is a single-word query or prefix query by looking at the final character.
    Returns:
        0 - Single-Word Query
        1 - Prefix Query
"""
def get_query_type(query):
    return 1 if query.endswith('*') else 0

"""
    Prints the result of a query.
    Arguments:
        query: String - Query
        result: List<String> - List of document ids that satisfy the query.
"""
def print_result(query, result):
    print("Query: {}\nDocument IDs: ".format(query),end='')
    if len(result) == 0:
        print()
        return
    for doc_id in result[:-1]:
        print(doc_id,end=' ')
    print(result[-1])