import os
import sys
import json
import pickle

import preprocessing, inverted_index, trie, query

is_inverted_index_found = inverted_index.search_inverted_index(file_name='inverted_index.json')
is_trie_found = trie.search_trie(file_name='trie.pickle')

invertedIndex = dict()
myTrie = trie.Trie()

# The program has two pathways based on whether the required data structures are constructed before.
if not(is_inverted_index_found and is_trie_found):
    # Applies the following operations if any of the data structures required is missing:
    #   1. Parsing the Reuters21578 dataset
    #   2. Tokenization
    #   3. Normalization
    #   4. Construction of Inverted Index & Trie
    # Then, the program saves the constructed data structures, namely inverted index and trie.
    try:
        os.remove('inverted_index.json')
        print('Deleting old inverted_index.json')
    except OSError:
        pass
    try:
        os.remove('trie.pickle')
        print('Deleting old trie.pickle')
    except OSError:
        pass
    print("Progressing: Parsing the Reuters21578 dataset")
    articles = preprocessing.get_articles(file_name_template='reuters21578/reut2-')
    print("Progressing: Tokenization")
    tokenized_articles = preprocessing.tokenize(articles)
    print("Progressing: Normalization")
    normalized_articles = preprocessing.normalize(tokenized_articles)
    print("Progressing: Construction of Inverted Index")
    invertedIndex = inverted_index.construct_inverted_index(normalized_articles)
    with open('inverted_index.json', 'w') as f: # Save
        json.dump(invertedIndex, f)
    print("Progressing: Construction of Trie")
    myTrie = trie.Trie()
    for word in invertedIndex.keys():
        myTrie.insert(word=word)
    with open('trie.pickle', 'wb') as f:
        pickle.dump(myTrie,f)
else:
    # Processes the valid query provided using 'query_manager' function defined in 'query.py'. Then, the program
    # prints the results using 'print_result' function defined in 'query.py'.
    if len(sys.argv) != 2:
        raise SystemExit("Please enter a valid query!")
    queryWord = sys.argv[1]
    result = query.query_manager(query=queryWord)
    query.print_result(queryWord,result)